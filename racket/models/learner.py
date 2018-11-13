import abc
import collections
import logging
import os
from typing import Iterable

import tensorflow.keras.backend as K
from tensorflow.keras import Sequential
from tensorflow.keras.models import model_from_json
from tensorflow.python.saved_model import builder as saved_model_builder, tag_constants
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def

from racket.managers.learner import LearnerManager
from racket.managers.server import ServerManager
from racket.managers.version import VersionManager
from racket.models import db
from racket.models.exceptions import TFSError
from racket.models.base import MLModel, ModelScores, MLModelType
from racket.models.helpers import get_or_create
from racket.operations.load import ModelLoader
from racket.operations.schema import activate, deactivate

log = logging.getLogger('root')


class Learner(abc.ABC):
    """
    Abstract Base Class for any learner implemented (currently Keras only, but more are planned).

    Note
    ----
    This as an abstract class and cannot be instantiated

    Attributes
    ----------
    semantic: str
        Semantic representation of the model version
    major : int
        Major version of the learner
    minor: int
        Minor version of the learner
    patch: int
        Patch version of the learner
    model_name: str
        Name of the model
    model_type: str
        Type of the model, either regression or classification
    _model: Any
        The instantiated model, such as a Keras compiled model
    _val_loss: dict
        Validation loss of the model according to the metrics defined in its implementation

    """
    VERSION = '0.0.1'
    MODEL_TYPE = ''
    MODEL_NAME = ''

    def __init__(self):
        self.vm = VersionManager()
        self.lm = LearnerManager()
        self.semantic, self.version_dir = self.vm.check_version(self.VERSION, self.MODEL_NAME)
        self.major, self.minor, self.patch = [int(i) for i in self.semantic.split('.')]
        self.model_type = self.MODEL_TYPE
        self.model_name = self.MODEL_NAME
        self._model = self.build_model()
        self._val_loss = None

    @abc.abstractmethod
    def model(self):
        raise NotImplementedError

    def get_or_create_path(self) -> str:
        p = self.lm.get_path(self.model_name)
        if not os.path.exists(p):
            os.makedirs(p, exist_ok=True)
        return p

    @property
    def path(self) -> str:
        """Path on disk of the model
        Returns
        -------
        str
        """

        return self.get_or_create_path()

    @property
    def sql(self) -> MLModel:
        """SQLized representation of model metadata

        Returns
        -------
        MLModel
            The SQLAlchemy representation of the model
        """
        values = {k: getattr(self, k) for k in ['model_name', 'major', 'minor', 'patch', 'version_dir']}
        values['type_id'] = get_or_create(MLModelType, 'type_name', 'type_id', self.model_type)[0]
        # noinspection PyArgumentList
        return MLModel(**values)

    @abc.abstractmethod
    def fit(self, x, y, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def store(self):
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def build_model(self):
        raise NotImplementedError  # pragma: no cover

    @property
    def keras_json(self) -> str:
        return self.path + '_' + self.version_dir + '.json'

    @property
    def keras_h5(self) -> str:
        return self.keras_json.replace('.json', '.h5')


class KerasLearner(Learner):
    """
    Base class providing functionality for training & storing a model
    """

    @property
    def model(self) -> Sequential:
        """
        Returns
        -------
        Sequential
            The compiled model
        """

        return self._model

    def get_last_loss(self) -> dict:
        return {k.replace('val_', ''): v[-1] for k, v in self.model.history.__dict__['history'].items()
                if k.startswith('val_')}

    @property
    def historic_scores(self) -> dict:
        """Only available when model has been fit. Provides access to the latest validation scores

        Returns
        -------
        dict
            Dictionary of metric scores ``{metric: score}``
        """

        latest_losses = self._val_loss or self.get_last_loss()
        self._val_loss = latest_losses
        return self._val_loss

    @historic_scores.setter
    def historic_scores(self, d: dict) -> None:
        self._val_loss = d

    @property
    def tf_path(self) -> str:
        """On disk path of the TensorFlow serialized model
        Returns
        -------
        str
        """

        return os.path.join(self.path, self.version_dir)

    def scores(self, x: Iterable, y: Iterable) -> object:
        """Evaluate scores on a test set

        Parameters
        ----------
        x : array_like
            A numpy array, or matrix that serves as input to the model. Must have matching dimensions
            to the model input specs

        y : array_like
            the targets for the input data

        Returns
        -------
        dict
            Dictionary of metric scores ``{metric: score}`` evaluated on the test set
        """

        score = self.model.evaluate(x, y)
        if isinstance(score, collections.Iterable):
            scores_ = dict(zip(self.model.metrics_names, score))
        else:
            scores_ = dict(zip(self.model.metrics_names, [score]))
        self._val_loss = scores_
        return scores_

    def build_model(self):
        """
        Abstract method. Must be overridden.
        Raises: ``NotImplementedError`` if called from base class
        """

        raise NotImplementedError  # pragma: no cover

    def fit(self, x, y, *args, **kwargs):
        """
        Abstract method. Must be overridden. \
        Raises: ``NotImplementedError`` if called from base class

        Parameters
        ----------
        x : array_like
            a numpy array, or matrix that serves as input to the model. Must have matching dimensions to the model input specs

        y : array_like
            the targets for the input data

        args
            Other parameters to be fed to the model
        kwargs
            Other parameters to be fed to the model
        """

        raise NotImplementedError  # pragma: no cover

    def store(self) -> None:
        """
        Stores the model in three different ways/patterns:

        1. Keras serialization, that is a json + h5 object, from which it can be loaded into a TensorFlow session
        2. TensorFlow protocol buffer + variables. That is the canonical TensorFlow way of storing models
        3. Metadata, scores, and info about the model are stored in a relational database for tracking purposes

        Returns
        -------
        None
        """

        if os.path.exists(self.tf_path):
            self.version_dir = self.vm.bump_disk(self.version_dir)

        with K.get_session() as sess:
            self._store_keras()
            self._store_tf(sess)
            self._store_meta()
            try:
                ModelLoader.load(self.model_name)
            except Exception as e:
                raise TFSError(f'Error loading trained model in TFS. Is TFS running? Full error: {e}')

    def _store_keras(self) -> None:
        K.set_learning_phase(0)  # prevent model from modifying weights
        model_json = self.model.to_json()
        with open(self.keras_json, 'w') as json_file:
            json_file.write(model_json)

        self.model.save_weights(self.keras_h5)
        log.info("Saved Keras model to disk")

    def _store_tf(self, session) -> None:

        json_model_file = open(self.keras_json, "r").read()
        loaded_model = model_from_json(json_model_file)
        loaded_model.load_weights(self.keras_h5)

        builder = saved_model_builder.SavedModelBuilder(self.tf_path)
        signature = predict_signature_def(inputs={'x': loaded_model.input},
                                          outputs={'y': loaded_model.output})

        builder.add_meta_graph_and_variables(sess=session,
                                             tags=[tag_constants.SERVING],
                                             signature_def_map={'helpers': signature})
        builder.save()

        log.info("Saved tf.txt model to disk")

    def _store_meta(self) -> None:
        app = ServerManager.create_app('prod', False)
        with app.app_context():
            deactivate()
            sqlized = self.sql
            db.session.add(sqlized)
            db.session.commit()
            activate()
            for scoring_function, score in self.historic_scores.items():
                obj = db.session.query(MLModel).order_by(MLModel.model_id.desc()).first()
                scoring_entry = ModelScores(model_id=obj.model_id, scoring_fn=scoring_function, score=score)
                db.session.add(scoring_entry)
            db.session.commit()

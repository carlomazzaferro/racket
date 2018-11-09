import os
import abc
import collections

from racket.models import db
from racket.models.helpers import get_or_create
from racket.models.base import MLModel, ModelScores, MLModelType
from racket.managers.learner import LearnerManager
import logging
import tensorflow.keras.backend as K
from tensorflow.keras.models import model_from_json
from tensorflow.python.saved_model import builder as saved_model_builder, tag_constants
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def

log = logging.getLogger('root')


class Learner(abc.ABC):

    VERSION = ''
    MODEL_TYPE = ''
    MODEL_NAME = ''

    def __init__(self):
        self.lm = LearnerManager()
        self.semantic, self.version_dir = self.lm.check_version(self.VERSION, self.MODEL_NAME)
        self.major, self.minor, self.patch = [int(i) for i in self.semantic.split('.')]
        self.model_type = self.MODEL_TYPE
        self.model_name = self.MODEL_NAME
        self._model = self.build_model()
        self._val_loss = None

    @abc.abstractmethod
    def model(self):
        raise NotImplementedError

    @property
    def get_or_create_path(self) -> str:
        p = self.lm.get_path(self.model_name)
        if not os.path.exists(p):
            os.makedirs(p, exist_ok=True)
        return p

    @property
    def path(self) -> str:
        return self.get_or_create_path

    @property
    def sql(self) -> MLModel:
        values = {k: getattr(self, k) for k in ['model_name', 'major', 'minor', 'patch', 'version_dir']}
        values['type_id'] = get_or_create(MLModelType, 'type_name', 'type_id', self.model_type)[0]
        return MLModel(**values)

    @abc.abstractmethod
    def fit(self, x, y, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def store(self):
        raise NotImplementedError

    @abc.abstractmethod
    def build_model(self):
        raise NotImplementedError

    @property
    def keras_json(self) -> str:
        return self.path + '_' + self.version_dir + '.json'

    @property
    def keras_h5(self) -> str:
        return self.keras_json.replace('.json', '.h5')


class KerasLearner(Learner):

    @property
    def model(self):
        return self._model

    def get_last_loss(self) -> dict:
        return {k.replace('val_', ''): v[-1] for k, v in self.model.history.__dict__['history'].items()
                if k.startswith('val_')}

    @property
    def historic_scores(self) -> dict:
        latest_losses = self._val_loss or self.get_last_loss()
        self._val_loss = latest_losses
        return self._val_loss

    @historic_scores.setter
    def historic_scores(self, d):
        self._val_loss = d

    def scores(self, x, y) -> dict:
        score = self.model.evaluate(x, y)
        if isinstance(score, collections.Iterable):
            scores_ = dict(zip(self.model.metrics_names, score))
        else:
            scores_ = dict(zip(self.model.metrics_names, [score]))
        self._val_loss = scores_
        return scores_

    def build_model(self):
        raise NotImplementedError

    def fit(self, x, y, *args, **kwargs):
        raise NotImplementedError

    def store(self) -> None:
        with K.get_session() as sess:
            self._store_keras()
            self._store_tf(sess)
            self._store_meta()

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

        builder = saved_model_builder.SavedModelBuilder(os.path.join(self.path, self.version_dir))
        signature = predict_signature_def(inputs={'x': loaded_model.input},
                                          outputs={'y': loaded_model.output})

        builder.add_meta_graph_and_variables(sess=session,
                                             tags=[tag_constants.SERVING],
                                             signature_def_map={'helpers': signature})
        builder.save()

        log.info("Saved tf.txt model to disk")

    def _store_meta(self) -> None:
        sqlized = self.sql
        db.session.add(sqlized)
        db.session.commit()

        for scoring_function, score in self.historic_scores.items():
            obj = db.session.query(MLModel).order_by(MLModel.model_id.desc()).first()
            scoring_entry = ModelScores(model_id=obj.model_id, scoring_fn=scoring_function, score=score)
            db.session.add(scoring_entry)
        db.session.commit()





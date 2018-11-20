from typing import Iterable

import tensorflow.keras.backend as K
from tensorflow.keras import Sequential

from racket.models.exceptions import TFSError
from racket.models.learner.base import Learner
from racket.models.serializers import t, meta
from racket.operations.load import ModelLoader


class TFLearner(Learner):
    """
    Base class providing functionality for training & storing a model
    """

    @property
    def serializers(self):
        kwargs = (self.path,
                  self.version_dir,
                  self.model,
                  self.model_name)
        return {
            'tf': t.TFSerializer(*kwargs),
            'meta': meta.MetadataSerializer(self.path, self.model_name)
        }

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
        pass

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

    def store(self, autoload: bool = False) -> None:
        """
        Stores the model in three different ways/patterns:

        1. Keras serialization, that is a json + h5 object, from which it can be loaded into a TensorFlow session
        2. TensorFlow protocol buffer + variables. That is the canonical TensorFlow way of storing models
        3. Metadata, scores, and info about the model are stored in a relational database for tracking purposes

        Parameters
        ----------
        autoload : bool
            Automatically load model into TensorFlow Serving. Will work only if the TFS docker container is running

        Returns
        -------
        None
        """

        with K.get_session() as sess:
            self.serializers['tf'].store(sess)
            self.serializers['meta'].store(sess)
            if autoload:
                try:
                    ModelLoader.load(self.model_name)
                except Exception as e:
                    raise TFSError(f'Error loading trained model in TFS. Is TFS running? Full error: {e}')

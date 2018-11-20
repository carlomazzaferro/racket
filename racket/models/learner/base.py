import abc
import logging
import os

from racket.managers.learner import LearnerManager

from racket.managers.version import VersionManager
from racket.models.base import MLModel

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
        self.major, self.minor, self.patch = self.vm.semantic_to_tuple(self.semantic)
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
    def historic_scores(self) -> dict:
        """Only available when model has been fit. Provides access to the latest validation scores

        Returns
        -------
        dict
            Dictionary of metric scores ``{metric: score}``
        """
        raise NotImplementedError

    @property
    def path(self) -> str:
        """Path on disk of the model
        Returns
        -------
        str
        """

        return self.get_or_create_path()

    @abc.abstractmethod
    def fit(self, x, y, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def store(self, autoload: bool = False):
        raise NotImplementedError  # pragma: no cover

    @abc.abstractmethod
    def build_model(self):
        raise NotImplementedError  # pragma: no cover

    @property
    def base_serializers(self):
        return

    @property
    def sql(self) -> MLModel:
        """SQLized representation of model metadata

        Returns
        -------
        MLModel
            The SQLAlchemy representation of the model
        """
        values = {k: getattr(self, k) for k in ['model_name', 'model_type', 'major', 'minor', 'patch', 'version_dir']}
        # noinspection PyArgumentList
        return MLModel(**values)

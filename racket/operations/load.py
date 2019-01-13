import logging

from tensorflow_serving.apis import model_management_pb2
from tensorflow_serving.config import model_server_config_pb2

from racket.managers.learner import LearnerManager
from racket.models.exceptions import CLIError
from racket.utils import Printer as p
from racket.models.channel import Channel
from racket.managers.server import ServerManager
from racket.operations.schema import __active

log = logging.getLogger('root')


def serve_model(model_id: int, model_name: str, version: str):
    """Serve a specific model.

    This allows you to specify either a model-id or a the name + version of a specific model that you'd like to serve.
        If the model-id is specified, the name and versions are ignored.

    Throws an error if the specified model do not exist.

    Parameters
    ----------
    model_id : int
        The desired model id to be loaded
    model_name : str
        The desired model name to be loaded. Must not be provided if model id is given
    version : str
        Semantic version, i.e. `1.1.20` of the model to be loaded
    """
    if (version != 'latest' and model_id) or (model_name and model_id):
        raise CLIError('You must specify either a model_id or a model_name + version, or just the model name ('
                       'in which case the default latest version will be used)')

    if not model_name and not model_id:
        raise CLIError('You must specify either a model_id or a model_name + version, or just the model name ('
                       'in which case the default latest version will be used)')

    if version == 'latest' and model_name:
        ModelLoader.load(model_name)

    else:
        app = ServerManager.create_app('prod', False)
        with app.app_context():
            active = __active()
            if model_id:
                servable = LearnerManager.query_by_id(model_id)
            else:
                servable = LearnerManager.query_by_name_version(model_name, version)
            if servable.model_id == active.model_id:
                p.print_warning('Model specified is already active')
                return
            else:
                LearnerManager.load_version_from_existing_servable(servable)
                ModelLoader.load(servable.model_name)


class ModelLoader:
    """
    This class provides the interface to load new models into TensorFlow Serving. This is implemented through a \
    gRPC call to the TFS api which triggers it to look for directories matching the name of the model specified
    """
    channel = Channel.service_channel()
    request = model_management_pb2.ReloadConfigRequest()
    model_server_config = model_server_config_pb2.ModelServerConfig()
    conf = model_server_config_pb2.ModelConfigList()

    @classmethod
    def set_config(cls, model_name: str) -> None:
        config = cls.conf.config.add()
        config.name = model_name
        config.base_path = '/models/' + model_name
        config.model_platform = 'tensorflow'
        cls.model_server_config.model_config_list.CopyFrom(cls.conf)
        cls.request.config.CopyFrom(cls.model_server_config)

    @classmethod
    def load(cls, model_name: str) -> None:
        """Load model

        This will send the gRPC request. In particular, it will open a gRPC channel and communicate with the \
        ReloadConfigRequest api to inform TFS of a change in configuration

        Parameters
        ----------
        model_name : str
            Name of the model, as specified in the instantiated Learner class

        Returns
        -------
        None
        """
        cls.set_config(model_name)
        log.info(cls.request.IsInitialized())
        log.info(cls.request.ListFields())

        response = cls.channel.HandleReloadConfigRequest(cls.request, ServerManager.PREDICTION_TIMEOUT)
        if response.status.error_code == 0:
            p.print_success(f'Loaded model {model_name} successfully')
        else:
            p.print_error(f'Loading failed, {response.status.error_code}: {response.status.error_message}')

import logging

from tensorflow_serving.apis import model_management_pb2
from tensorflow_serving.config import model_server_config_pb2

from racket.utils import Printer as p
from racket.models.channel import Channel
from racket.managers.server import ServerManager

log = logging.getLogger('root')


class ModelLoader:
    """
    This class provides the interface to load new models into TensorFlow Serving. This is implemented through a
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

        This will send the gRPC request. In particular, it will open a gRPC channel and communicate with the
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


if __name__ == '__main__':
    ModelLoader.load('keras-simple-regression')

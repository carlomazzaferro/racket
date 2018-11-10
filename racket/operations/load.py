import logging

from tensorflow_serving.apis import model_management_pb2
from tensorflow_serving.config import model_server_config_pb2

from racket.models.channel import Channel

log = logging.getLogger('root')


class ModelLoader:

    channel = Channel.service_channel()
    request = model_management_pb2.ReloadConfigRequest()
    model_server_config = model_server_config_pb2.ModelServerConfig()
    conf = model_server_config_pb2.ModelConfigList()

    @classmethod
    def set_config(cls, model_name):
        config = cls.conf.config.add()
        config.name = model_name
        config.base_path = '/models/' + model_name
        config.model_platform = 'tensorflow'
        cls.model_server_config.model_config_list.CopyFrom(cls.conf)
        cls.request.config.CopyFrom(cls.model_server_config)

    @classmethod
    def load(cls, model_name):
        cls.set_config(model_name)

        log.info(cls.request.IsInitialized())
        log.info(cls.request.ListFields())

        response = cls.channel.HandleReloadConfigRequest(cls.request, 10)
        if response.status.error_code == 0:
            log.info(f'Loaded model {model_name} successfully')
        else:
            log.warning(f'Loading failed, {response.status.error_code}: {response.status.error_message}')


if __name__ == '__main__':
    ModelLoader.load('keras-simple-lstm')

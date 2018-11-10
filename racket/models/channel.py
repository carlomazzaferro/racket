import logging

import grpc
from tensorflow_serving.apis import model_service_pb2_grpc
from tensorflow_serving.apis import prediction_service_pb2_grpc

log = logging.getLogger('root')


class Channel:
    host: str = 'localhost'
    port: str = '8500'
    channel = grpc.insecure_channel(host + ':' + port)

    @classmethod
    def service_channel(cls):
        return model_service_pb2_grpc.ModelServiceStub(cls.channel)

    @classmethod
    def prediction_channel(cls):
        return prediction_service_pb2_grpc.PredictionServiceStub(cls.channel)

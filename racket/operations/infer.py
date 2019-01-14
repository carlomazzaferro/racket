import logging

import numpy
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2

from racket.managers.server import ServerManager
from racket.models.channel import Channel

log = logging.getLogger('root')


class ServerTarget:
    channel = Channel.prediction_channel()
    request = predict_pb2.PredictRequest()

    @classmethod
    def set_config(cls, model_name: str) -> None:
        cls.request.model_spec.name = model_name
        cls.request.model_spec.signature_name = ServerManager.TF_MODEL_SIGNATURE_NAME

    @classmethod
    def predict(cls, model_name: str, tensor: numpy.ndarray) -> dict:
        cls.set_config(model_name)
        cls.request.inputs[ServerManager.TF_MODEL_INPUTS_KEY].CopyFrom(
            tf.make_tensor_proto(tensor, dtype=tf.float32)
        )
        result = cls.channel.Predict(cls.request, ServerManager.PREDICTION_TIMEOUT)
        return cls.format(result)

    @classmethod
    def format(cls, result) -> dict:
        result = numpy.array(result.outputs['y'].float_val)
        return {'result': result}


if __name__ == '__main__':
    print(ServerTarget.predict(numpy.array([[1.1, 2.3, 3.3, 4.3, 0]])))

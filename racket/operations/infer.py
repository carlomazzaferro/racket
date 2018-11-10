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
    def set_config(cls) -> None:
        cls.request.model_spec.name = ServerManager.TF_MODEL_NAME
        cls.request.model_spec.signature_name = ServerManager.TF_MODEL_SIGNATURE_NAME

    @classmethod
    def predict(cls, tensor: numpy.ndarray) -> dict:
        inputs = cls.request.inputs[ServerManager.TF_MODEL_INPUTS_KEY].CopyFrom(
            tf.make_tensor_proto(tensor, dtype=tf.float32)
        )
        result = cls.channel.Predict(inputs, ServerManager.PREDICTION_TIMEOUT)
        return cls.format(result)

    @classmethod
    def format(cls, result):
        result = numpy.array(result.outputs['y'].float_val)
        return {'result': result}

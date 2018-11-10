from racket.models.channel import Channel
from tensorflow_serving.apis.model_service_pb2_grpc import ModelServiceStub
from tensorflow_serving.apis.prediction_service_pb2_grpc import PredictionServiceStub


def test_channel():
    c = Channel()
    assert isinstance(c.prediction_channel(), PredictionServiceStub)
    assert isinstance(c.service_channel(), ModelServiceStub)
    assert c.channel

from racket.models.base import MLModel
from racket.models.helpers import get_or_create


def test_get_or_create():
    goc = get_or_create(MLModel, 'model_name', 'model_id', 'base')
    assert goc[0] == 1
    goc = get_or_create(MLModel, 'model_name', 'model_id', 'non-existing-model')
    assert goc[0] == 3

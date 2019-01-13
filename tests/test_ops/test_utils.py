import pytest

from racket.operations.utils import unfold, merge_result_sequences, merge_and_unfold
from racket.models.base import MLModel, MLModelInputs


@pytest.fixture
def sample_response():
    # noinspection PyArgumentList
    return [
        MLModel(model_name='m', major=1, minor=1, patch=0, model_type='reg'),
        MLModel(model_name='m1', major=1, minor=1, patch=0, model_type='reg'),
        MLModel(model_name='m2', major=1, minor=1, patch=0, model_type='reg'),
        MLModel(model_name='m1', major=1, minor=1, patch=2, model_type='reg'),
    ]


def test_unfold(sample_response):
    assert isinstance(unfold(sample_response), list)
    for i in unfold(sample_response):
        assert isinstance(i, dict)

    for i in unfold(sample_response, keep_keys=['model_name']):
        assert list(i.keys()) == ['model_name']

    for i in unfold(sample_response, filter_keys=['model_name']):
        print(i)
        assert 'model_id' in list(i.keys())
        assert 'major' in list(i.keys())
        assert 'version_dir' in list(i.keys())


def test_merge(sample_response):
    t_data = [{'a': 1, 'b': 2}, {'a': 0, 'b': -1}]
    t_data_1 = [{'c': 10, 'd': 5}, {'c': 2, 'd': 5}]
    merged = merge_result_sequences([t_data, t_data_1])
    assert isinstance(merged, list)
    assert list(merged[0].keys()) == ['a', 'b', 'c', 'd']
    combined_resp = [(m, MLModelInputs()) for m in sample_response]
    assert isinstance(merge_and_unfold(combined_resp), list)

import pytest

from racket.models.exceptions import ModelNotFoundError
from racket.operations.schema import list_models, active_model_, active_model_name_, current_schema_, query_by_id_, \
    model_filterer_, query_scores_
from racket.utils import dict_tabulate


def test_list_models(capfd, init_project):
    dict_tabulate(list_models())
    out, err = capfd.readouterr()
    assert 'model_id' in out
    assert 'model_name' in out
    assert 'base' in out
    assert 'regression' in out


def test_query_active(init_project):
    a = active_model_(scores=True)
    assert isinstance(a, list)
    assert len(a[0]) == 2


def test_active_model_name(init_project):
    a = active_model_name_()
    assert a == 'test'


def test_q_current_schema(init_project):
    with pytest.raises(NotImplementedError):
        _ = current_schema_()


def test_q_by_id(init_project):
    a = query_by_id_(model_id=1, scores=True)
    assert isinstance(a, list)
    assert len(a[0]) == 2
    with pytest.raises(ModelNotFoundError):
        _ = query_by_id_(model_id=34234321, scores=False)


def test_model_filterer(init_project):
    a = model_filterer_(name='test', scores=False)
    assert isinstance(a, list)
    assert a[0].model_id == 45

    a = model_filterer_(version='1.1.1', scores=False)
    assert a[0].model_name == 'test'

    a = model_filterer_(m_type='regression', scores=False)
    assert a[0].model_name == 'base'


def test_query_scores(init_project):
    a = query_scores_(model_id=45)
    assert isinstance(a, list)
    assert a[0].model_id == 45

    a = query_scores_(version='1.1.1', name='test')
    assert isinstance(a, list)
    assert a[0].model_id == 45
    assert a[0].score == 0.9
    assert a[1].score == 1

    with pytest.raises(ValueError):
        _ = query_scores_(version='1.1.1')

    with pytest.raises(ValueError):
        _ = query_scores_(version='1.1.39423', name='test')


from racket.operations.schema import list_models
from racket.utils import dict_tabulate


def test_list_models(capfd, init_project):
    dict_tabulate(list_models())
    out, err = capfd.readouterr()
    assert 'model_id' in out
    assert 'model_name' in out
    assert 'base' in out
    assert 'regression' in out


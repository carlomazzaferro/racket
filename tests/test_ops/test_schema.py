from racket.operations.schema import list_models


def test_list_models(capfd, init_project):
    list_models()
    out, err = capfd.readouterr()
    assert 'model_id' in out
    assert 'model_name' in out
    assert 'base' in out
    assert 'regression' in out
    #
    # list_models(active=True)
    # out, err = capfd.readouterr()
    # assert 'model_id' in out
    # assert 'model_name' in out
    # assert 'base' in out
    # assert 'regression' in out
    #

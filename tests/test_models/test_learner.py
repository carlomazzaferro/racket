import os
import shutil

import pytest
from tensorflow.keras.models import Sequential

from racket.models.learner.base import Learner


# noinspection PyTypeChecker,PyCallByClass
def test_abcs():
    with pytest.raises(TypeError):
        _ = Learner()

    with pytest.raises(NotImplementedError):
        _ = Learner.model(Learner)

    with pytest.raises(NotImplementedError):
        _ = Learner.fit(Learner, None, None)


# noinspection PyTypeChecker,PyCallByClass,PyProtectedMember
def test_concrete_methods(instantiated_learner, init_project):
    p = instantiated_learner.get_or_create_path()
    assert os.path.exists(p)
    shutil.rmtree(p)

    assert instantiated_learner.path == instantiated_learner.get_or_create_path()
    shutil.rmtree(p)

    assert instantiated_learner._val_loss is None
    instantiated_learner.historic_scores = 1
    assert instantiated_learner._val_loss == 1
    shutil.rmtree('serialized')


# noinspection PyProtectedMember
def test_on_trained_model(instantiated_learner, sample_data, init_project):
    x_tr, x_te, y_tr, y_te = sample_data

    instantiated_learner._val_loss = None
    instantiated_learner.fit(x_tr, y_tr, x_val=x_te, y_val=y_te)
    assert isinstance(instantiated_learner.historic_scores, dict)
    ll = instantiated_learner.scores(x_te, y_te)
    assert isinstance(ll, dict)
    assert 'loss' in ll.keys()

    with pytest.raises(Exception):
        instantiated_learner.store(autoload=True)
    assert os.path.exists('serialized/keras-complex-lstm_1.h5')
    shutil.rmtree('serialized')


def test_kl(instantiated_learner, init_project):
    assert instantiated_learner.VERSION == '1.2.1'
    assert instantiated_learner.MODEL_TYPE == 'regression'
    assert instantiated_learner.MODEL_NAME == 'keras-complex-lstm'
    assert isinstance(instantiated_learner.build_model(), Sequential)
    assert instantiated_learner.model.built is True

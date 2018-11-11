import os
import shutil

import pytest
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.metrics import mse
from tensorflow.keras.models import Sequential

from racket.models.base import MLModel
from racket.models.learner import Learner, KerasLearner


@pytest.fixture(scope='session')
def instantiated_learner():
    class KerasModel(KerasLearner):
        VERSION = '1.2.1'
        MODEL_TYPE = 'regression'
        MODEL_NAME = 'keras-complex-lstm'

        def build_model(self):
            optimizer = tf.train.RMSPropOptimizer(0.001)
            model = Sequential()
            model.add(Dense(3, input_dim=5, kernel_initializer='normal', activation='relu'))
            model.add(Dense(4, kernel_initializer='normal', activation='relu'))
            model.add(Dense(1, kernel_initializer='normal'))
            model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=[mse])
            return model

        def fit(self, x, y, x_val=None, y_val=None, epochs=10, batch_size=2):
            self.model.fit(x, y, epochs=epochs, verbose=0, validation_data=(x_val, y_val))

    kl = KerasModel()
    return kl


# noinspection PyTypeChecker,PyCallByClass
def test_abcs():
    with pytest.raises(TypeError):
        _ = Learner()

    with pytest.raises(NotImplementedError):
        _ = Learner.model(Learner)

    with pytest.raises(NotImplementedError):
        _ = Learner.fit(Learner, None, None)


# noinspection PyTypeChecker,PyCallByClass,PyProtectedMember
def test_concrete_methods(instantiated_learner):
    p = instantiated_learner.get_or_create_path()
    assert os.path.exists(p)
    shutil.rmtree(p)

    assert instantiated_learner.path == instantiated_learner.get_or_create_path()
    shutil.rmtree(p)

    assert isinstance(instantiated_learner.sql, MLModel)

    assert instantiated_learner.keras_json == p + '_1.json'
    assert instantiated_learner.keras_h5 == p + '_1.h5'
    assert p in instantiated_learner.tf_path

    assert instantiated_learner._val_loss is None
    instantiated_learner.historic_scores = 1
    assert instantiated_learner._val_loss == 1
    shutil.rmtree('serialized')


# noinspection PyProtectedMember
def test_on_trained_model(instantiated_learner, sample_data):
    x_tr, x_te, y_tr, y_te = sample_data

    instantiated_learner._val_loss = None
    instantiated_learner.fit(x_tr, y_tr, x_val=x_te, y_val=y_te)
    assert isinstance(instantiated_learner.historic_scores, dict)
    ll = instantiated_learner.scores(x_te, y_te)
    assert isinstance(ll, dict)
    assert 'loss' in ll.keys()

    instantiated_learner.store()
    assert os.path.exists('serialized/keras-complex-lstm_1.h5')
    shutil.rmtree('serialized')


def test_kl(instantiated_learner):
    assert instantiated_learner.VERSION == '1.2.1'
    assert instantiated_learner.MODEL_TYPE == 'regression'
    assert instantiated_learner.MODEL_NAME == 'keras-complex-lstm'
    assert isinstance(instantiated_learner.build_model(), Sequential)
    assert instantiated_learner.model.built is True

import os
import shutil

import pytest
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Dense
from tensorflow.keras.losses import mse

from racket import KerasLearner
from racket.managers.project import ProjectManager
from racket.operations.schema import active_model_


@pytest.fixture(scope='function')
def create_proj():
    ProjectManager.init('.', 'sample_project')
    yield
    shutil.rmtree('sample_project')


@pytest.fixture
def learner():
    class KerasModel(KerasLearner):
        VERSION = '1.2.1'
        MODEL_TYPE = 'regression'
        MODEL_NAME = 'keras-complex-lstm'

        def build_model(self):
            optimizer = tf.train.RMSPropOptimizer(0.001)
            model = Sequential()
            model.add(Dense(3, input_dim=5, kernel_initializer='normal', activation='relu'))
            model.add(Dense(1, kernel_initializer='normal'))
            model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=[mse])
            return model

        def fit(self, x, y, x_val=None, y_val=None, epochs=2, batch_size=2):
            self.model.fit(x, y, epochs=epochs, verbose=0, validation_data=(x_val, y_val))

    return KerasModel


def fit_store_model(l, v, sample_data, change_name=None):
    x_tr, x_te, y_tr, y_te = sample_data
    if change_name:
        l.MODEL_NAME = change_name
    l.VERSION = v
    le = l()
    le.fit(x_tr, y_tr, x_val=x_te, y_val=y_te)
    le.store(autoload=False)
    K.clear_session()


def assert_query_works(vals):
    from racket.managers.server import ServerManager

    app = ServerManager.create_app('prod', False)
    with app.app_context():
        active = active_model_()
        a = isinstance(active, dict)
        b = active['model_id'] == int(vals)
        c = active['version_dir'] == str(vals)
    if all([a, b, c]):
        return True
    else:
        return False


def test_create_multiple(learner, sample_data, create_proj):
    patch_bump = ['.'.join(['0', '0', str(i + 1)]) for i in range(15)]
    minor_bump = ['.'.join(['0', str(i + 1), '5']) for i in range(10)]
    major_bump = ['.'.join([str(i + 1), str(i), '0']) for i in range(10)]
    name_change = ['0.2.4', '0.2.5', '0.3.1', '1.0.0']

    os.chdir('sample_project')
    ProjectManager.RACKET_DIR = '.'

    for v in patch_bump:
        fit_store_model(learner, v, sample_data)

    assert assert_query_works('16') is True

    for m in minor_bump:
        fit_store_model(learner, m, sample_data)

    assert assert_query_works('26') is True

    for M in major_bump:
        fit_store_model(learner, M, sample_data)

    assert assert_query_works('36') is True

    for n in name_change:
        fit_store_model(learner, n, sample_data, change_name='keras-other-model')

    from racket.managers.server import ServerManager
    app = ServerManager.create_app('prod', False)
    with app.app_context():
        active = active_model_(name=True)
        assert isinstance(active, str)
        assert active == 'keras-other-model'

    os.chdir('../')

import shutil
import os

import numpy
import pytest
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.losses import mse

from racket import KerasLearner
from racket.managers.project import ProjectManager


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


@pytest.fixture(scope='session')
def init_project():
    ProjectManager.init('tests', 'sample_project')
    yield
    os.chdir('../')
    shutil.rmtree('sample_project')


@pytest.fixture
def sample_data():
    x_tr = numpy.array([[1.51056886, -1.10391378, 0.83966854, -0.38076806, -1.28748887],
                        [-1.98789246, -0.40725765, 0.53758981, 0.39959485, -2.03600702],
                        [1.74334494, -1.01190045, 0.15248708, -0.73862008, 2.73005256],
                        [1.01596461, -0.43746054, -0.47035088, 0.12761908, -1.40538919],
                        [-0.85529551, -0.65163851, -1.02298002, 1.34480648, -1.09345988],
                        [-0.16468608, -1.20990292, 0.2967414, -0.21567038, 0.04117535],
                        [0.37387182, -0.67070869, 0.04786631, 0.80555065, 1.43579999]])

    x_te = numpy.array([[-0.59071176, -0.99329361, 0.49799128, 0.5062066, 0.56500408],
                        [-0.65697283, 1.17548768, -0.42178183, -0.47219576, -0.77634661],
                        [0.0764596, 1.19363889, -0.67655733, 0.60724056, -0.44658216]])

    y_tr = numpy.array([23.2619347, -281.71966776, 304.89544539, -78.44385254,
                        -227.98436845, -37.65778507, 122.51348244])

    y_te = numpy.array([-1.75175537, -95.32782004, -22.154719])
    return x_tr, x_te, y_tr, y_te

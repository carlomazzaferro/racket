from sklearn.datasets import make_regression
import tensorflow as tf

from racket.models.learner.k import KerasLearner

from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import TensorBoard
from time import time


tensorboard = TensorBoard(log_dir="logs/{}".format(time()))


class KerasModel(KerasLearner):

    VERSION = '1.1.1'
    MODEL_TYPE = 'regression'
    MODEL_NAME = 'keras-simple-regression'

    def build_model(self):
        optimizer = tf.train.RMSPropOptimizer(0.001)
        model = Sequential()
        model.add(Dense(24, input_dim=5, kernel_initializer='normal', activation='relu'))
        model.add(Dense(48, kernel_initializer='normal', activation='relu'))
        model.add(Dense(1, kernel_initializer='normal'))
        model.compile(loss='mean_absolute_error', optimizer=optimizer)
        return model

    def fit(self, x, y, x_val=None, y_val=None, epochs=2, batch_size=20):
        self.model.fit(x, y, epochs=epochs, verbose=0, validation_data=(x_val, y_val))


if __name__ == '__main__':
    x, y = make_regression(n_samples=1250, n_features=5,  n_informative=5)
    X_train, X_test, y_train, y_test = train_test_split(x, y)
    kf = KerasModel()
    kf.fit(X_train, y_train, x_val=X_test, y_val=y_test)
    kf.store(autoload=True)

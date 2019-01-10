from time import time

import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.datasets.fashion_mnist import load_data
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.python.keras.layers import Flatten

from racket.models.learner.k import KerasLearner

tensorboard = TensorBoard(log_dir="logs/{}".format(time()))


def get_data():
    (x_tr, y_tr), (x_te, y_te) = load_data()
    x_tr = x_tr/255.0
    x_te = x_te/255.0
    return (x_tr, y_tr), (x_te, y_te)


class KerasModel(KerasLearner):
    VERSION = '1.0.0'
    MODEL_TYPE = 'classification'
    MODEL_NAME = 'base-model'

    def build_model(self):
        model = Sequential([
            Flatten(input_shape=(28, 28)),
            Dense(128, activation=tf.nn.relu),
            Dense(10, activation=tf.nn.softmax)
        ])
        model.compile(optimizer=tf.train.AdamOptimizer(),
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        return model

    def fit(self, x, y, x_val=None, y_val=None, epochs=3, batch_size=64):
        self.model.fit(x, y, epochs=epochs,
                       batch_size=batch_size, verbose=2, validation_data=(x_val, y_val),
                       callbacks=[tensorboard])
        test_loss, test_acc = self.model.evaluate(x_val, y_val)

        print('Test accuracy:', test_acc)
        print('Test loss:', test_loss)


if __name__ == '__main__':
    (x_train, y_train), (x_test, y_test) = get_data()
    m = KerasModel()
    m.fit(x_train, y_train, x_val=x_test, y_val=y_test)
    m.store(autoload=True)

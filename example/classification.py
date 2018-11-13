from racket.models.learner import KerasLearner

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.optimizers import Adam

from tensorflow.python.keras import utils
from sklearn.preprocessing import LabelEncoder


from time import time


tensorboard = TensorBoard(log_dir="logs/{}".format(time()))


class KerasModel(KerasLearner):

    VERSION = '1.0.0'
    MODEL_TYPE = 'regression'
    MODEL_NAME = 'keras-simple-regression'

    def build_model(self):
        adam = Adam(lr=0.1, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.01, amsgrad=False)

        model = Sequential()
        model.add(Dense(3, input_dim=4, activation='relu'))
        model.add(Dense(2, activation='softmax'))
        model.compile(loss='binary_crossentropy', optimizer=adam)
        return model

    def fit(self, x, y, x_val=None, y_val=None, epochs=15, batch_size=64):
        self.model.fit(x, y, epochs=epochs,
                       batch_size=batch_size, verbose=2, validation_data=(x_val, y_val),
                       callbacks=[tensorboard])


if __name__ == '__main__':
    x, y = make_classification(n_samples=150, n_features=4, n_classes=2, shuffle=True, class_sep=0.2)

    encoder = LabelEncoder()
    encoder.fit(y)
    encoded_Y = encoder.transform(y)
    # convert integers to dummy variables (i.e. one hot encoded)
    dummy_y = utils.np_utils.to_categorical(encoded_Y)

    X_train, X_test, y_train, y_test = train_test_split(x, dummy_y, test_size=0.2)
    m = KerasModel()
    m.fit(X_train, y_train, x_val=X_test, y_val=y_test)

    from racket.metrics import Metric

    pred = m.model.predict(X_test)
    print(pred)
    print(y_test)
    import numpy
    from sklearn.metrics import classification_report

    import tensorflow.keras.backend as K
    import tensorflow as tf
    from tensorflow.keras.metrics import categorical_accuracy, binary_accuracy
    K.get_session().run(tf.local_variables_initializer())

    print(K.eval(categorical_accuracy(y_test, pred)))


import json

import tensorflow.keras.backend as K
from tensorflow.python.client.session import Session

from racket.models.serializers.t import TFSerializerBase, TFSerializer
from racket.utils import Printer as p


class KerasSerializer(TFSerializerBase):

    def store(self, session: Session) -> None:
        self.store_history()
        K.set_learning_phase(0)  # prevent model from modifying weights
        model_json = self.model.to_json()
        with open(self.keras_json, 'w') as json_file:
            json_file.write(model_json)

        self.model.save_weights(self.keras_h5)
        p.print_success(f'Successfully stored Keras model: {self.model_name}')
        tf_serializer = TFSerializer(self.path, self.version_dir, self.model, self.model_name)
        tf_serializer.store(session, from_keras=True)

    def store_history(self):
        with open(self.keras_history, 'w') as history:
            json.dump(str(self.model.history.history), history)

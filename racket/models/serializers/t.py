from typing import Tuple
import os

from tensorflow.python.client.session import Session
from tensorflow.python.keras.models import model_from_json, Sequential
from tensorflow.python.saved_model import builder as saved_model_builder, tag_constants
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def

from racket.models.serializers.base import ModelSerializer
from racket.utils import Printer as p
from racket.managers.version import VersionManager


class TFSerializerBase(ModelSerializer):
    def __init__(self, path: str, version_dir: str, model: Sequential, model_name: str):
        super().__init__(path, model_name)
        self.version_dir = version_dir
        self.model = model
        if os.path.exists(self.tf_path):
            self.version_dir = VersionManager.bump_disk(self.version_dir)

    @property
    def tf_path(self) -> str:
        """On disk path of the TensorFlow serialized model
        Returns
        -------
        str
        """

        return os.path.join(self.path, self.version_dir)

    @property
    def keras_json(self) -> str:
        return self.path + '_' + self.version_dir + '.json'

    @property
    def keras_h5(self) -> str:
        return self.keras_json.replace('.json', '.h5')


class TFSerializer(TFSerializerBase):
    # TODO: make this builder more flexible as far as defining the signature def inputs
    def store(self, session: Session, from_keras: bool = False, inputs: Tuple = None) -> None:
        if from_keras:
            json_model_file = open(self.keras_json, "r").read()
            loaded_model = model_from_json(json_model_file)
            loaded_model.load_weights(self.keras_h5)
            x_in, y_in = loaded_model.input, loaded_model.output
        else:
            x_in, y_in = inputs

        builder = saved_model_builder.SavedModelBuilder(self.tf_path)
        signature = predict_signature_def(inputs={'x': x_in},
                                          outputs={'y': y_in})

        builder.add_meta_graph_and_variables(sess=session,
                                             tags=[tag_constants.SERVING],
                                             signature_def_map={'helpers': signature})
        builder.save()
        p.print_success(f'Successfully stored TensorFlow model: {self.model_name}')


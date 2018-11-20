
class ModelSerializer:

    def __init__(self, path: str, model_name: str):
        self.path = path
        self.model_name = model_name

    def store(self, *args, **kwargs):
        return NotImplementedError

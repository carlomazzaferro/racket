import pkgutil
import os
from racket.managers.constants import TEMPLATE_PROJECT_FILES, TEMPLATE_PROJECT_DIRS
from racket.managers.base import BaseConfigManager
from racket.models.exceptions import NotInitializedError


class ProjectManager(BaseConfigManager):
    """Manages project configuration racket.yaml file."""

    IS_GLOBAL = False
    RACKET_DIR = None
    CONFIG_FILE_NAME = 'racket.yaml'
    CONFIG = None

    @classmethod
    def set_path(cls, path):
        cls.RACKET_DIR = path

    @classmethod
    def init_project(cls):
        cls.init_config()
        cls.create_template()

    @classmethod
    def create_template(cls):
        cls.create_subdirs()
        for file in TEMPLATE_PROJECT_FILES:
            data = pkgutil.get_data('racket', file)
            file_path = file.replace('template/', '')
            with open(os.path.join(cls.RACKET_DIR, file_path), 'w') as f:
                f.write(data.decode('utf-8'))

    @classmethod
    def create_subdirs(cls):
        for path in TEMPLATE_PROJECT_DIRS:
            os.makedirs(os.path.join(cls.RACKET_DIR, path), exist_ok=True)

    @classmethod
    def get_models(cls):
        if not cls.is_initialized():
            raise NotInitializedError('Project must be initialized first with `racket init`')
        models = os.listdir(cls.get_value('saved-models'))
        return sorted([int(i) for i in models if i.isnumeric()])

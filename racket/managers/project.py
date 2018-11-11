import os
import pkgutil

from racket.managers.base import BaseConfigManager
from racket.managers.constants import TEMPLATE_PROJECT_FILES, TEMPLATE_PROJECT_DIRS
from racket.models.exceptions import NotInitializedError


class ProjectManager(BaseConfigManager):
    """Manages project configuration racket.yaml file."""

    IS_GLOBAL: bool = False
    RACKET_DIR: str = None
    CONFIG_FILE_NAME: str = 'racket.yaml'
    CONFIG: dict = None

    @classmethod
    def set_path(cls, path: str) -> None:
        cls.RACKET_DIR = path

    @classmethod
    def init_project(cls, name: str) -> None:
        cls.init_config(name)
        cls.create_template()

    @classmethod
    def create_template(cls) -> None:
        cls.create_subdirs()
        for file in TEMPLATE_PROJECT_FILES:
            data = pkgutil.get_data('racket', file)
            file_path = file.replace('template/', '')
            with open(os.path.join(cls.RACKET_DIR, file_path), 'w') as f:
                f.write(data.decode('utf-8'))

    @classmethod
    def create_subdirs(cls) -> None:
        for path in TEMPLATE_PROJECT_DIRS:
            os.makedirs(os.path.join(cls.RACKET_DIR, path), exist_ok=True)

    @classmethod
    def get_models(cls) -> list:
        if not cls.is_initialized():
            raise NotInitializedError('Project must be initialized first with `racket init`')
        models = os.listdir(cls.get_value('saved-models'))
        return sorted([int(i) for i in models if i.isnumeric()])

    @classmethod
    def db_path(cls) -> str:
        db = cls.get_value('db')
        if db['type'] == 'sqlite':
            return 'sqlite:///' + os.path.join(os.getcwd(), db['connection'])
        else:
            return db['connection']

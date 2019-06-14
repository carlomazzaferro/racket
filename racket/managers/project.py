import os
import sys
import pkgutil
import json

from racket.managers.base import BaseConfigManager
from racket.managers.constants import TEMPLATE_PROJECT_FILES, TEMPLATE_PROJECT_DIRS, WEB_MANIFEST
from racket.models.exceptions import NotInitializedError


class ProjectManager(BaseConfigManager):
    """Manages project configuration racket.yaml file."""

    RACKET_DIR: str = None
    CONFIG_FILE_NAME: str = 'racket.yaml'
    CONFIG: dict = None

    @classmethod
    def set_path(cls, path: str) -> None:
        cls.RACKET_DIR = path

    @classmethod
    def init(cls, path: str, name: str) -> None:
        path = os.path.join(path, name)
        cls.create_dir(path)
        cls.set_path(path)
        cls.init_config(name)
        cls.create_template()
        cls.initiate_db()

    @classmethod
    def init_project(cls, path: str, name: str) -> None:
        project_path = os.path.join(path, name)
        if os.path.isdir(project_path):
            cls.safe_init(project_path, name)
        else:
            cls.init(path, name)

    @classmethod
    def safe_init(cls, path: str, name: str) -> None:
        overwrite = input('WARNING: Path specified already exists. Any configuration will be overwritten. Proceed?[Y/n]')
        if overwrite == 'Y':
            cls.init(path, name)
        elif overwrite == 'n':
            sys.exit()
        else:
            cls.safe_init(path, name)

    @classmethod
    def create_template(cls) -> None:
        cls.create_subdirs()
        cls.copy_dist_files()
        cls.create_web_dir()

    @classmethod
    def copy_dist_files(cls) -> None:
        for file in TEMPLATE_PROJECT_FILES:
            data = pkgutil.get_data('racket', file)
            cls._copy_file(file, data)

    @classmethod
    def create_web_dir(cls) -> None:
        for k, v in WEB_MANIFEST.items():
            data = pkgutil.get_data('racket', v)
            cls._copy_file(v, data)

        asset_manifest = WEB_MANIFEST['assets']
        data = pkgutil.get_data('racket', asset_manifest)
        extras = json.loads(data, encoding='utf-8')['files'].values()
        for f in extras:
            real_path = os.path.join('template/web', f[1:])
            data = pkgutil.get_data('racket', real_path)
            cls._copy_file(real_path, data)

    @classmethod
    def create_subdirs(cls) -> None:
        for path in TEMPLATE_PROJECT_DIRS:
            os.makedirs(os.path.join(cls.RACKET_DIR, path), exist_ok=True)

    @classmethod
    def _copy_file(cls, file, data, replace_path=''):
        file_path = file.replace('template/', replace_path)
        try:
            with open(os.path.join(cls.RACKET_DIR, file_path), 'w') as f:
                f.write(data.decode('utf-8'))
        except UnicodeDecodeError:
            with open(os.path.join(cls.RACKET_DIR, file_path), 'wb') as f:
                f.write(data)

    @classmethod
    def get_models(cls) -> list:
        if not cls.is_initialized():
            raise NotInitializedError('Project must be initialized first with `racket init`')
        models = os.listdir(cls.get_value('saved-models'))
        return sorted([int(i) for i in models if i.isnumeric()])

    @classmethod
    def db_path(cls) -> str:
        if cls.RACKET_DIR is not None:
            if cls.RACKET_DIR not in os.getcwd():
                db_dir = os.path.join(os.path.join(os.getcwd(), cls.RACKET_DIR))
            else:
                db_dir = os.getcwd()
        else:
            db_dir = os.getcwd()
        db = cls.get_value('db')
        if db['type'] == 'sqlite':
            return 'sqlite:///' + os.path.join(db_dir, db['connection'])
        else:
            return db['connection']

    # noinspection PyArgumentList
    @classmethod
    def initiate_db(cls) -> None:
        from racket.managers.server import ServerManager
        ServerManager.create_app('prod', True)


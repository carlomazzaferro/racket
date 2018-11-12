import os
import sys
import pkgutil
from datetime import datetime

from racket.managers.base import BaseConfigManager
from racket.managers.constants import TEMPLATE_PROJECT_FILES, TEMPLATE_PROJECT_DIRS
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
        cls.create_db()

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
        for file in TEMPLATE_PROJECT_FILES:
            data = pkgutil.get_data('racket', file)
            file_path = file.replace('template/', '')
            try:
                with open(os.path.join(cls.RACKET_DIR, file_path), 'w') as f:
                    f.write(data.decode('utf-8'))
            except UnicodeDecodeError:
                with open(os.path.join(cls.RACKET_DIR, file_path), 'wb') as f:
                    f.write(data)

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
    def create_db(cls) -> None:
        from racket.managers.server import ServerManager
        from racket.models import db
        from racket.models.base import MLModel, ModelScores, MLModelType

        m = MLModel(model_id=1, model_name='base', major=0, minor=1, patch=0, version_dir=1, active=True,
                    created_at=datetime.now(), type_id=1)
        t = MLModelType(type_id=1, type_name='regression')
        s = ModelScores(id=1, model_id=1, scoring_fn='loss', score=9378.2468363119)
        mse = ModelScores(id=2, model_id=1, scoring_fn='mean_squared_error', score=9378.2468363119)
        app = ServerManager.create_app('dev', True)
        with app.app_context():
            db.session.add(m)
            db.session.add(t)
            db.session.add(s)
            db.session.add(mse)
        db.session.commit()


import os
import pkgutil
from datetime import datetime

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
            print(file_path, 'PATHHHH')
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

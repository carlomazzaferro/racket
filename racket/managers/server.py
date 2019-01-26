import os
from datetime import datetime

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from racket.conf import config_by_name
from racket.managers.project import ProjectManager
from racket.models.base import MLModel, ModelScores, ActiveModel
from racket.models.exceptions import validate_config


class ServerManager(ProjectManager):
    # client settings
    DEFAULT_TF_SERVER_NAME: str = 'localhost'
    DEFAULT_TF_SERVER_PORT: int = 8501
    TF_MODEL_SIGNATURE_NAME: str = 'helpers'
    TF_MODEL_INPUTS_KEY: str = 'x'
    PREDICTION_TIMEOUT: int = 10

    @classmethod
    def create_db(cls, database: SQLAlchemy, clean: bool) -> None:
        database.session.commit()
        if clean:
            database.drop_all()
        database.create_all()
        try:
            cls.create_inital_state(database)
        except IntegrityError:
            pass

    # noinspection PyArgumentList
    @classmethod
    def create_inital_state(cls, database: SQLAlchemy):
        m = MLModel(model_id=1, model_name='base', major=0, minor=1, patch=0, version_dir=1,
                    created_at=datetime.now(), model_type='regression')
        s = ModelScores(id=1, model_id=1, scoring_fn='loss', score=9378.2468363119)
        a = ActiveModel(model_id=1)
        database.session.add(m)
        database.session.add(s)
        database.session.add(a)
        database.session.commit()

    @classmethod
    def create_app(cls, env: str, clean: bool) -> Flask:
        app = Flask(__name__,
                    static_folder=cls.static_files_dir() if not env == 'test' else None,
                    template_folder=cls.template_files_dir() if not env == 'test' else None
                    )

        @app.route('/')
        def index():
            return send_from_directory(cls.template_files_dir(), "index.html")

        app.config.from_object(config_by_name[env])
        app.config['SQLALCHEMY_DATABASE_URI'] = ProjectManager.db_path()

        from racket.api import api_bp
        from racket.models import db

        with app.app_context():
            db.app = app
            db.init_app(app)
            cls.create_db(db, clean)
        app.register_blueprint(api_bp, url_prefix='/api/v1')

        return app

    @classmethod
    @validate_config
    def run(cls, host: str, port: int, env: str, clean: bool = False) -> None:
        app = cls.create_app(env, clean)
        app.run(host, port)

    @classmethod
    def static_files_dir(cls, dirpath: str = None) -> str:
        return os.path.join(os.getcwd(), cls.get_value('dashboard')['STATIC_FILES_DIR'])

    @classmethod
    def template_files_dir(cls, dirpath: str = None) -> str:
        return os.path.join(os.getcwd(), cls.get_value('dashboard')['TEMPLATE_FILES_DIR'])

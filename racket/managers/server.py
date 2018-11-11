import os

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy

from racket.conf import config_by_name
from racket.managers.base import BaseConfigManager
from racket.managers.project import ProjectManager


class ServerManager(BaseConfigManager):
    # client settings
    DEFAULT_TF_SERVER_NAME: str = 'localhost'
    DEFAULT_TF_SERVER_PORT: int = 8501
    TF_MODEL_NAME: str = 'default'
    TF_MODEL_SIGNATURE_NAME: str = 'helpers'
    TF_MODEL_INPUTS_KEY: str = 'x'
    PREDICTION_TIMEOUT: int = 10

    @classmethod
    def create_db(cls, database: SQLAlchemy, clean: bool) -> None:
        database.session.commit()
        if clean:
            database.drop_all()
        database.create_all()

    @classmethod
    def create_app(cls, env: str, clean: bool) -> Flask:
        app = Flask(__name__,
                    static_folder=cls.static_files_dir(),
                    template_folder=cls.react_dist_dir()
                    )
        app.config.from_object(config_by_name[env])
        app.config['SQLALCHEMY_DATABASE_URI'] = ProjectManager.db_path()

        from racket.api import api_bp
        from racket.models import db

        with app.app_context():
            db.app = app
            db.init_app(app)
            cls.create_db(db, clean)
        app.register_blueprint(api_bp, url_prefix='/api/v1')

        @app.route('/')
        def index():
            return send_from_directory(cls.react_dist_dir(), "index.html")

        return app

    @classmethod
    def run(cls, host: str, port: int, env: str, clean: bool) -> None:
        app = cls.create_app(env, clean)
        app.run(host, port)

    @classmethod
    def static_files_dir(cls) -> str:
        return os.path.join(os.getcwd(), 'racket/web/build/static')

    @classmethod
    def react_dist_dir(cls) -> str:
        return os.path.join(os.getcwd(), 'racket/web/build')

from datetime import datetime

from flask import Flask, send_from_directory
from flask_cors import CORS
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
                    created_at=datetime.now(), model_type='regression', parameters='{"batch_size": 64, "epochs": 3}')
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
        CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers="*")
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
        if env == 'gunicorn':
            cls.run_gunicorn(host, port)
            return
        app = cls.create_app(env, clean)
        app.run(host, port)

    @classmethod
    def static_files_dir(cls) -> str:
        return os.path.join(os.getcwd(), cls.get_value('dashboard')['STATIC_FILES_DIR'])

    @classmethod
    def template_files_dir(cls) -> str:
        return os.path.join(os.getcwd(), cls.get_value('dashboard')['TEMPLATE_FILES_DIR'])

    @classmethod
    def run_gunicorn(cls, host, port):
        from racket.managers.gu import run
        run()

import os
import subprocess


class ShellCommandException(Exception):
    pass


def exec_cmd(cmd, throw_on_error=True, cwd=None, cmd_stdin=None,
             **kwargs):
    """
    Runs a command as a child process.
    A convenience wrapper for running a command from a Python script.
    Keyword arguments:
    cmd -- the command to run, as a list of strings
    throw_on_error -- if true, raises an Exception if the exit code of the program is nonzero
    env -- additional environment variables to be defined when running the child process
    cwd -- working directory for child process
    stream_output -- if true, does not capture standard output and error; if false, captures these
      streams and returns them
    cmd_stdin -- if specified, passes the specified string as stdin to the child process.
    Note on the return value: If stream_output is true, then only the exit code is returned. If
    stream_output is false, then a tuple of the exit code, standard output and standard error is
    returned.
    """
    print("EXECUTING")
    cmd_env = os.environ.copy()
    child = subprocess.Popen(cmd, env=cmd_env, cwd=cwd, universal_newlines=True,
                             stdin=subprocess.PIPE, **kwargs)
    exit_code = child.wait()
    if throw_on_error and exit_code is not 0:
        raise ShellCommandException("Non-zero exitcode: %s" % (exit_code))
    return exit_code

from typing import Any

from flask_sqlalchemy.model import DefaultMeta
from racket.managers.server import ServerManager
from racket.models import db


def get_or_create(table: DefaultMeta, column: str, column_id: str, value: Any) -> tuple:
    app = ServerManager.create_app('dev', False)
    with app.app_context():
        instance = db.session.query(getattr(table, column_id)).filter(getattr(table, column) == value).first()
        if instance:
            return instance
        else:
            instance = table(**{column: value})
            db.session.add(instance)
            return get_or_create(table, column, column_id, value)

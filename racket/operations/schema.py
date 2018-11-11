from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound

from racket.managers.server import ServerManager
from racket.models import db
from racket.models.base import MLModelInputs, MLModel


def deactivate() -> None:
    app = ServerManager.create_app('dev', False)
    with app.app_context():
        try:
            active = db.session.query(MLModel).filter(MLModel.active == True).one()  # NOQA
        except NoResultFound:
            return
        print(active)
        active.active = False
        db.session.commit()


def activate() -> None:
    app = ServerManager.create_app('dev', False)
    with app.app_context():
        active = db.session.query(MLModel).order_by(desc(MLModel.version_dir)).first()
        active.active = True
        db.session.commit()


def active_model() -> str:
    """
    Query the model id of the currently active model
    Returns
    -------
    str
        Unique model identifier
    """

    app = ServerManager.create_app('dev', False)
    with app.app_context():
        active = db.session.query(MLModel.active == True).one()  # NOQA
    return active[0].model_id


def determine_current_schema() -> dict:
    """
    Get the input specification of the currently active model
    Returns
    -------
    dict: dictionary of the specs
    """
    app = ServerManager.create_app('dev', False)
    model = active_model()
    with app.app_context():
        schema = db.session.query(MLModelInputs).filter(MLModelInputs.model_id == model).one()
    return schema.as_dict()

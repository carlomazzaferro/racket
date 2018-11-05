from racket.models import db
from racket.models.base import ActiveModel, MLModelInputs
from racket.operations.utils import unfold


def active_model():
    active = db.session.query(ActiveModel).all()
    return active[0].model_id


def determine_current_schema():
    model = active_model()
    schema = db.session.query(MLModelInputs).filter(MLModelInputs.model_id == model).one()
    return schema.as_dict()

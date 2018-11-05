import datetime

from sqlalchemy.schema import ForeignKey
from racket.models import SerialializableModel, db


class MLModel(db.Model, SerialializableModel):
    __tablename__ = 'MLModel'
    model_id = db.Column(db.Integer, index=True, primary_key=True)
    model_name = db.Column(db.Text)
    major = db.Column(db.Integer)
    minor = db.Column(db.Integer)
    patch = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    type_id = db.Column(db.Integer, ForeignKey("MLModelType.type_id"))


class MLModelType(db.Model, SerialializableModel):
    __tablename__ = 'MLModelType'
    type_id = db.Column(db.Integer, index=True, primary_key=True)
    type_name = db.Column(db.String)


class MLModelInputs(db.Model, SerialializableModel):
    __tablename__ = 'MLModelInputs'
    model_id = db.Column(db.Integer, ForeignKey('MLModel.model_id'), primary_key=True, index=True)
    model_inputs = db.Column(db.JSON)


class ActiveModel(db.Model):
    __tablename__ = 'ActiveModel'
    id = db.Column(db.Integer, index=True, primary_key=True)
    model_id = db.Column(db.Integer, ForeignKey('MLModel.model_id'))




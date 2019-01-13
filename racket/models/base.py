import datetime

from sqlalchemy.schema import ForeignKey

from racket.models import SerialializableModel, db


class ActiveModel(db.Model, SerialializableModel):
    """
    Specifies the currently active model
    """
    __tablename__ = 'ActiveModel'
    model_id = db.Column(db.Integer, index=True, primary_key=True)


class MLModel(db.Model, SerialializableModel):
    """
    The SQL DeclarativeMeta model responsible for storing a model's metadata

    Parameters
    ----------
    model_id: int
        The model's unique identifier
    model_name: str
        Model name, usually defined with instantiating a Learner class
    major : int
        Major version of the learner
    minor: int
        Minor version of the learner
    patch: int
        Patch version of the learner
    version_dir: str
        Directory where the models will be stored inside TensorFlow serving and on-disk
    created_at: dateteime.datetime
        When the model was created
    model_type: str
        The model type usually either regression or classification
    """

    __tablename__ = 'MLModel'
    model_id = db.Column(db.Integer, index=True, primary_key=True)
    model_name = db.Column(db.Text)
    major = db.Column(db.Integer)
    minor = db.Column(db.Integer)
    patch = db.Column(db.Integer)
    version_dir = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    model_type = db.Column(db.String)


class MLModelInputs(db.Model, SerialializableModel):
    __tablename__ = 'MLModelInputs'
    model_id = db.Column(db.Integer, ForeignKey('MLModel.model_id'), primary_key=True, index=True)
    model_inputs = db.Column(db.Text)


class ModelScores(db.Model, SerialializableModel):
    """Scores of the model

    Parameters
    ----------
    model_id: int
        The model's unique identifier
    scoring_fn: str
        The name of the scoring function
    score: float
        The cross-validation score associated with the scoring function and the model id
    """

    __tablename__ = 'ModelScores'
    id = db.Column(db.Integer, primary_key=True, index=True)
    model_id = db.Column(db.Integer, ForeignKey('MLModel.model_id'), primary_key=False, index=True)
    scoring_fn = db.Column(db.Text)
    score = db.Column(db.Float)

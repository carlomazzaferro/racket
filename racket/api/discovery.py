from flask import jsonify
from flask_restplus import Namespace, Resource, fields
from racket.models import db
from racket.models.base import MLModel


discover_ns = Namespace('discover', description='Inference endpoint')
ds = discover_ns.model('discover', {'max': fields.Integer, 'available_only': fields.Boolean})


@discover_ns.route('/active')
class Discover(Resource):
    def get(self):
        from racket.operations.schema import active_model
        active = db.session.query(MLModel).filter(MLModel.model_id == active_model()).one()
        return jsonify(active.as_dict())


@discover_ns.route('/available')
class Discover(Resource):
    def get(self):
        from racket.operations.schema import active_model
        active = db.session.query(MLModel).filter(MLModel.model_id == active_model()).one()
        return jsonify(active.as_dict())







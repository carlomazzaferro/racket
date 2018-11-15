from flask import jsonify
from flask_restplus import Namespace, Resource, fields
from racket.models import db
from racket.models.base import MLModel


discover_ns = Namespace('discover', description='Inference endpoint')
ds = discover_ns.model('discover', {'max': fields.Integer, 'available_only': fields.Boolean})


@discover_ns.route('/active')
class Discover(Resource):
    def get(self):
        from racket.operations.schema import active_model_
        return jsonify(active_model_(name=None))


@discover_ns.route('/available')
class DiscoverAvailable(Resource):
    def get(self):
        from racket.operations.schema import active_model_
        active = db.session.query(MLModel).filter(MLModel.model_id == active_model_()).one()
        return jsonify(active.as_dict())

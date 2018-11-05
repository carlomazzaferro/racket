from flask import jsonify
from flask_restplus import Namespace, Resource, fields
from racket.models import db


infer_ns = Namespace('infer', description='Inference endpoint')
vh = infer_ns.model('infer', {'max': fields.Integer, 'available_only': fields.Boolean})


@infer_ns.route('/')
class Inference(Resource):
    def post(self):
        pass





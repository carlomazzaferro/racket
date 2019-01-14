import numpy
from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields

from racket.operations.infer import ServerTarget
from racket.operations.schema import active_model_name_

infer_ns = Namespace('infer', description='Inference endpoint')
ts = infer_ns.model('infer', {'input': fields.Raw})


@infer_ns.route('/')
class Inference(Resource):

    @infer_ns.expect(ts)
    def post(self):
        req = request.get_json()
        model_name = active_model_name_()
        predictions = ServerTarget.predict(model_name, numpy.array(req['input']))
        return jsonify({'predictions': predictions['result'].tolist()})

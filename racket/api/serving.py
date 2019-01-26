import numpy
from flask import request, jsonify
from flask_restplus import Namespace, Resource

from racket.operations.infer import ServerTarget
from racket.operations.schema import active_model_name_

serve_ns = Namespace('serve', description='Inference endpoint')

id_parser = serve_ns.parser()
id_parser.add_argument('model_id', type=int, location='args', help='Model ID to be served')

name_ver_parser = serve_ns.parser()
name_ver_parser.add_argument('name', type=str, location='args', help='Model ID to be served')
name_ver_parser.add_argument('version', type=str, location='args',
                             help='Model version, in the format "major.minor.patch"')


@serve_ns.route('/id')
class ServeById(Resource):

    @serve_ns.expect(id_parser)
    def post(self):
        req = request.get_json()
        model_name = active_model_name_()
        predictions = ServerTarget.predict(model_name, numpy.array(req['input']))
        return jsonify({'predictions': predictions['result'].tolist()})


@serve_ns.route('/name_ver')
class ServeById(Resource):

    @serve_ns.expect(name_ver_parser)
    def post(self):
        req = request.get_json()
        model_name = active_model_name_()
        predictions = ServerTarget.predict(model_name, numpy.array(req['input']))
        return jsonify({'predictions': predictions['result'].tolist()})

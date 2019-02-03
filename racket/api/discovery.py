from flask import jsonify
from flask_restplus import Namespace, Resource, fields
from racket.operations.utils import unfold

discover_ns = Namespace('model', description='Inference endpoint')
ds = discover_ns.model('model', {'max': fields.Integer, 'available_only': fields.Boolean})


parser = discover_ns.parser()
parser.add_argument('model_id', type=int, location='args', help='Model ID to be served')
parser.add_argument('name', type=str, location='args', help='Model ID to be served')
parser.add_argument('version', type=str, location='args', help='Model version, in the format "major.minor.patch"')


@discover_ns.route('/active')
class Active(Resource):
    def get(self):
        from racket.operations.schema import active_model_
        return jsonify(active_model_().as_dict())


@discover_ns.route('/all')
class All(Resource):
    @discover_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        from racket.operations.schema import model_filterer_, query_by_id_
        if args['model_id']:
            return jsonify(query_by_id_(args['model_id']).as_dict())
        return jsonify(unfold(model_filterer_(name=args['name'], version=args['version'])))


@discover_ns.route('/scores')
class ScoresId(Resource):
    @discover_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        from racket.operations.schema import query_scores_
        return jsonify(unfold(query_scores_(model_id=args['model_id'], name=args['name'], version=args['version'])))


@discover_ns.route('/historic')
class EpochsLossAcc(Resource):
    @discover_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        from racket.operations.schema import historic_scores_
        return jsonify(historic_scores_(model_id=args['model_id'], name=args['name'], version=args['version']))


@discover_ns.route('/parameters')
class Parameters(Resource):
    @discover_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        from racket.operations.schema import query_params_
        return jsonify(query_params_(model_id=args['model_id'], name=args['name'], version=args['version']))








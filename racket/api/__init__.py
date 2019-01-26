from flask import Blueprint
from flask_restplus import Api

from racket.api.infer import infer_ns
from racket.api.discovery import discover_ns
from racket.api.serving import serve_ns

api_bp = Blueprint('api', __name__)

api = Api(api_bp)
api.add_namespace(infer_ns)
api.add_namespace(discover_ns)
api.add_namespace(serve_ns)

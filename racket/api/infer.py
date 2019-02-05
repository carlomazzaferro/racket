import sys
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
        model_name = active_model_name_()
        if 'data' in request.files:
            if 'cv2' not in sys.modules:
                return 'cv2 is required if input is an image. Please install it with: pip install cv2', 400
            else:
                import cv2
                img = cv2.imdecode(numpy.fromstring(request.files['data'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
                img = img.reshape(1, img.shape[0]**2) / 255.0
                predictions = ServerTarget.predict(model_name, img)
        else:
            req = request.get_json()
            predictions = ServerTarget.predict(model_name, numpy.array(req['input']))
        return jsonify({'predictions': predictions['result'].tolist()})

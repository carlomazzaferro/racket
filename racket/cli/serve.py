import click
import logging

from racket.models import db
from racket.models.base import MLModel

__author__ = "Carlo Mazzaferro"
__copyright__ = "Carlo Mazzaferro"
__license__ = "none"

_logger = logging.getLogger('root')


@click.command()
@click.option('--model-id', default=None, help='Model unique identifier')
@click.option('--model-name', default=None, help='Model name')
@click.option('--version', default='latest', help='Model version as major.minor.patch, or latest')
def serve(model_id, model_name, version):
    """
    docker run -it $USER/tensorflow-serving-devel --name tf_serving
    docker cp stored_models/$1/tf tf_serving:/serving
    docker start tf_serving && docker exec -it tf_serving mv /serving/tf /serving/$1
    docker exec -it tf_serving /serving/bazel-bin/tensorflow_serving/model_servers/tensorflow_model_server \
        --port=9000 --model_base_path=/serving/ &> gan_log &
    Args:
        model_id:
        model_name:
        version:
    Returns:
    """
    version = version.split('.')
    filter_on = ('model_id', model_id) if model_id else ('model_name', model_name)
    servable = db.session.query(MLModel).filter(getattr(MLModel, filter_on[0]) == filter_on[1])
    servable.copy_to_container()
    servable.serve()

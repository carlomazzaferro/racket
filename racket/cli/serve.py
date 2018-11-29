import logging

import click

from racket.operations.load import serve_model


log = logging.getLogger('root')


@click.command()
@click.option('--model-id', default=None, help='Model unique identifier')
@click.option('--model-name', default=None, help='Model name')
@click.option('--version', default='latest', help='Model version as major.minor.patch, or latest')
def serve(model_id, model_name, version):
    """{}""".format(serve_model.__doc__)
    serve_model(model_id, model_name, version)

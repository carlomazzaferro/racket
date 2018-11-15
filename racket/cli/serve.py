import logging

import click

from racket.utils import Printer as p
from racket.managers.learner import LearnerManager
from racket.managers.server import ServerManager
from racket.models.exceptions import CLIError
from racket.operations.load import ModelLoader


log = logging.getLogger('root')


@click.command()
@click.option('--model-id', default=None, help='Model unique identifier')
@click.option('--model-name', default=None, help='Model name')
@click.option('--version', default='latest', help='Model version as major.minor.patch, or latest')
def serve(model_id, model_name, version):
    """Serve a specific model.

    This allows you to specify either a model-id or a the name + version of a specific model that you'd like to serve.
    If the model-id is specified, the name and versions are ignored.

    Throws an error if the specified model do not exist.
    """
    if (version != 'latest' and model_id) or (model_name and model_id):
        raise CLIError('You must specify either a model_id or a model_name + version, or just the model name ('
                       'in which case the default latest version will be used)')

    if not model_name and not model_id:
        raise CLIError('You must specify either a model_id or a model_name + version, or just the model name ('
                       'in which case the default latest version will be used)')

    if version == 'latest' and model_name:
        ModelLoader.load(model_name)

    else:
        app = ServerManager.create_app('prod', False)
        with app.app_context():
            if model_id:
                servable = LearnerManager.query_by_id(model_id)
            else:
                servable = LearnerManager.query_by_name_version(model_name, version)
            if servable.active:
                p.print_warning('Model specified is already active')
                return
            else:
                LearnerManager.load_version_from_existing_servable(servable)
                ModelLoader.load(servable.model_name)

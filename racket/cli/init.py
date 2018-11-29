import logging

import click

from racket.utils import Printer as p
from racket.managers.project import ProjectManager

_logger = logging.getLogger('root')


@click.command()
@click.option('--name', help='Name of the project', default='racket-server')
@click.option('--path', help='Directory where the new project will be created', default='.')
def init(path: str, name: str) -> None:
    """Creates a new project with the necessary scaffolding, as well as the supporting
        files needed. The directory structure of a new project , and the files within it
        will look like this::

            regression.py         # Regression starter file
            classification.py     # Classification starter file
            racket.yaml           # Main project config file
            .gitignore            # Just in case
            Dockerfile            # TFS' Dockerfile
            docker-compose.yaml   # Docker-compose to start up TFS
            serialized/           # Where the serialized models will be stored

        """
    ProjectManager.init_project(path, name)
    p.print_success(f'Successfully initiated project: {name}!')

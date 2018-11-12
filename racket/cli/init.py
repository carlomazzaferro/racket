import logging

import click
from racket.managers.project import ProjectManager

_logger = logging.getLogger('root')


@click.command()
@click.option('--name', help='Name of the project', default='racket-server')
@click.option('--path', help='Directory where the new project will be created', default='.')
def init(path: str, name: str) -> None:
    """ Creates a new project """
    ProjectManager.init_project(path, name)

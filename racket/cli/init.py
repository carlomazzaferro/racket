import os
import sys
import logging

import click
from racket.managers.project import ProjectManager

_logger = logging.getLogger('root')


@click.command()
@click.option('--name', help='Project Name', default='racket-server')
@click.option('--path', help='Path where project will live', default='.')
def init(name: str, path: str) -> None:
    project_path = os.path.join(path, name)
    if os.path.isdir(project_path):
        safe_init(project_path, name)
    else:
        ProjectManager.create_dir(project_path)
        ProjectManager.set_path(project_path)
        ProjectManager.init_project(name)
        ProjectManager.create_db()


def safe_init(project_path: str, name: str) -> None:
    overwrite = input('WARNING: Path specified already exists. Any configuration will be overwritten. Proceed?[Y/n]')
    if overwrite == 'Y':
        ProjectManager.set_path(project_path)
        ProjectManager.init_project(name)
    elif overwrite == 'n':
        sys.exit()
    else:
        safe_init(project_path, name)

# -*- coding: utf-8 -*-

"""Console script for racket."""

import click

from racket.cli.dashboard import dashboard
from racket.cli.init import init
from racket.cli.serve import serve
from racket.cli.version import version, v
from racket.cli.ls import ls
from racket.conf import setup_logging

__author__ = "Carlo Mazzaferro"
__copyright__ = "Carlo Mazzaferro"
__license__ = "GNU General Public License v3"


@click.group()
@click.option('-v', '--verbose', is_flag=True, default=False, help='Turn on debug logging')
@click.pass_context
def cli(context, verbose):
    """ racket CLI tool to:
        * Create new projects
        * Interact with racket server.
        * Manage model lifecycle
    Check the help available for each command listed below.
    """
    setup_logging(verbose)


cli.add_command(init)
cli.add_command(version)
cli.add_command(serve)
cli.add_command(dashboard)
cli.add_command(version)
cli.add_command(v)
cli.add_command(ls)

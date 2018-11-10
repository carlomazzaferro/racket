# -*- coding: utf-8 -*-

"""Console script for racket."""

import click

from racket.conf import setup_logging
from racket.cli.init import init
from racket.cli.serve import serve
from racket.cli.version import version
from racket.cli.dashboard import dashboard


@click.group()
@click.option('-v', '--verbose', is_flag=True, default=False, help='Turn on debug logging')
@click.pass_context
def cli(context, verbose):
    """ Polyaxon CLI tool to:
        * Parse, Validate, and Check Polyaxonfiles.
        * Interact with Polyaxon server.
        * Run and Monitor experiments.
    Check the help available for each command listed below.
    """
    setup_logging(verbose)


cli.add_command(init)
cli.add_command(version)
cli.add_command(serve)
cli.add_command(dashboard)

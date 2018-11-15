import racket
import click
import logging

from racket.utils import Printer as p

log = logging.getLogger('root')


@click.command()
def version():
    """ Retrive the version of the current ``racket`` install"""
    p.print_success('racket version: ' + racket.__version__)


@click.command()
def v():
    """ Retrive the version of the current ``racket`` install"""
    p.print_success('racket version: ' + racket.__version__)

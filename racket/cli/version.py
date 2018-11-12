import racket
import click
import logging


log = logging.getLogger('root')


@click.command()
def version():
    """ Retrive the version of the current ``racket`` install"""
    log.info('racket version: ' + racket.__version__)
    print('racket version: ' + racket.__version__)


@click.command()
def V():
    """ Retrive the version of the current ``racket`` install"""
    log.info('racket version: ' + racket.__version__)
    print('racket version: ' + racket.__version__)

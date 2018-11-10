import racket
import click
import logging


log = logging.getLogger('root')


@click.command()
def version():
    logging.info('Kryptoflow version: ' + racket.__version__)

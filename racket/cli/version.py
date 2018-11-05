import racket
import click
import logging


_logger = logging.getLogger('root')


@click.command()
def version():
    logging.info('Kryptoflow version: ' + racket.__version__)

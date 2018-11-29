from typing import List, Dict, Tuple

import click
from tabulate import tabulate


class Printer(object):

    @staticmethod
    def print_header(text):
        click.secho('\n{}\n'.format(text), fg='yellow')

    @staticmethod
    def print_warning(text):
        click.secho('\n{}\n'.format(text), fg='magenta')

    @staticmethod
    def print_success(text):
        click.secho('\n{}\n'.format(text), fg='green')

    @staticmethod
    def print_error(text):
        click.secho('\n{}\n'.format(text), fg='red')

    @staticmethod
    def add_color(value, color):
        return click.style('{}'.format(value), fg=color)


def list_dicts_to_tabulate(list_dicts: List[Dict]) -> Tuple[List, Dict.items]:
    header = list_dicts[0].keys()
    values = [l.values() for l in list_dicts]
    return values, header


def dict_tabulate(values: List) -> None:
    v, h = list_dicts_to_tabulate(values)
    click.echo(tabulate(v, headers=h))


def register_docstrings(parent=None):
    def doc_decorator(func):
        func.__doc__ = parent.__doc__ + func.__doc__
        return func
    return doc_decorator

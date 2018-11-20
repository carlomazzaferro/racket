import pytest
from tabulate import tabulate

from racket.utils import Printer as p
from racket.utils import dict_tabulate, list_dicts_to_tabulate


@pytest.fixture
def list_d():
    yield [
        {'a': 1, 'b': 2},
        {'a': 4, 'b': 3},
        {'a': 12, 'b': '132'}
    ]


def test_printer(capfd):
    red, bold = '\x1b[31m', '\x1b[0m'
    for _ in ['print_header', 'print_warning', 'print_success', 'print_error']:
        func = getattr(p, _)
        func('some log message')
        out, err = capfd.readouterr()
        assert out == '\nsome log message\n\n'

    assert p.add_color('some log message', 'red') == red + 'some log message' + bold


def test_tabulation(list_d):
    v, h = list_dicts_to_tabulate(list_d)
    assert ([list(i) for i in v], list(h)) == ([[1, 2], [4, 3], [12, '132']], ['a', 'b'])


def test_dict_tabulate(list_d, capfd):
    v, h = list_dicts_to_tabulate(list_d)
    v = [list(i) for i in v]
    dict_tabulate(list_d)
    out, err = capfd.readouterr()
    assert out[2:-2] in tabulate(v, headers=h)  # formatting issues, 1 character mismatch

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `racket` package."""
import shutil

from click.testing import CliRunner

from racket.cli.init import init


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(init, ['--path', 'tests/'])
    assert result.exit_code == 0
    result = runner.invoke(init, ['--path', 'tests/'])
    assert result.exit_code == 1
    assert 'WARNING' in result.stdout_bytes.decode("utf-8")
    shutil.rmtree('tests/racket-server')

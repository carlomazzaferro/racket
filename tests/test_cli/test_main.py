#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `racket` package."""

from click.testing import CliRunner

from racket.main import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--verbose', 'ls'])
    assert result.exit_code == 0
    assert 'model_id' in result.stdout_bytes.decode("utf-8")

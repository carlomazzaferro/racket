#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `racket` package."""

from click.testing import CliRunner

from racket.cli.ls import ls


def test_command_line_interface(init_project):
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(ls)
    print(result.stdout_bytes.decode("utf-8"))
    assert result.exit_code == 0
    assert 'model_id' in result.stdout_bytes.decode("utf-8")

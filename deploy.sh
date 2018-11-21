#!/usr/bin/env bash

python setup.py sdist bdist_wheel
pip install twine
twine uplaod --username Mazzafish --password $PYPI dist/*

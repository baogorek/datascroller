#! /usr/bin/env bash

# make sure to install test library with pip install flake8

flake8 --max-line-length 160 --per-file-ignores='datascroller/__init__.py:F401' --verbose

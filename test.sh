#! /usr/bin/env bash

# make sure to install test dependencies with pip install -r ./test_requirements.txt

flake8 \
--max-line-length 160 \
--exclude __init__.py \
./datascroller

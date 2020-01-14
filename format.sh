#! /usr/bin/env bash

# make sure to install formatter with pip install autopep8

autopep8 --in-place --max-line-length 159 --aggressive --aggressive --recursive .

#!/usr/bin/sh
#
# Create a virtual environment and install the dependencies

python3 -m venv .venv
poetry install

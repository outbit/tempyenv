#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:./src"
coverage run --source=tempyenv -m unittest discover tests/units/

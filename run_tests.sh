#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:./src"
coverage run --source=ansibledocgen -m unittest discover tests/units/

#!/bin/bash

python -m venv django_venv
django_venv/bin/pip install -r requirement.txt
. django_venv/bin/activate
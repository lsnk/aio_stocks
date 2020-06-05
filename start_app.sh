#!/bin/bash

set -o errexit
set -o xtrace

export PYTHONPATH=$PYTHONPATH:src

python src/db.py
uvicorn api.app:app

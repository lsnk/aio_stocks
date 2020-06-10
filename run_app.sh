#!/bin/bash

set -o errexit

export PYTHONPATH=$PYTHONPATH:src

python src/db.py

uvicorn api.app:app &
python src/parsers/run.py &

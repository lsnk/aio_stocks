#!/bin/bash

set -o errexit

export PYTHONPATH=$PYTHONPATH:src

python src/db.py

gunicorn api.app:app -c src/gunicorn_conf.py &
python src/parsers/run.py &
wait

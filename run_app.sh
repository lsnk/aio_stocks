#!/bin/bash

set -o errexit

export PYTHONPATH=$PYTHONPATH:python/src

python python/src/db.py

gunicorn api.app:app -c python/src/gunicorn_conf.py &
python python/src/parsers/run.py &
wait

#!/bin/sh

set -o errexit
set -o nounset


python db.py
gunicorn api.app:app -c gunicorn_conf.py

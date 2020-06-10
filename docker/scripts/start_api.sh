#!/bin/sh

set -o errexit
set -o nounset


python db.py
uvicorn --host 0.0.0.0 api.app:app

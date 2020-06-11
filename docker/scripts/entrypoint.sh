#!/bin/sh

set -o errexit
set -o nounset


postgres_ready() {
python << END
import os
import sys

import psycopg2

try:
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        dbname=os.environ['DB_NAME'],
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres ${DB_HOST}:${DB_PORT}/${DB_NAME} is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."


exec "$@"

#!/bin/sh
set -e

echo "Running migrations..."
alembic upgrade head
echo "Migrations finished their execution..."

echo "Starting Gunicorn..."
exec gunicorn run:app --bind 0.0.0.0:10000
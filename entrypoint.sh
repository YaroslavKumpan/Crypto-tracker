#!/bin/sh
set -e
echo "Running migrations..."
alembic upgrade head

echo "Starting Celery worker & beat..."
celery -A app.tasks.price_tasks worker --beat --loglevel=info &

echo "Starting Uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
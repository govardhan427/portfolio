#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- 1. Collecting static files ---"
python manage.py collectstatic --noinput

echo "--- 2. Running database migrations ---"
python manage.py migrate

echo "--- 3. Loading initial data fixture ---"
python manage.py loaddata initial_data.json

echo "--- Build process complete ---"
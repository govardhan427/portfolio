#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- 0. Installing Python dependencies ---"
pip install -r requirements.txt

echo "--- 1. Collecting static files ---"
python manage.py collectstatic --noinput

echo "--- 2. Running database migrations ---"
python manage.py migrate

# echo "--- 3. Loading initial data fixture ---"
# python manage.py loaddata initial_data.json

echo "--- 4. Creating non-interactive superuser ---"
python manage.py shell -c "import os; from django.contrib.auth import get_user_model; User = get_user_model(); username=os.environ.get('DJANGO_SUPERUSER_USERNAME'); password=os.environ.get('DJANGO_SUPERUSER_PASSWORD'); email='admin@example.com'; User.objects.filter(username=username).exists() or User.objects.create_superuser(username, email, password)"

echo "--- Build process complete ---"
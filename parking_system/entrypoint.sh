#!/bin/sh

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Execute the command passed as arguments to the script
exec "$@"

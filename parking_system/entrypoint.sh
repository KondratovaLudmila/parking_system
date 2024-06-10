#!/bin/sh

# Check if the database is set to use PostgreSQL
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    # Loop until PostgreSQL is ready to accept connections
    while ! nc -z $POSTGRES_HOST 5432; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Apply database migrations
python manage.py migrate

# Create initial superuser
python manage.py shell <<EOF
import os
import django
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking_system.settings')
django.setup()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='password',
        first_name='Admin',
        last_name='User'
    )
EOF

# Execute the command passed as arguments to the script
exec "$@"

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

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Execute the command passed as arguments to the script
exec "$@"

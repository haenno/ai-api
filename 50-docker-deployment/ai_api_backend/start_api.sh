#!/bin/bash

echo 'Django startup...'
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate # Apply database migrations
pipenv run python manage.py collectstatic --noinput  # Collect static files
pipenv run python -m chatbot -t  # train AI model

# fixtures (superuser)
# pipenv run python manage.py loaddata apiproject/fixtures/users.json

echo 'Starting Django in production mode:'
exec pipenv run daphne -b 0.0.0.0 -p 8000 aiapiproject.asgi:application

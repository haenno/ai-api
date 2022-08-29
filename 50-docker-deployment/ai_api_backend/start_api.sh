#!/bin/bash

echo 'Django startup... '
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate --run-syncdb  # Apply database migrations
pipenv run python manage.py collectstatic --noinput  # Collect static files
pipenv run python -m chatbot -t  # train AI model

echo 'Starting Django in production mode (Daphne)... '
exec pipenv run daphne -b 0.0.0.0 -p 8000 aiapiproject.asgi:application

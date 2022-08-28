# docker-deployment

Dockerized Django backend and a nginx frontend to start with docker-compse.

## Useage

1. Install and start docker.
2. Build the containers with ``docker-compose build`` from this folder.
3. Start the containers with ``docker-compose up``.
4. Open the frontend (Vue.js with Axios) here <http://localhost:8080> or the backend (Django REST API to a AI application) here <http://localhost:8000>.
5. Optional: Create a superuser to access the Django admin interface and/or run the AI model training via the API with ``docker-compose exec ai_api_backend pipenv run python manage.py createsuperuser``.

## Sources

- Docker-compose part from <https://github.com/bbachi/vuejs-nodejs-docker-compose> over <https://medium.com/bb-tutorials-and-thoughts/vue-js-local-development-with-docker-compose-275304534f7c>
- Deploy Vue.js App via Nginx <https://v2.vuejs.org/v2/cookbook/dockerize-vuejs-app.html>

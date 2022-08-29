# docker-deployment

Dockerized Django backend and a nginx frontend to start with docker-compse. Live demo here <https://ai-api.tstsrv.de>, documentation there <https://github.com/haenno/ai-api>.

## Useage

1. Install and start docker.
2. Build the containers with ``docker-compose build`` from this folder.
3. Start the containers with ``docker-compose up``.
4. Open the frontend (Vue.js with Axios) here <http://localhost:8080> or the backend (Django REST API to a AI application) here <http://localhost:8000>.
5. Optional: Create a superuser to access the Django admin interface and/or run the AI model training via the API with ``docker-compose exec ai_api_backend pipenv run python manage.py createsuperuser``.

## Inspiration and credit

For docker-compose hintes to <https://medium.com/bb-tutorials-and-thoughts/vue-js-local-development-with-docker-compose-275304534f7c> and details for Vue.js deployment to <https://v2.vuejs.org/v2/cookbook/dockerize-vuejs-app.html>.

## License

MIT License: Copyright (c) 2022 Henning 'haenno' Beier, haenno@web.de, <https://github.com/haenno/ai-api>

# docker-deployment

Dockerized Django backend and a nginx frontend to start with docker-compse. Live demo here <https://ai-api.tstsrv.de>, documentation there <https://github.com/haenno/ai-api>.

## Useage

1. Install and start docker.
2. Build the containers with ``docker-compose build`` from this folder.
3. Start the containers with ``docker-compose up``.
4. Open the frontend (Vue.js with Axios) here <http://localhost:8080> or the backend (Django REST API to a AI application) here <http://localhost:8000>.
5. Optional: Create a superuser to access the Django admin interface and/or run the AI model training via the API with ``docker-compose exec ai_api_backend pipenv run python manage.py createsuperuser``.

## Inspiration and credit

For docker-compose hints to <https://medium.com/bb-tutorials-and-thoughts/vue-js-local-development-with-docker-compose-275304534f7c> and details for Vue.js deployment to <https://v2.vuejs.org/v2/cookbook/dockerize-vuejs-app.html>.

## Errata: Known errors / hickups

Sometimes the backend container will not start, presenting a error message like "bash not found" or "no permissions". In that case try making the ``start_api.sh``-file in the ``ai_api_backend``-folder executable with ``chmod +x start_api.sh``. 
Also check the encoding of this file: It should be UNIX like and not Windows like. That means that the line endings should be **LF** and not **CRLF**. The tool *Notepad++* can help with that.

## License

MIT License: Copyright (c) 2022 Henning 'haenno' Beier, haenno@web.de, <https://github.com/haenno/ai-api>

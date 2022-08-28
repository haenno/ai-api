# same base container as the frontend to save traffic and space 
FROM node:18-bullseye
WORKDIR /usr/src/ai_api_backend
COPY . .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install pipenv -y
RUN pipenv install --skip-lock
RUN chmod +x start_api.sh
CMD ["sh", "start_api.sh"]

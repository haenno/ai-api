# same base container as the frontend to save traffic and space 
FROM node:18-bullseye
WORKDIR /usr/src/ai_api_backend
COPY . .
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install pipenv -y
RUN pipenv install
RUN chmod +x start_api.sh
CMD ["sh", "start_api.sh"]

# build stage
FROM node:18-bullseye as build-stage
WORKDIR /usr/src/app/ai_api_frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /usr/src/app/ai_api_frontend/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
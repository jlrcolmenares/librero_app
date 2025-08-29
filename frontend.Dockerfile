FROM nginx:alpine

WORKDIR /usr/share/nginx/html

COPY web/static/* ./

EXPOSE 80

FROM nginx:alpine

WORKDIR /usr/share/nginx/html

COPY frontend/static/* ./
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

FROM nginx:alpine

WORKDIR /usr/share/nginx/html

COPY web/static/* ./
COPY web/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

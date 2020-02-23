FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/nginx/nginx.conf /etc/nginx/conf.d

# letsencrypt removed for now
COPY ./compose/nginx/fullchain.pem /etc/nginx/fullchain.pem
COPY ./compose/nginx/privkey.pem /etc/nginx/privkey.pem

COPY ./compose/nginx/fullchain.pem /fullchain.pem
COPY ./compose/nginx/privkey.pem /privkey.pem

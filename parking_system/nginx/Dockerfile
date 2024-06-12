FROM nginx:latest

RUN apt-get update && apt-get install -y openssl && \
    mkdir -p /etc/nginx/certs && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/certs/selfsigned.key -out /etc/nginx/certs/selfsigned.crt -subj "/C=US/ST=State/L=City/O=Organization/OU=Department/CN=5spm.space"

COPY nginx.conf /etc/nginx/nginx.conf

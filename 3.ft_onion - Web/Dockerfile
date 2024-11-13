FROM debian:bullseye

RUN apt update && apt install -y nginx && apt install -y openssh-server && apt install -y tor
RUN mkdir -p /var/run/nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY index.html /var/www/html/index.html
COPY sshd_config /etc/ssh/sshd_config
COPY torrc /etc/tor/torrc
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80
EXPOSE 4242

CMD ["/start.sh"]
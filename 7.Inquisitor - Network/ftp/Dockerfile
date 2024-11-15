FROM debian:bullseye

RUN apt update && apt install -y vsftpd net-tools watch

RUN mkdir -p /var/run/vsftpd/empty

COPY vsftpd.conf /etc/vsftpd.conf

RUN useradd -m zeph && echo "zeph:zeph" | chpasswd

CMD ["/usr/sbin/vsftpd", "/etc/vsftpd.conf"]
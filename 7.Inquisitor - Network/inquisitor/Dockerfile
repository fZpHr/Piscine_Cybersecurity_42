FROM debian:bullseye

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    net-tools \
    libpcap-dev
    

RUN pip3 install scapy


CMD ["tail", "-f", "/dev/null"]
#!/bin/bash

echo 'root:root' | chpasswd

service ssh start
service tor start
sed -i "/<\/body>/i <a href=\"http://$(cat /var/lib/tor/ft_onion/hostname | awk '{print $1}')\">http://$(cat /var/lib/tor/ft_onion/hostname | awk '{print $1}')</a>" /var/www/html/index.html
nginx -g 'daemon off;'



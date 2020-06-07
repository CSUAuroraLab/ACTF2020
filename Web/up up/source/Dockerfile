FROM ubuntu:14.04

LABEL Author="fenghlz" Blog="https://www.fenghlz.xyz"

RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list
RUN sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list\
    && apt-get update \
    && apt-get install -y python curl apache2 \
    && apt-get install -y php5 libapache2-mod-php5 \
    && rm /var/www/html/index.html

COPY src /var/www/html

RUN mv /var/www/html/flag.sh / && \
    chmod +x /flag.sh && \
    rm -rf /home/www-data

ENTRYPOINT /flag.sh
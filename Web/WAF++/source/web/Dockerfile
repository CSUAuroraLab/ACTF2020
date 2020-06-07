FROM ubuntu:16.04

RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN sed -i 's/security.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN \
    DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install --allow-unauthenticated -y \
        build-essential \
	tcpdump \
	ssh \
        apt-utils \
        ssl-cert \
        apache2 \
        apache2-utils \
        apache2-dev \
        libapache2-mod-perl2 \
        libapache2-mod-perl2-dev \
        libcgi-pm-perl \
        liblocal-lib-perl \
        cpanminus \
        libexpat1-dev \
        libssl-dev \
        libapreq2-dev \
        zip && \
    a2enmod cgid && \
    a2enmod rewrite && \
    a2dissite 000-default && \
    apt-get update  --allow-unauthenticated  -y && \
    apt-get upgrade  --allow-unauthenticated  -y && \
    apt-get --allow-unauthenticated  -y clean


COPY localhost.conf /etc/apache2/sites-enabled/localhost.conf
COPY diag.cgi /usr/lib/cgi-bin/diag.cgi
COPY DSSafe.pm /usr/lib/cgi-bin/DSSafe.pm
COPY ./www/index.html  /var/www/html/index.html


COPY FLAG_is_here /FLAG_is_here

RUN \
	chmod 755 /usr/lib/cgi-bin/diag.cgi /usr/lib/cgi-bin/DSSafe.pm && \
	mkdir /usr/lib/cgi-bin/tmp && \
	chmod 733 /usr/lib/cgi-bin/tmp	


CMD [ "sh","-c","service apache2 restart;while true;do echo hello docker;sleep 1;done"]



 

FROM php:7.1-apache

COPY ./html /var/www/html
COPY ./run.sh /var/www/run.sh
RUN chmod +x /var/www/run.sh

EXPOSE 80

ENTRYPOINT /var/www/run.sh && docker-php-entrypoint apache2-foreground
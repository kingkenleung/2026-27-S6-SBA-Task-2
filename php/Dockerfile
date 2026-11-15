FROM php:8.2-fpm-alpine

# The official PHP 8.2 image already ships pdo_sqlite; fail early if that changes.
RUN php -r 'exit(extension_loaded("pdo_sqlite") ? 0 : 1);' \
 && apk add --no-cache sqlite

WORKDIR /var/www/html

# Build the pristine SQLite seed once, outside the web root.
COPY db/seed.sql /tmp/seed.sql
RUN mkdir -p /seed \
 && sqlite3 /seed/app.db < /tmp/seed.sql \
 && chmod 644 /seed/app.db \
 && rm -f /tmp/seed.sql

COPY php/entrypoint.sh php/restore.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh /usr/local/bin/restore.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["php-fpm"]

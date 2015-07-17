FROM postgres

ENV POSTGRES_USER=moses_user POSTGRES_PASSWORD=Moses765
COPY *.sh /docker-entrypoint-initdb.d/
VOLUME /var/lib/pgsql/data

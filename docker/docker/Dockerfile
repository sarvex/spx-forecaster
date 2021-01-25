FROM postgres:12.0-alpine

COPY init.sql /docker-entrypoint-initdb.d/

USER postgres

RUN chmod 0700 /var/lib/postgresql_/data &&\
    initdb /var/lib/postgresql_/data &&\
    echo "host all  all    172.17.0.0/16  md5" >> /var/lib/postgresql/data/pg_hba.conf &&\
    echo "listen_addresses='*'" >> /var/lib/postgresql/data/postgresql.conf
    
EXPOSE 5432
FROM mariadb:latest

# 1. Copy the SQL schema file into the automatic initialization directory
COPY DbSchema/KatalogMariaDB.sql /docker-entrypoint-initdb.d/01_schema.sql

# 2. Fix the config validation issue by baking the my.cnf optimizations right into the image
RUN echo "[mysqld]" > /etc/mysql/conf.d/optimize.cnf && \
    echo "innodb_buffer_pool_size = 1G" >> /etc/mysql/conf.d/optimize.cnf && \
    echo "innodb_buffer_pool_instances = 1" >> /etc/mysql/conf.d/optimize.cnf && \
    echo "innodb_io_capacity = 200" >> /etc/mysql/conf.d/optimize.cnf && \
    echo "innodb_io_capacity_max = 400" >> /etc/mysql/conf.d/optimize.cnf && \
    echo "innodb_read_io_threads = 8" >> /etc/mysql/conf.d/optimize.cnf && \
    echo "innodb_write_io_threads = 8" >> /etc/mysql/conf.d/optimize.cnf

# Ensure permissions are correct
USER root
RUN chmod 644 /docker-entrypoint-initdb.d/01_schema.sql /etc/mysql/conf.d/optimize.cnf
USER mysql

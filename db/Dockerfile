FROM mariadb:latest

# Copy the SQL schema file into the automatic initialization directory
COPY DbSchema/KatalogMariaDB.sql /docker-entrypoint-initdb.d/01_schema.sql

# Optional: Ensure the file has the correct permissions
USER root
RUN chmod 644 /docker-entrypoint-initdb.d/01_schema.sql
USER mysql

#>> Use a base image with MySQL
FROM mysql:8.3.0


#>> Copiar el script SQL a la carpeta docker-entrypoint-initdb.d
COPY init.sql /docker-entrypoint-initdb.d/init.sql
RUN chmod +rx /docker-entrypoint-initdb.d/init.sql


#>> Expose the port MySQL runs on
#EXPOSE 3306
#!/usr/bin/env bash

DOCKERHUB_NAME=arturim13

# 1. Front
docker build -t ${DOCKERHUB_NAME}/katalog-front:latest ./front
docker push ${DOCKERHUB_NAME}/katalog-front:latest

# 2. Connector
docker build -t ${DOCKERHUB_NAME}/katalog-connector:latest ./connector
docker push ${DOCKERHUB_NAME}/katalog-connector:latest

# 3. Nginx
docker build -t ${DOCKERHUB_NAME}/katalog-nginx:latest ./nginx
docker push ${DOCKERHUB_NAME}/katalog-nginx:latest

# 4. mariadb
docker build -t ${DOCKERHUB_NAME}/katalog-db:latest ./db
docker push ${DOCKERHUB_NAME}/katalog-db:latest

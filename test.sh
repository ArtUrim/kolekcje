#/usr/bin/env bash

FNAME=compose_test.yml

docker compose -f ${FNAME} up -d && \
docker compose logs -f front connector

docker compose -f ${FNAME} down

#/usr/bin/env bash

FNAME=compose_test.yml

docker compose -f "${FNAME}" up -d && \
docker compose -f "${FNAME}" logs connector front -f
docker compose -f "${FNAME}" down

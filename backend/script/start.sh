#!/bin/bash

docker run \
    --name $DB_CONTAINER_NAME \
    -e POSTGRES_PASSWORD=$DATABASE_PASSWORD \
    -e POSTGRES_USER=$DATABASE_USER \
    -e POSTGRES_DB=$DATABASE_NAME \
    -v $DATABASE_STORAGE_PATH:/var/lib/postgresql/data \
    -p 5432:5432 \
    -d \
    postgres:15.4

until [ -n "$(docker exec $DB_CONTAINER_NAME pg_isready | grep accepting)" ]; do
    echo "Waiting for DB to come alive..."
    sleep 0.1;
done;

docker run \
    --detach \
    --publish 8000:8000 \
    --name $APP_CONTAINER_NAME \
    --env-file ../backend.env \
    rotini:dev

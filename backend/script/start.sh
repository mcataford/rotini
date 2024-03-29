#!/bin/bash

$CONTAINER_MANAGER network create rotini-local || echo "Network already exists"

$CONTAINER_MANAGER run \
    --name $DB_CONTAINER_NAME \
    -e POSTGRES_PASSWORD=$DB_PASSWORD \
    -e POSTGRES_USER=$DB_USER \
    -e POSTGRES_DB=$DB_NAME \
    -v $DATABASE_STORAGE_PATH:/var/lib/postgresql/data:Z \
    -p 5432:5432 \
    --network rotini-local \
    -d \
    postgres:15

until [ -n "$($CONTAINER_MANAGER exec $DB_CONTAINER_NAME pg_isready | grep accepting)" ]; do
    echo "Waiting for DB to come alive..."
    sleep 0.1;
done;

$CONTAINER_MANAGER run \
    --detach \
    --publish 8000:8000 \
    --name $APP_CONTAINER_NAME \
    --env-file ../backend.env \
    --network rotini-local \
    -v ./rotini:/app/rotini \
    rotini:dev

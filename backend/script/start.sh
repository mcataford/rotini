#!/bin/bash

docker run \
    --detach \
    --publish 8000:8000 \
    --name $APP_CONTAINER_NAME \
    --env-file ../backend.env \
    rotini:dev

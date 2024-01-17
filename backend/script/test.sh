#!/bin/bash

# Test runner script
#
# This sets up an ephemeral database for test purposes, runs migrations on it
# and triggers pytest. Regardless of outcome, the database container is cleaned
# up after the fact.
#
# This will return 0 or 1 as exit code, depending on outcome.

TEST_DB_CONTAINER="rotini-test-ephemeral-$(date +%s)"

VENV_PYTHON=.venv/bin/python
VENV_PYTEST=.venv/bin/pytest

HEALTHCHECK_SLEEP=0.5

# Log & exit.
function fail {
    echo $1
    exit 1
}

# Cleanup before exit (success/failure)
function cleanup {
    $CONTAINER_MANAGER rm $TEST_DB_CONTAINER -f > /dev/null || echo "Failed to clean up test database container."
}

trap cleanup EXIT

$CONTAINER_MANAGER run \
    --name $TEST_DB_CONTAINER \
    -e POSTGRES_PASSWORD=test \
    -p 5431:5432 \
    -d \
    postgres:15.4

until [ -n "$($CONTAINER_MANAGER exec $TEST_DB_CONTAINER pg_isready | grep accepting)" ]; do
    echo "Waiting for DB to come alive..."
    sleep $HEALTHCHECK_SLEEP
done;

sleep $HEALTHCHECK_SLEEP

$VENV_PYTEST . -vv -s $@ || fail "Test run failed."

cleanup

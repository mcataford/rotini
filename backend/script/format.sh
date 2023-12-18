#!/bin/bash

if [ "$FIX" != "1" ]; then
    $VENV_BIN/black . --check
    $VENV_BIN/pylint ./rotini
    return
fi

$VENV_BIN/black .
$VENV_BIN/pylint ./rotini

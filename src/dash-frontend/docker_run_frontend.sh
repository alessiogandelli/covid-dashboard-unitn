#!/bin/bash

set -x

echo "Frontend Run Script start"

sleep 120

python3 -u /app/app/app.py docker

echo "Frontend Run Script end"
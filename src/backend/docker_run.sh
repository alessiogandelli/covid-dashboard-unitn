#!/bin/bash

set -x

echo "Backend Run Script start"

sleep 60

python3 -u /app/ingestion/consumer.py /app/kafka_conf.ini &
python3 -u /app/ingestion/producer.py /app/kafka_conf.ini &
python3 -u /app/computation/compute_models.py

echo "Backend Run Script end"
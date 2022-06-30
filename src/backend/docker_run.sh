#!/bin/bash

set -x

echo "Docker run"

python3 -u /app/ingestion/consumer.py /app/kafka_conf.ini 
python3 -u /app/ingestion/producer.py /app/kafka_conf.ini
python3 -u /app/computation/compute_models.py

echo "docker finished"
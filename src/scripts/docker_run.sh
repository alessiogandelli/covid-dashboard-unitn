#!/bin/bash

rm covid.sqlite
rm covid.sqlite-journal


python3 src/backend/ingestion/consumer.py kafka_conf.ini & 
python3 src/backend/ingestion/producer.py kafka_conf.ini &
python3 src/backend/computation/compute_models.py &
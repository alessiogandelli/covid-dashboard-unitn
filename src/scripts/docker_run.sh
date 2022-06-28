#!/bin/bash

python3 src/backend/ingestion/consumer.py & 
python3 src/backend/ingestion/producer.py 
#!/bin/bash

python3 src/ingestion/consumer.py & 
python3 src/ingestion/producer.py 
#!/bin/bash

############### create environment ###############

#rm -rf venv
#PATH=$PATH:/Users/alessiogandelli/Library/Python/3.8/bin
#virtualenv venv 
./venv/bin/pip3 install -r requirements.txt


python3 src/ingestion/database.py  &
python3 src/ingestion/start.py 
#%%
import sys
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer, OFFSET_BEGINNING
import pandas as pd
import sqlite3
import utils
import constants as c
import logging
import psycopg2
import os

logging.basicConfig(filename='flow.log', level=logging.DEBUG)



config = utils.get_kafka_config(consumer=True)


#%%
 
# Create Consumer instance
consumer = Consumer(config)
consumer.subscribe([c.topic])

db = utils.Database('covid')
db.clean_db()


utils.listen(consumer, db)

# %%

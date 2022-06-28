import sys
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer, OFFSET_BEGINNING
import pandas as pd
import sqlite3
import utils
import constants as c
import logging
logging.basicConfig(filename='flow.log', level=logging.DEBUG)



(# # Parse the command line.
# parser = ArgumentParser()
# parser.add_argument('config_file', type=FileType('r'))
# parser.add_argument('--reset', action='store_true')
# args = parser.parse_args()

# # Parse the configuration.
# # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
# config_parser = ConfigParser()
# config_parser.read_file(args.config_file)
# config = dict(config_parser['default'])
# config.update(config_parser['consumer'])
)


# Create Consumer instance
consumer = Consumer(c.config_consumer)
consumer.subscribe([c.topic])

db = utils.Database('covid.sqlite')


utils.listen(consumer, db)

#%%
from confluent_kafka import Consumer, OFFSET_BEGINNING
import utils
import constants as c
import logging

print("consumer.py")

logging.basicConfig(filename='flow.log', level=logging.DEBUG)



config = utils.get_kafka_config(consumer=True)


#%%
 
# Create Consumer instance
consumer = Consumer(config)
consumer.subscribe([c.topic])

db = utils.Database('covid')
db.clean_db()

print("Consumer: Listen to DB")

utils.listen(consumer, db)

# %%

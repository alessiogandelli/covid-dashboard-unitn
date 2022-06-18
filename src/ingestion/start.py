#%%
import sqlite3
import pandas as pd
import paho.mqtt.client as mqtt 
import numpy as np
import utils
import constants as c
import time
import schedule
import logging
logging.basicConfig(filename='flow.log', encoding='utf-8', level=logging.INFO)

# set up mqtt client
broker_address="broker.hivemq.com"
client = mqtt.Client("carlos")      #create new instance
client.connect(broker_address) 

# compute tables and datatypes to store in the database: stats, regions, age
df_region_age = utils.get_df_region_age(c.url_region, c.col_region)

df_stats, data_types_stats = utils.get_df_stats(c.url_tot, c.drop_stats, c.col_stats)
df_age, data_types_age = utils.get_df_age(df_region_age, c.drop_age)
df_region, data_types_region = utils.get_df_region(df_region_age, c.group_by_region)

logging.info('dataframe created')



# for each table create a dictionary with the columns name and the datatypes 
stats_col = {'table':'cases', 'cols': list(df_stats), 'dtype': data_types_stats}
regions_col = {'table':'regions', 'cols': list(df_region), 'dtype': data_types_region}
age_col = {'table':'age', 'cols': list(df_age), 'dtype': data_types_age}

# send tables to the broker
utils.send_table(client, df_age, age_col, "covid_italy_age")                  # age table
utils.send_table(client, df_region, regions_col, "covid_italy_region")        # region table
utils.send_table(client, df_stats, stats_col, "covid_italy")                  # stats table


schedule.every().minute.do(utils.update_stats,client )



while True:
    schedule.run_pending()
    time.sleep(1)
# %%

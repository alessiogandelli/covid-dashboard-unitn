# %%
# from argparse import ArgumentParser, FileType
# from configparser import ConfigParser
from confluent_kafka import Producer
import utils
import constants as c
import time
import schedule
import logging
logging.basicConfig(filename='flow.log', encoding='utf-8', level=logging.INFO)


# %%
# Parse the command line.
#parser = ArgumentParser()
#parser.add_argument('config_file', type=FileType('r'))
#args = parser.parse_args()

# Parse the configuration.
# See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
#config_parser = ConfigParser()
# config_parser.read_file(args.config_file)
#config = dict(config_parser['default'])

# Create Producer instance
producer = Producer(c.config_producer)
logging.info('kafka producer created')


# %%
# compute tables and datatypes to store in the database: stats, regions, age
df_region_age = utils.get_df_region_age(c.url_region, c.col_region)

df_stats,  data_types_stats  = utils.get_df_stats(c.url_tot, c.drop_stats, c.col_stats)
df_age,    data_types_age    = utils.get_df_age(df_region_age, c.drop_age)
df_region, data_types_region = utils.get_df_region(df_region_age, c.group_by_region)

logging.info('dataframe created')



# for each table create a dictionary with the columns name and the datatypes 
stats_col = {'table':'stats', 'cols': list(df_stats), 'dtype': data_types_stats}
regions_col = {'table':'regions', 'cols': list(df_region), 'dtype': data_types_region}
age_col = {'table':'age', 'cols': list(df_age), 'dtype': data_types_age}




# %%
utils.send_table(df_region,c.topic, producer, regions_col)
utils.send_table(df_stats, c.topic, producer, stats_col)
utils.send_table(df_age, c.topic, producer, age_col)




schedule.every().day.do(utils.update_stats, producer )


while True:
    schedule.run_pending()
    time.sleep(1)
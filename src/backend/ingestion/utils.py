import sqlite3
import constants as c
import pandas as pd
import logging
import numpy as np
from confluent_kafka import Producer


logging.basicConfig(filename='flow.log', level=logging.DEBUG, format='%(asctime)s:%(process)d:%(levelname)s:%(message)s')

class Database:
    def __init__(self, name):
        self._conn = sqlite3.connect(name)
        self._cursor = self._conn.cursor()
        #logging.info('Connected to database')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()
    
    def from_pandas(self, df, table_name, if_exists='replace'):
        df.to_sql(table_name, self.connection, if_exists=if_exists, index=False)

## consumer 

def consume_msg(db, chiave, value):
    data = eval(value)

    if chiave == 'info':
        print('start', data['table'] )
        df = pd.DataFrame(columns=data['cols']).astype(data['dtype'])
        db.from_pandas(df, data['table']) # a trick for creating table without a sql query
    
    elif chiave == 'stats':
        db.execute(c.insert_stats, tuple(data))

    elif chiave == 'regions':
        db.execute(c.insert_regions, tuple(data))

    elif chiave == 'age':
        db.execute(c.insert_age, tuple(data))

def listen(consumer, db):
    print('listening..')
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                pass
            elif msg.error():
                logging.error("ERROR: %s".format(msg.error()))
            else:
                if msg.key().decode('utf-8') == 'finish':
                    db.commit()
                    print('finish', msg.value())
                else:
                    try:
                        consume_msg(db, msg.key().decode('utf-8'), msg.value().decode('utf-8'))
                    except Exception as e:
                        print(e)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close() # Leave group and commit final offsets


# producer

def update_stats(producer):
    df_stats, data_types_stats = get_df_stats(c.url_latest, c.drop_stats, c.col_stats)
    for index, row in df_stats.iterrows():
        producer.produce(c.topic, key = 'stats', value = str(list(row))) 

    producer.poll(10) # Wait for delivery
    producer.flush() # Flush pending messages
 
    logging.info('table stats updated')
    producer.produce(c.topic, key = 'compute', value = str(list(row))) # if i put a string in the value it gives me name 'covid' not found 

   


def send_table(table, topic, producer, info):
    producer.produce(topic, key = 'info', value = str(info))
    producer.poll(0)
    for index, row in table.iterrows():
        producer.produce(topic, key = info['table'], value = str(list(row))) 

    producer.produce(topic, key = 'finish', value = str(info['table']))

    producer.poll(10) # Wait for delivery
    producer.flush() # Flush pending messages
    logging.info('table'+info['table']+' sent')

def get_df_region_age(url, col_names):
    df_region_age = pd.read_csv(url)                                                                     # load data 
    df_region_age = df_region_age.set_axis(col_names, axis=1, inplace=False)      
                                 # change column names
    return df_region_age

def get_df_region(df_region_age, group_by_region):
    df_region = df_region_age.groupby(group_by_region).sum().reset_index()  # group by region 
    data_types_region = df_region.dtypes.apply(lambda x: x.name).to_dict()
    return (df_region, data_types_region)

def get_df_age(df_region_age, col_drop_age):
    df_age = df_region_age.drop(columns=col_drop_age)            # drop redundant columns
    data_types_age = df_age.dtypes.apply(lambda x: x.name).to_dict()
    return (df_age, data_types_age)

def get_df_stats(url, col_drop, col_names):
    df_stats = pd.read_csv(url)                                     # load data
    df_stats = df_stats.drop(columns=col_drop)                      # drop useless columns
    df_stats = df_stats.set_axis(col_names, axis=1, inplace=False)  # change column names
    df_stats = df_stats.replace({np.nan: 0})

    f = df_stats.select_dtypes(np.number).drop(columns = ['lat', 'long'])    # select only numeric columns
    df_stats[f.columns]= f.round().astype('Int64')      
    data_types_stats = df_stats.dtypes.apply(lambda x: x.name).to_dict() # convert to int

    return (df_stats, data_types_stats)
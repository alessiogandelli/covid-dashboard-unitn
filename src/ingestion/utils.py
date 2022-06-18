import pandas as pd
import numpy as np
import constants as c
import logging
logging.basicConfig(filename='flow.log', level=logging.DEBUG)

def send_table(client, table, cols, topic):
    client.publish("covid_italy_col", str(cols)) 
    client.loop()
    for index, row in table.iterrows():
        client.publish(topic, str(list(row))) 
        client.loop()
    logging.info('table'+ cols['table']+ 'sent')

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

def update_stats(client):
    df_stats, data_types_stats = get_df_stats(c.url_latest, c.drop_stats, c.col_stats)
    for index, row in df_stats.iterrows():
        client.publish('covid_italy', str(list(row))) 
        client.loop()
    logging.info('table stats updated')
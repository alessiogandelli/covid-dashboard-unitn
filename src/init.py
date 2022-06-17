#%%
import sqlite3
import pandas as pd
import paho.mqtt.client as mqtt 
import numpy as np

## data source 
url_tot = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'
url_latest = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-latest.csv'
url_region = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-statistici-riferimento/popolazione-istat-regione-range.csv'

# constants
drop_stats = ['stato','casi_da_sospetto_diagnostico', 'casi_da_screening', 
                'note', 'note_test', 'note_casi', 'codice_nuts_1', 'codice_nuts_2']
drop_age = ['zone','sigla','cn1', 'cn2', 'region_name', 'lat', 'long']
col_stats = ['date', 'region_id', 'region_name', 'lat', 'long', 'recovered', 'intensive_care', 
            'hospitalized', 'domestic_isolation', 'total_positive', 'variation_total_positive', 
            'new_positive', 'dimessi_guariti', 'deaths', 'total_cases', 'test', 'tested_cases',
               'new_intensive_care', 'tot_positive_pcr', 'tot_positive_antigenic', 'test_pcr', 'test_antigenic']

col_region = ['region_id', 'cn1', 'zone', 'cn2','region_name', 'sigla', 'lat', 'long', 'age_group', 'population_males', 'population_females', 'population']


def send_table(table, cols, topic):
    client.publish("covid_italy_col", str(cols)) 
    client.loop()
    for index, row in table.iterrows():
        client.publish(topic, str(list(row))) 
        client.loop()


#%% data with cases  and other stats
df_stats = pd.read_csv(url_tot)                                 # load data
df_stats = df_stats.drop(columns=drop_stats)                    # drop useless columns
df_stats = df_stats.set_axis(col_stats, axis=1, inplace=False)  # change column names
df_stats = df_stats.replace({np.nan: 0})

f = df_stats.select_dtypes(np.number).drop(columns = ['lat', 'long'])    # select only numeric columns
df_stats[f.columns]= f.round().astype('Int64')      
data_types_stats = df_stats.dtypes.apply(lambda x: x.name).to_dict()
                     # convert to int

# %% region and age data
df_region_age = pd.read_csv(url_region)                                                                     # load data 
df_region_age = df_region_age.set_axis(col_region, axis=1, inplace=False)                                   # change column names
df_region = df_region_age.groupby(['region_id', 'zone', 'region_name', 'lat', 'long']).sum().reset_index()  # group by region 
df_age = df_region_age.drop(columns=['zone','sigla','cn1', 'cn2', 'region_name', 'lat', 'long'])            # drop redundant columns

data_types_region = df_region.dtypes.apply(lambda x: x.name).to_dict()
data_types_age = df_age.dtypes.apply(lambda x: x.name).to_dict()


#%% set up mqtt client
broker_address="broker.hivemq.com"
client = mqtt.Client("carlos")      #create new instance
client.connect(broker_address)      #connect to broker

# %% nome of the tables and the columns to store in the database 
stats_col = {'table':'cases', 'cols': list(df_stats), 'dtype': data_types_stats}
regions_col = {'table':'regions', 'cols': list(df_region), 'dtype': data_types_region}
age_col = {'table':'age', 'cols': list(df_age), 'dtype': data_types_age}

# send tables
send_table(df_age, age_col, "covid_italy_age")                  # age table
send_table(df_region, regions_col, "covid_italy_region")        # region table
send_table(df_stats, stats_col, "covid_italy")                  # stats table

# %%

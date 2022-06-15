#%%
import sqlite3
import pandas as pd
import paho.mqtt.client as mqtt #import the client1
import numpy as np


url_tot = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'
url_latest = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-latest.csv'
url_region = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-statistici-riferimento/popolazione-istat-regione-range.csv'

#%% data with cases  and other stats
data = pd.read_csv(url_tot)
data = data.drop(columns=['stato','casi_da_sospetto_diagnostico', 'casi_da_screening', 'note', 'note_test', 'note_casi', 'codice_nuts_1', 'codice_nuts_2'])
col_names_data = ['date', 'region_id', 'region_name', 
               'lat', 'long', 'recovered', 'intensive_care', 'hospitalized', 'domestic_isolation', 'total_positive',
               'variation_total_positive', 'new_positive', 'dimessi_guariti', 'deaths', 'total_cases', 'test', 'tested_cases',
               'new_intensive_care', 'tot_positive_pcr', 'tot_positive_antigenic', 'test_pcr', 'test_antigenic']

data = data.set_axis(col_names_data, axis=1, inplace=False)
data  = data.replace({np.nan: None})

# %% region and age data

data_region_age = pd.read_csv(url_region)
col_names_region = ['region_id', 'cn1', 'zone', 'cn2','region_name', 'sigla', 'lat', 'long', 'age_group', 'population_males', 'population_females', 'population']

data_region_age = data_region_age.set_axis(col_names_region, axis=1, inplace=False)
data_region = data_region_age.groupby(['region_id', 'zone', 'region_name', 'lat', 'long']).sum().reset_index()



data_age = data_region_age.drop(columns=['zone','sigla','cn1', 'cn2', 'region_name', 'lat', 'long'])


#%%

broker_address="broker.hivemq.com"
client = mqtt.Client("carlos") #create new instance
client.connect(broker_address) #connect to broker




# %%



# %%
data_col = {'table':'cases', 'cols': list(data)}
regions_col = {'table':'regions', 'cols': list(data_region)}
age_col = {'table':'age', 'cols': list(data_age)}


#%%
def send_table(table, cols, topic):
    client.publish("covid_italy_col", str(cols)) 
    client.loop()

    for index, row in table.iterrows():
        client.publish(topic, str(list(row))) 
        client.loop()
        
send_table(data_age, age_col, "covid_italy_age")
send_table(data_region, regions_col, "covid_italy_region")
send_table(data, data_col, "covid_italy")

# %%

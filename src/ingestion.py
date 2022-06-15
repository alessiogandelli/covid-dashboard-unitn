#%%
import sqlite3
import pandas as pd
import paho.mqtt.client as mqtt #import the client1



url_tot = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'
url_latest = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-latest.csv'

data = pd.read_csv(url_latest)
# drop useless columns
data = data.drop(columns=['stato','casi_da_sospetto_diagnostico', 'casi_da_screening', 'note', 'note_test', 'note_casi', 'codice_nuts_1', 'codice_nuts_2'])
# change column names 
col_names = ['date', 'region_id', 'region_name', 
               'lat', 'long', 'recovered', 'intensive_care', 'hospitalized', 'domestic_isolation', 'total_positive',
               'variation_total_positive', 'new_positive', 'dimessi_guariti', 'deaths', 'total_cases', 'test', 'tested_cases',
               'new_intensive_care', 'tot_positive_pcr', 'tot_positive_antigenic', 'test_pcr', 'test_antigenic']

data = data.set_axis(col_names, axis=1, inplace=False)
# %%



broker_address="broker.hivemq.com"
client = mqtt.Client("carlos") #create new instance
client.connect(broker_address) #connect to broker




# %%

for index, row in data.iterrows():
    client.publish("covid_italy", str(list(row))) #publish
    client.loop()

# %%
client.publish("covid_italy_col", str(list(data))) #publish
client.loop()
# %%


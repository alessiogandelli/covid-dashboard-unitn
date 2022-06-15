import sqlite3
import paho.mqtt.client as mqtt #import the client1
import time
import pandas as pd


insert_data = ''' insert into cases values ( ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,? )'''
insert_regions = ''' insert into regions values ( ?,?,?,?,?,?,?,? )'''
insert_age = ''' insert into age values ( ?,?,?,?,? )'''


class Database:
    def __init__(self, name):
        self._conn = sqlite3.connect(name)
        self._cursor = self._conn.cursor()
        print('Connected to database')

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

def on_message(client, userdata, message):
    data = eval(str(message.payload.decode("utf-8")))

    if message.topic == "covid_italy_col":
        df = pd.DataFrame(columns=data['cols'])
        db.from_pandas(df, data['table'])
        print('table', data['table'], 'created')

    elif  message.topic == "covid_italy":
        db.execute(insert_data, tuple(data))
        db.commit() # understand if the frequence of commits is a problem
    
    elif message.topic == "covid_italy_age":
        db.execute(insert_age, tuple(data))
        db.commit() # understand if the frequence of commits is a problem

    elif message.topic == "covid_italy_regions":
        db.execute(insert_regions, tuple(data))
        db.commit()

# set up the mqtt client
broker_address="broker.hivemq.com"
client = mqtt.Client("pyclient")   #create new instance
client.connect(broker_address)     #connect to broker
client.on_message=on_message       #attach function to callback
print("Client connected")

# subscribe to topics
print("Subscribing to topic","covid_italy_col")
print("Subscribing to topic","covid_italy_age")
print("Subscribing to topic","covid_italy_region")
print("Subscribing to topic","covid_italy")

client.subscribe("covid_italy")
client.subscribe("covid_italy_col")
client.subscribe("covid_italy_age")
client.subscribe("covid_italy_region")


db = Database('covid.sqlite')

client.loop_forever()









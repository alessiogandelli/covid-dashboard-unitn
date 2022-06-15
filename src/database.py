import sqlite3
import paho.mqtt.client as mqtt #import the client1
import time
import pandas as pd

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




broker_address="broker.hivemq.com"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("pyclient") #create new instance
print("connecting to broker")
client.connect(broker_address) #connect to broker


print("Subscribing to topic","covid_italy")
client.subscribe("covid_italy")
client.subscribe("covid_italy_col")
print("Subscribing to topic","covid_italy_col")


db = Database('covid.sqlite')

query = ''' insert into calamaro values ( ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,? )'''

def on_message(client, userdata, message):
    
    if (message.topic == "covid_italy_col"):
        cols = eval(str(message.payload.decode("utf-8")))
        df = pd.DataFrame(columns=cols)
        db.from_pandas(df, 'calamaro')
        print("Message arrived")
    else:
        line = eval(str(message.payload.decode("utf-8")))
        db.execute(query, tuple(line))
        db.commit()


client.on_message=on_message        #attach function to callback

client.loop_forever()

#db.from_pandas(data, 'covid_italy')



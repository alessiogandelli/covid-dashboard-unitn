#%%
import sqlite3
import pandas as pd



url_tot = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'

#%%


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



#%%
data = pd.read_csv(url_tot)

# drop useless columns
data = data.drop(columns=['stato','casi_da_sospetto_diagnostico', 'casi_da_screening', 'note', 'note_test', 'note_casi', 'codice_nuts_1', 'codice_nuts_2'])


# change column names 
col_names = ['date', 'region_id', 'region_name', 
               'lat', 'long', 'recovered', 'intensive_care', 'hospitalized', 'domestic_isolation', 'total_positive',
               'variation_total_positive', 'new_positive', 'dimessi_guariti', 'deaths', 'total_cases', 'test', 'tested_cases',
               'new_intensive_care', 'tot_positive_pcr', 'tot_positive_antigenic', 'test_pcr', 'test_antigenic']

data = data.set_axis(col_names, axis=1, inplace=False)
# %%


db = Database('covid.sqlite')
db.from_pandas(data, 'covid_italy')



# %%

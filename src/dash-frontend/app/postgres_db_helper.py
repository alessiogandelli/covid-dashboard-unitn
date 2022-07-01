import psycopg2

class Database:
    def __init__(self):
        dbname = 'covid'
        print('connecting to ' + dbname)
        self._conn = psycopg2.connect(
                            host='db',
                            database=dbname,
                            user='user',
                            password='example')
        self._cursor = self._conn.cursor()

        print('connected to db ' + dbname)

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

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()
    
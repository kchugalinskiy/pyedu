import psycopg2
from psycopg2.extras import DictCursor


class Repository(object):
    def __init__(self, host: str, port: str, dbname: str, username: str, password: str):
        self.conn = psycopg2.connect(dbname=dbname, user=username,
                                     password=password, host=host, port=port)
        print("pg connection at " + host + ':' + port)

    def get_number_of_tables(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute('SELECT count(*) FROM information_schema.tables')
            records = cursor.fetchall()
            return str(records[0]['count'])

import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor


class Repository(object):
    def __init__(self, host: str, port: str, dbname: str, username: str, password: str):
        self.conn = psycopg2.connect(dbname=dbname, user=username,
                                     password=password, host=host, port=port)
        print("pg connection at " + host + ':' + port)
        self.insert_query = sql.SQL("insert into {table}({username}) values (%s)").format(
            table=sql.Identifier('greetings'), username=sql.Identifier('username'))
        self.count_hello_query = sql.SQL('SELECT count(*) FROM {table} WHERE {username}=%s').format(
            username=sql.Identifier('username'), table=sql.Identifier('greetings'))

    def get_number_of_tables(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute('SELECT count(*) FROM information_schema.tables')
            records = cursor.fetchone()
            return str(records['count'])

    def insert_hello(self, username: str):
        with self.conn.cursor() as cursor:
            cursor.execute(self.insert_query, [username])
            self.conn.commit()

    def count_hello(self, username: str):
        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(self.count_hello_query, [username])
            records = cursor.fetchone()
            return records['count']

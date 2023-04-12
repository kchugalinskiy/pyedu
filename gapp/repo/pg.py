import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
from gapp.core.config import settings


class Repository(object):
    def __init__(self):
        self.conn = psycopg2.connect(dbname=settings.POSTGRES_DB,
                                     user=settings.POSTGRES_USER,
                                     password=settings.POSTGRES_PASSWORD,
                                     host=settings.POSTGRES_SERVER,
                                     port=settings.POSTGRES_PORT)
        print(f"pg connection at {settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}")
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

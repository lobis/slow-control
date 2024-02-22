from __future__ import annotations

import psycopg2
from psycopg2 import Error


class Database:
    def __init__(
        self, *, dbname: str, user: str, password: str, host: str, port: int = 5432
    ):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query):
        # reconnect if connection is closed
        if not self.connection:
            self.connect()

        try:
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error executing query: {e}")
            return None

    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database connection is closed")

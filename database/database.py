import sqlite3


class Database:

    def __init__(self):

        self.conn = sqlite3.connect(
            "database/database.db",
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.db_init()

    def db_init(self):

        with open(
            "database/schema.sql",
            "r",
            encoding="utf-8"
        ) as f:

            self.cursor.executescript(f.read())

        with open(
            "database/test_data.sql",
            "r",
            encoding="utf-8"
        ) as f:

            self.cursor.executescript(f.read())

        self.conn.commit()

    def execute(
        self,
        query,
        params=(),
        fetchone=False,
        fetchall=False
    ):

        self.cursor.execute(query, params)

        result = None

        if fetchone:
            result = self.cursor.fetchone()

        elif fetchall:
            result = self.cursor.fetchall()

        self.conn.commit()

        return result
    

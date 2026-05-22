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
    


    def clear_user_data(self, user_id):
        self.cursor.execute(
        "DELETE FROM mood_entries WHERE user_id = ?",
        (user_id,)
         )
        self.conn.commit()


    def add_entry(
        self,
        user_id,
        mood,
        work,
        sleep,
        comment
    ):

        query = """
        INSERT INTO mood_entries
        (
            user_id,
            mood,
            hours_work,
            hours_sleep,
            comment
        )

        VALUES (?, ?, ?, ?, ?)

        ON CONFLICT(user_id, entry_date)
        DO UPDATE SET
            mood = excluded.mood,
            hours_work = excluded.hours_work,
            hours_sleep = excluded.hours_sleep,
            comment = excluded.comment
        """

        self.execute(
            query,
            (user_id, mood, work, sleep, comment)
        )

    def get_history(self, user_id, limit=10):

        query = """
        SELECT
            entry_date,
            mood,
            hours_work,
            hours_sleep,
            comment

        FROM mood_entries

        WHERE user_id = ?

        ORDER BY entry_date DESC

        LIMIT ?
        """

        return self.execute(
            query,
            (user_id, limit),
            fetchall=True
        )

    def get_stats(self, user_id):

        query = """
        SELECT
            AVG(mood),
            AVG(hours_work),
            AVG(hours_sleep)

        FROM mood_entries

        WHERE user_id = ?
        """

        return self.execute(
            query,
            (user_id,),
            fetchone=True
        )

    def get_all_entries(self, user_id):

        query = """
        SELECT
            entry_date,
            mood,
            hours_work,
            hours_sleep,
            comment

        FROM mood_entries

        WHERE user_id = ?

        ORDER BY entry_date
        """

        return self.execute(
            query,
            (user_id,),
            fetchall=True
        )


db = Database()

print("SQLite подключена!")
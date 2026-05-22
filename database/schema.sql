    CREATE TABLE IF NOT EXISTS mood_entries (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        entry_date DATE DEFAULT CURRENT_DATE,

        mood INTEGER NOT NULL,

        hours_work REAL,

        hours_sleep REAL,

        comment TEXT,

        UNIQUE(user_id, entry_date)
    );
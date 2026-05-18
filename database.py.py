import sqlite3
from contextlib import contextmanager

DB_NAME = "data/group_collab.db"


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
        conn.commit()

    finally:
        conn.close()



def init_db():
    with get_conn() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_name TEXT UNIQUE,
                room_token TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS members (
                id TEXT PRIMARY KEY,
                room_name TEXT,
                name TEXT,
                nickname TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS availability (
                member_id TEXT,
                slot TEXT
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS norms (
                id TEXT PRIMARY KEY,
                room_name TEXT,
                content TEXT,
                supporters INTEGER DEFAULT 0,
                opponents INTEGER DEFAULT 0
            )
            """
        )
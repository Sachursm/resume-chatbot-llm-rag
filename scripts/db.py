import sqlite3

DB_NAME = 'database.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS resumes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                text TEXT
                )
                """)
    conn.commit()
    conn.close()
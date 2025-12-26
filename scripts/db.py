# Database Layer
import sqlite3

DB_NAME = "database.db"


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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER,
            question TEXT,
            answer TEXT
        )
    """)

    conn.commit()
    conn.close()


def get_all_resumes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, filename FROM resumes ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_chat_history(resume_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT question, answer FROM chat_history WHERE resume_id=? ORDER BY id",
        (resume_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

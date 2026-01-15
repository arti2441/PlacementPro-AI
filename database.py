import sqlite3
from datetime import datetime

DB_NAME = "app.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        description TEXT,
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()

def add_user(name, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)",
        (name, email, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    conn.close()
    return data

def add_record(user_id, title, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO records (user_id, title, description, created_at) VALUES (?, ?, ?, ?)",
        (user_id, title, description, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_records():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT records.id, users.name, records.title, records.description
        FROM records
        JOIN users ON records.user_id = users.id
    """)
    data = cur.fetchall()
    conn.close()
    return data
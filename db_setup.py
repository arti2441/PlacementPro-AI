import sqlite3
from datetime import datetime

def setup_database():
    """Create SQLite database with all tables"""
    conn = sqlite3.connect('placementpro.db')
    cursor = conn.cursor()
    
    # Users table (common for all)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,  -- student, tpo, faculty
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Student Profiles
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        university TEXT,
        batch TEXT,
        cgpa REAL,
        department TEXT,
        phone TEXT,
        target_role TEXT DEFAULT 'Data Scientist',
        skills TEXT DEFAULT '[]',  -- JSON array of skills
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    # TPO Profiles
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tpo_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        college TEXT,
        department TEXT,
        phone TEXT,
        position TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    # Faculty Profiles
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS faculty_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        college TEXT,
        department TEXT,
        phone TEXT,
        designation TEXT,
        expertise TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    setup_database()
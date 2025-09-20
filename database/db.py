# db/db.py
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

def connect():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT", 5432)
    )

def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pomodoro_sessions (
            id SERIAL PRIMARY KEY,
            start_time TIMESTAMP NOT NULL,
            duration INTEGER NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id SERIAL PRIMARY KEY,
            habit_name TEXT NOT NULL,
            date DATE NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ PostgreSQL tables are ready.")

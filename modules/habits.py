from database.db import connect
from datetime import date

# ------------------------------
# HABIT DATABASE FUNCTIONS
# ------------------------------

def add_habit(name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO habits (habit_name, date) VALUES (%s, %s)", (name, date.today()))
    conn.commit()
    conn.close()

def complete_habit(habit_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE habits SET completed = TRUE WHERE id = %s", (habit_id,))
    conn.commit()
    conn.close()

def get_today_habits():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, habit_name, completed FROM habits WHERE date = %s", (date.today(),))
    habits = cur.fetchall()
    conn.close()
    return habits

def get_habit_stats():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM habits")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM habits WHERE completed = TRUE")
    completed = cur.fetchone()[0]

    conn.close()
    return total, completed

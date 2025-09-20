# modules/timer.py

from database.db import connect
from datetime import datetime
from modules.quote import get_random_quote  # <- Import quote magic

def save_pomodoro_session(duration):
    conn = connect()
    cur = conn.cursor()

    start_time = datetime.now()
    cur.execute("""
        INSERT INTO pomodoro_sessions (start_time, duration)
        VALUES (%s, %s)
    """, (start_time, duration))

    conn.commit()
    cur.close()
    conn.close()

    # 🧠 Drop a quote after session is saved
    quote = get_random_quote()
    print(f"✅ Pomodoro saved: {duration} mins at {start_time}")
    print(f"💬 Motivation for you: “{quote}”")

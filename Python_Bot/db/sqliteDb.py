import sqlite3

import os

if os.path.exists("bot_database.db"):
    os.remove("bot_database.db")

connect = sqlite3.connect("bot_database.db", check_same_thread=False)
cursor = connect.cursor()

cursor.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    full_name TEXT
)
''')
connect.commit()


def add_or_update_user(user):
    cursor.execute('''
        INSERT INTO users(user_id, username, first_name, last_name,full_name)
        VALUES (?, ?, ?, ?,?)
        ON CONFLICT(user_id) DO UPDATE SET
            username=excluded.username,
            first_name=excluded.first_name,
            last_name=excluded.last_name,
            full_name=excluded.full_name
    ''', (user.id, user.username, user.first_name, user.last_name, user.full_name))
    connect.commit()

def get_user_data(user_id: int) -> str | None:
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    return row if row else None
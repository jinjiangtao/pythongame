import sqlite3
import os
from settings import DATABASE_NAME, MAX_HISTORY_COUNT

def init_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clipboard_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            copy_time TEXT NOT NULL,
            is_favorite INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_record(content, copy_time):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clipboard_history (content, copy_time, is_favorite) VALUES (?, ?, 0)', (content, copy_time))
    conn.commit()
    conn.close()
    trim_records()

def get_all_records(search_query=""):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    if search_query:
        cursor.execute('SELECT id, content, copy_time, is_favorite FROM clipboard_history WHERE content LIKE ? ORDER BY id DESC', ('%' + search_query + '%',))
    else:
        cursor.execute('SELECT id, content, copy_time, is_favorite FROM clipboard_history ORDER BY id DESC')
    records = cursor.fetchall()
    conn.close()
    return records

def get_record_by_id(record_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, content, copy_time, is_favorite FROM clipboard_history WHERE id = ?', (record_id,))
    record = cursor.fetchone()
    conn.close()
    return record

def delete_record(record_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clipboard_history WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

def delete_all_records():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clipboard_history')
    conn.commit()
    conn.close()

def toggle_favorite(record_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT is_favorite FROM clipboard_history WHERE id = ?', (record_id,))
    current = cursor.fetchone()[0]
    new_value = 1 if current == 0 else 0
    cursor.execute('UPDATE clipboard_history SET is_favorite = ? WHERE id = ?', (new_value, record_id))
    conn.commit()
    conn.close()
    return new_value

def trim_records():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM clipboard_history ORDER BY id DESC LIMIT -1 OFFSET ?', (MAX_HISTORY_COUNT,))
    old_records = cursor.fetchall()
    for record in old_records:
        cursor.execute('DELETE FROM clipboard_history WHERE id = ?', (record[0],))
    conn.commit()
    conn.close()

def get_record_count():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM clipboard_history')
    count = cursor.fetchone()[0]
    conn.close()
    return count
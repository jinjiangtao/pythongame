import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'attendance.db')

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            check_in_time TEXT,
            check_out_time TEXT,
            status TEXT DEFAULT '正常',
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_database()
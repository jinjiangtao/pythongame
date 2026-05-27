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
            department TEXT NOT NULL,
            position TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            email TEXT DEFAULT '',
            hire_date TEXT DEFAULT '',
            status TEXT DEFAULT '在职'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            check_in_time TEXT,
            check_out_time TEXT,
            status TEXT DEFAULT '正常',
            leave_type TEXT DEFAULT '',
            overtime_hours REAL DEFAULT 0.0,
            work_hours REAL DEFAULT 0.0,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            morning_start TEXT DEFAULT '09:00',
            morning_end TEXT DEFAULT '12:00',
            afternoon_start TEXT DEFAULT '13:30',
            afternoon_end TEXT DEFAULT '18:00',
            late_threshold INTEGER DEFAULT 30,
            early_leave_threshold INTEGER DEFAULT 30
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS operation_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operator TEXT DEFAULT 'SYSTEM',
            operation TEXT NOT NULL,
            target TEXT DEFAULT '',
            time TEXT NOT NULL,
            result TEXT DEFAULT 'SUCCESS'
        )
    ''')
    
    cursor.execute('''
        INSERT OR IGNORE INTO work_schedule (name, morning_start, morning_end, afternoon_start, afternoon_end)
        VALUES ('标准班次', '09:00', '12:00', '13:30', '18:00')
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_database()
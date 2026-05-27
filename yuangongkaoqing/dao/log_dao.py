import sqlite3
import os
from database.db_init import DB_PATH

class LogDAO:
    def __init__(self):
        self.ensure_db_directory()
        
    def ensure_db_directory(self):
        db_dir = os.path.dirname(DB_PATH)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def get_connection(self):
        return sqlite3.connect(DB_PATH)

    def add_log(self, operator, operation, target='', result='SUCCESS'):
        import datetime
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                INSERT INTO operation_log (operator, operation, target, time, result)
                VALUES (?, ?, ?, ?, ?)
            ''', (operator, operation, target, time, result))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding log: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def get_all_logs(self):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM operation_log ORDER BY time DESC LIMIT 100')
            return cursor.fetchall()
        except Exception as e:
            print(f"Error getting logs: {e}")
            return []
        finally:
            if conn:
                conn.close()
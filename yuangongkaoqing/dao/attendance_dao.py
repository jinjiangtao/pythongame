import sqlite3
import os
from model.attendance import Attendance
from database.db_init import DB_PATH

class AttendanceDAO:
    def __init__(self):
        self.ensure_db_directory()
        
    def ensure_db_directory(self):
        db_dir = os.path.dirname(DB_PATH)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def get_connection(self):
        return sqlite3.connect(DB_PATH)

    def add_attendance(self, attendance):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO attendance (employee_id, check_in_time, check_out_time, status)
                VALUES (?, ?, ?, ?)
            ''', (attendance.employee_id, attendance.check_in_time, 
                  attendance.check_out_time, attendance.status))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding attendance: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def update_attendance(self, attendance):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE attendance SET check_out_time = ?, status = ?
                WHERE id = ?
            ''', (attendance.check_out_time, attendance.status, attendance.id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating attendance: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def get_all_attendance(self):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM attendance ORDER BY check_in_time DESC')
            rows = cursor.fetchall()
            return [Attendance(row[1], row[2], row[3], row[4], row[0]) for row in rows]
        except Exception as e:
            print(f"Error getting attendance records: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_attendance_by_employee_id(self, employee_id):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM attendance WHERE employee_id = ? 
                ORDER BY check_in_time DESC
            ''', (employee_id,))
            rows = cursor.fetchall()
            return [Attendance(row[1], row[2], row[3], row[4], row[0]) for row in rows]
        except Exception as e:
            print(f"Error getting attendance by employee: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_today_attendance(self, employee_id, today_date):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM attendance 
                WHERE employee_id = ? AND check_in_time LIKE ?
            ''', (employee_id, f'{today_date}%'))
            row = cursor.fetchone()
            if row:
                return Attendance(row[1], row[2], row[3], row[4], row[0])
            return None
        except Exception as e:
            print(f"Error getting today's attendance: {e}")
            return None
        finally:
            if conn:
                conn.close()
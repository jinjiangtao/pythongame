import sqlite3
from model.attendance import Attendance
from database.db_init import DB_PATH

class AttendanceDAO:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def add_attendance(self, attendance):
        try:
            self.cursor.execute('''
                INSERT INTO attendance (employee_id, check_in_time, check_out_time, status)
                VALUES (?, ?, ?, ?)
            ''', (attendance.employee_id, attendance.check_in_time, 
                  attendance.check_out_time, attendance.status))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding attendance: {e}")
            return False

    def update_attendance(self, attendance):
        try:
            self.cursor.execute('''
                UPDATE attendance SET check_out_time = ?, status = ?
                WHERE id = ?
            ''', (attendance.check_out_time, attendance.status, attendance.id))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating attendance: {e}")
            return False

    def get_all_attendance(self):
        try:
            self.cursor.execute('SELECT * FROM attendance ORDER BY check_in_time DESC')
            rows = self.cursor.fetchall()
            return [Attendance(row[1], row[2], row[3], row[4], row[0]) for row in rows]
        except Exception as e:
            print(f"Error getting attendance records: {e}")
            return []

    def get_attendance_by_employee_id(self, employee_id):
        try:
            self.cursor.execute('''
                SELECT * FROM attendance WHERE employee_id = ? 
                ORDER BY check_in_time DESC
            ''', (employee_id,))
            rows = self.cursor.fetchall()
            return [Attendance(row[1], row[2], row[3], row[4], row[0]) for row in rows]
        except Exception as e:
            print(f"Error getting attendance by employee: {e}")
            return []

    def get_today_attendance(self, employee_id, today_date):
        try:
            self.cursor.execute('''
                SELECT * FROM attendance 
                WHERE employee_id = ? AND check_in_time LIKE ?
            ''', (employee_id, f'{today_date}%'))
            row = self.cursor.fetchone()
            if row:
                return Attendance(row[1], row[2], row[3], row[4], row[0])
            return None
        except Exception as e:
            print(f"Error getting today's attendance: {e}")
            return None

    def __del__(self):
        self.conn.close()
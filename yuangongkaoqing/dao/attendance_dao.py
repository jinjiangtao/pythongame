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
                INSERT INTO attendance (employee_id, check_in_time, check_out_time, status, 
                                      leave_type, overtime_hours, work_hours)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (attendance.employee_id, attendance.check_in_time, attendance.check_out_time, 
                  attendance.status, attendance.leave_type, 
                  attendance.overtime_hours, attendance.work_hours))
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
                UPDATE attendance SET check_out_time = ?, status = ?, leave_type = ?, 
                    overtime_hours = ?, work_hours = ?
                WHERE id = ?
            ''', (attendance.check_out_time, attendance.status, attendance.leave_type,
                  attendance.overtime_hours, attendance.work_hours, attendance.id))
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
            return [Attendance(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[0]) for row in rows]
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
            return [Attendance(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[0]) for row in rows]
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
                return Attendance(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[0])
            return None
        except Exception as e:
            print(f"Error getting today's attendance: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_attendance_by_date_range(self, start_date, end_date, employee_id=''):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = '''
                SELECT * FROM attendance 
                WHERE check_in_time >= ? AND check_in_time <= ?
            '''
            params = [f'{start_date} 00:00:00', f'{end_date} 23:59:59']
            
            if employee_id:
                query += ' AND employee_id = ?'
                params.append(employee_id)
            
            query += ' ORDER BY check_in_time DESC'
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            return [Attendance(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[0]) for row in rows]
        except Exception as e:
            print(f"Error getting attendance by date range: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_monthly_statistics(self, employee_id, year, month):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            start_date = f'{year}-{month:02d}-01'
            end_date = f'{year}-{month:02d}-31'
            
            cursor.execute('''
                SELECT status, COUNT(*) as count, 
                       SUM(work_hours) as total_work_hours,
                       SUM(overtime_hours) as total_overtime_hours
                FROM attendance 
                WHERE employee_id = ? AND check_in_time >= ? AND check_in_time <= ?
                GROUP BY status
            ''', (employee_id, f'{start_date} 00:00:00', f'{end_date} 23:59:59'))
            
            rows = cursor.fetchall()
            stats = {
                '正常': 0, '迟到': 0, '早退': 0, '缺勤': 0, '请假': 0, '加班': 0,
                'total_work_hours': 0.0, 'total_overtime_hours': 0.0
            }
            
            for row in rows:
                status = row[0]
                count = row[1]
                work_hours = row[2] if row[2] else 0.0
                overtime_hours = row[3] if row[3] else 0.0
                
                if status in stats:
                    stats[status] = count
                stats['total_work_hours'] += work_hours
                stats['total_overtime_hours'] += overtime_hours
            
            return stats
        except Exception as e:
            print(f"Error getting monthly statistics: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_department_monthly_statistics(self, department, year, month):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            start_date = f'{year}-{month:02d}-01'
            end_date = f'{year}-{month:02d}-31'
            
            cursor.execute('''
                SELECT a.status, COUNT(*) as count
                FROM attendance a
                JOIN employees e ON a.employee_id = e.employee_id
                WHERE e.department = ? AND a.check_in_time >= ? AND a.check_in_time <= ?
                GROUP BY a.status
            ''', (department, f'{start_date} 00:00:00', f'{end_date} 23:59:59'))
            
            rows = cursor.fetchall()
            stats = {'正常': 0, '迟到': 0, '早退': 0, '缺勤': 0, '请假': 0, '加班': 0}
            
            for row in rows:
                status = row[0]
                count = row[1]
                if status in stats:
                    stats[status] = count
            
            return stats
        except Exception as e:
            print(f"Error getting department monthly statistics: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def delete_attendance(self, attendance_id):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM attendance WHERE id = ?', (attendance_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting attendance: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def clear_all_attendance(self):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM attendance')
            conn.commit()
            return True
        except Exception as e:
            print(f"Error clearing attendance: {e}")
            return False
        finally:
            if conn:
                conn.close()
import sqlite3
import os
from model.employee import Employee
from database.db_init import DB_PATH

class EmployeeDAO:
    def __init__(self):
        self.ensure_db_directory()
        
    def ensure_db_directory(self):
        db_dir = os.path.dirname(DB_PATH)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def get_connection(self):
        return sqlite3.connect(DB_PATH)

    def add_employee(self, employee):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO employees (employee_id, name, department)
                VALUES (?, ?, ?)
            ''', (employee.employee_id, employee.name, employee.department))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error adding employee: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def get_all_employees(self):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM employees')
            rows = cursor.fetchall()
            return [Employee(row[1], row[2], row[3], row[0]) for row in rows]
        except Exception as e:
            print(f"Error getting employees: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_employee_by_id(self, employee_id):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM employees WHERE employee_id = ?', (employee_id,))
            row = cursor.fetchone()
            if row:
                return Employee(row[1], row[2], row[3], row[0])
            return None
        except Exception as e:
            print(f"Error getting employee: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def delete_employee(self, employee_id):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM employees WHERE employee_id = ?', (employee_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting employee: {e}")
            return False
        finally:
            if conn:
                conn.close()
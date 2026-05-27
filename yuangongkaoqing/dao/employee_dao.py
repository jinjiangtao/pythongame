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
                INSERT INTO employees (employee_id, name, department, position, phone, email, hire_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (employee.employee_id, employee.name, employee.department, 
                  employee.position, employee.phone, employee.email, 
                  employee.hire_date, employee.status))
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

    def update_employee(self, employee):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE employees SET name = ?, department = ?, position = ?, 
                    phone = ?, email = ?, hire_date = ?, status = ?
                WHERE employee_id = ?
            ''', (employee.name, employee.department, employee.position, 
                  employee.phone, employee.email, employee.hire_date, 
                  employee.status, employee.employee_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating employee: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def get_all_employees(self):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM employees ORDER BY employee_id')
            rows = cursor.fetchall()
            return [Employee(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[0]) for row in rows]
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
                return Employee(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[0])
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
            cursor.execute('DELETE FROM attendance WHERE employee_id = ?', (employee_id,))
            cursor.execute('DELETE FROM employees WHERE employee_id = ?', (employee_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting employee: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def search_employees(self, employee_id='', name='', department=''):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = 'SELECT * FROM employees WHERE 1=1'
            params = []
            
            if employee_id:
                query += ' AND employee_id LIKE ?'
                params.append(f'%{employee_id}%')
            if name:
                query += ' AND name LIKE ?'
                params.append(f'%{name}%')
            if department:
                query += ' AND department LIKE ?'
                params.append(f'%{department}%')
            
            query += ' ORDER BY employee_id'
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            return [Employee(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[0]) for row in rows]
        except Exception as e:
            print(f"Error searching employees: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def get_departments(self):
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT department FROM employees ORDER BY department')
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        except Exception as e:
            print(f"Error getting departments: {e}")
            return []
        finally:
            if conn:
                conn.close()
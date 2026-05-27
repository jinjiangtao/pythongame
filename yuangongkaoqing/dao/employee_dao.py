import sqlite3
from model.employee import Employee
from database.db_init import DB_PATH

class EmployeeDAO:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def add_employee(self, employee):
        try:
            self.cursor.execute('''
                INSERT INTO employees (employee_id, name, department)
                VALUES (?, ?, ?)
            ''', (employee.employee_id, employee.name, employee.department))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error adding employee: {e}")
            return False

    def get_all_employees(self):
        try:
            self.cursor.execute('SELECT * FROM employees')
            rows = self.cursor.fetchall()
            return [Employee(row[1], row[2], row[3], row[0]) for row in rows]
        except Exception as e:
            print(f"Error getting employees: {e}")
            return []

    def get_employee_by_id(self, employee_id):
        try:
            self.cursor.execute('SELECT * FROM employees WHERE employee_id = ?', (employee_id,))
            row = self.cursor.fetchone()
            if row:
                return Employee(row[1], row[2], row[3], row[0])
            return None
        except Exception as e:
            print(f"Error getting employee: {e}")
            return None

    def delete_employee(self, employee_id):
        try:
            self.cursor.execute('DELETE FROM employees WHERE employee_id = ?', (employee_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting employee: {e}")
            return False

    def __del__(self):
        self.conn.close()
class Employee:
    def __init__(self, employee_id, name, department, position='', phone='', email='', hire_date='', status='在职', id=None):
        self.id = id
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.position = position
        self.phone = phone
        self.email = email
        self.hire_date = hire_date
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'name': self.name,
            'department': self.department,
            'position': self.position,
            'phone': self.phone,
            'email': self.email,
            'hire_date': self.hire_date,
            'status': self.status
        }
class Employee:
    def __init__(self, employee_id, name, department, id=None):
        self.id = id
        self.employee_id = employee_id
        self.name = name
        self.department = department

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'name': self.name,
            'department': self.department
        }
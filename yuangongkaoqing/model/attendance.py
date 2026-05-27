class Attendance:
    def __init__(self, employee_id, check_in_time=None, check_out_time=None, status='正常', id=None):
        self.id = id
        self.employee_id = employee_id
        self.check_in_time = check_in_time
        self.check_out_time = check_out_time
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'check_in_time': self.check_in_time,
            'check_out_time': self.check_out_time,
            'status': self.status
        }
class Registration:
    def __init__(self, id, name, gender, department, doctor, phone, create_time):
        self.id = id
        self.name = name
        self.gender = gender
        self.department = department
        self.doctor = doctor
        self.phone = phone
        self.create_time = create_time

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'department': self.department,
            'doctor': self.doctor,
            'phone': self.phone,
            'create_time': self.create_time
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            name=data['name'],
            gender=data['gender'],
            department=data['department'],
            doctor=data['doctor'],
            phone=data['phone'],
            create_time=data['create_time']
        )

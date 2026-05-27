import json
import os
from models.registration import Registration

class StorageManager:
    def __init__(self, filename='registrations.json'):
        self.filename = filename
        self.data_dir = 'data'
        self.filepath = os.path.join(self.data_dir, filename)
        self._ensure_dir()

    def _ensure_dir(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def load_data(self):
        registrations = []
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        registrations.append(Registration.from_dict(item))
            except Exception:
                registrations = []
        return registrations

    def save_data(self, registrations):
        try:
            data = [reg.to_dict() for reg in registrations]
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def get_next_id(self):
        registrations = self.load_data()
        if not registrations:
            return 1
        max_id = max(reg.id for reg in registrations)
        return max_id + 1

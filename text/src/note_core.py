
from src.db import DatabaseManager

class NoteCore:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()
        self.current_note_id = None

    def create_new_note(self):
        self.current_note_id = None

    def save_note(self, title, content):
        if not title.strip() or not content.strip():
            raise ValueError("Title and content cannot be empty")
        
        if self.current_note_id:
            success = self.db_manager.update_note(self.current_note_id, title, content)
            return success
        else:
            note_id = self.db_manager.add_note(title, content)
            self.current_note_id = note_id
            return True

    def load_note(self, note_id):
        note = self.db_manager.get_note_by_id(note_id)
        if note:
            self.current_note_id = note[0]
            return note
        return None

    def delete_note(self, note_id):
        success = self.db_manager.delete_note(note_id)
        if success and self.current_note_id == note_id:
            self.current_note_id = None
        return success

    def get_all_notes(self):
        return self.db_manager.get_all_notes()

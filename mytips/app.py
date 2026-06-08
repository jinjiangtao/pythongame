import customtkinter as ctk
from database import Database
from note import NoteWindow
from tray import SystemTray
from settings import SettingsWindow
from reminder import ReminderAlert
from datetime import datetime
import threading
import time


class StickyNotesApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.db = Database()
        self.notes = {}
        self.root = ctk.CTk()
        self.root.withdraw()
        
        self.tray = SystemTray(self)
        self.tray.start()
        
        self._load_notes()
        self._setup_hotkeys()
        self._start_reminder_check()
        
    def _load_notes(self):
        notes_data = self.db.get_all_notes()
        for note_data in notes_data:
            self._create_note_from_data(note_data)
            
        if not notes_data:
            self.create_note()
            
    def _create_note_from_data(self, note_data):
        note = NoteWindow(
            self.root,
            self.db,
            note_id=note_data['id'],
            content=note_data['content'],
            x=note_data['x'],
            y=note_data['y'],
            width=note_data['width'],
            height=note_data['height'],
            color=note_data['color'],
            opacity=note_data['opacity'],
            font_size=note_data['font_size'],
            is_topmost=note_data['is_topmost'],
            reminder_time=note_data['reminder_time']
        )
        note.set_on_close(self._on_note_closed)
        self.notes[note_data['id']] = note
        
    def _setup_hotkeys(self):
        self.root.bind_all('<Control-n>', lambda e: self.create_note())
        self.root.bind_all('<Control-N>', lambda e: self.create_note())
        
    def _start_reminder_check(self):
        self.reminder_thread = threading.Thread(target=self._check_reminders, daemon=True)
        self.reminder_thread.start()
        
    def _check_reminders(self):
        checked_reminders = set()
        while True:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:00")
            notes_to_check = list(self.notes.items())
            for note_id, note in notes_to_check:
                if note.reminder_time and note.reminder_time == now:
                    key = f"{note_id}_{note.reminder_time}"
                    if key not in checked_reminders:
                        self.root.after(0, lambda n=note: ReminderAlert(self.root, n.content, n))
                        checked_reminders.add(key)
            time.sleep(1)
            
    def create_note(self):
        note = NoteWindow(self.root, self.db)
        note.set_on_close(self._on_note_closed)
        self.notes[note.note_id] = note
        
    def show_all_notes(self):
        for note in self.notes.values():
            note.deiconify()
            note.lift()
            
    def show_settings(self):
        SettingsWindow(self.root, self.db)
        
    def _on_note_closed(self, note):
        if note.note_id in self.notes:
            del self.notes[note.note_id]
            
    def quit_app(self):
        self.tray.stop()
        self.db.close()
        self.root.quit()
        
    def run(self):
        self.root.mainloop()

import sqlite3
import os
from typing import Optional, List, Dict, Any


class Database:
    def __init__(self, db_path: str = "notes.db"):
        self.db_path = db_path
        self.conn = None
        self._init_db()

    def _init_db(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                x INTEGER NOT NULL,
                y INTEGER NOT NULL,
                width INTEGER NOT NULL,
                height INTEGER NOT NULL,
                color TEXT NOT NULL,
                opacity REAL NOT NULL,
                font_size INTEGER NOT NULL,
                is_topmost INTEGER NOT NULL,
                reminder_time TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def get_all_notes(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM notes')
        columns = [desc[0] for desc in cursor.description]
        notes = []
        for row in cursor.fetchall():
            note = dict(zip(columns, row))
            note['is_topmost'] = bool(note['is_topmost'])
            notes.append(note)
        return notes

    def create_note(self, content: str, x: int, y: int, width: int, height: int,
                    color: str, opacity: float, font_size: int, is_topmost: bool,
                    reminder_time: Optional[str] = None) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO notes (content, x, y, width, height, color, opacity, font_size, is_topmost, reminder_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (content, x, y, width, height, color, opacity, font_size, int(is_topmost), reminder_time))
        self.conn.commit()
        return cursor.lastrowid

    def update_note(self, note_id: int, **kwargs):
        valid_columns = ['content', 'x', 'y', 'width', 'height', 'color', 'opacity', 'font_size', 'is_topmost', 'reminder_time']
        set_clause = []
        values = []
        for key, value in kwargs.items():
            if key in valid_columns:
                if key == 'is_topmost':
                    value = int(value)
                set_clause.append(f"{key} = ?")
                values.append(value)
        if set_clause:
            set_clause.append("updated_at = CURRENT_TIMESTAMP")
            cursor = self.conn.cursor()
            cursor.execute(f'UPDATE notes SET {", ".join(set_clause)} WHERE id = ?', (*values, note_id))
            self.conn.commit()

    def delete_note(self, note_id: int):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        self.conn.commit()

    def get_setting(self, key: str, default: Any = None) -> Any:
        cursor = self.conn.cursor()
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        return result[0] if result else default

    def set_setting(self, key: str, value: str):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, value))
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()

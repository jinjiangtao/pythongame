
import sqlite3
from src.config import DATABASE_NAME

class DatabaseManager:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self.conn = None
        self._initialize_database()

    def _connect(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def _initialize_database(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        conn.close()

    def add_note(self, title, content):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (title, content) VALUES (?, ?)",
            (title, content)
        )
        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return note_id

    def get_all_notes(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, content, created_at, updated_at FROM notes ORDER BY updated_at DESC")
        notes = cursor.fetchall()
        conn.close()
        return notes

    def get_note_by_id(self, note_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, content, created_at, updated_at FROM notes WHERE id = ?", (note_id,))
        note = cursor.fetchone()
        conn.close()
        return note

    def update_note(self, note_id, title, content):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE notes SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (title, content, note_id)
        )
        conn.commit()
        conn.close()
        return cursor.rowcount > 0

    def delete_note(self, note_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0

    def close(self):
        if self.conn:
            self.conn.close()

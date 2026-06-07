import sqlite3
import os
from settings import DATABASE_PATH, HISTORY_TABLE
from utils import get_timestamp


class HistoryManager:
    def __init__(self):
        self.conn = None
        self._connect()
        self._create_table()
    
    def _connect(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
    
    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {HISTORY_TABLE} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                image_name TEXT NOT NULL,
                image_path TEXT,
                ocr_result TEXT NOT NULL
            )
        ''')
        self.conn.commit()
    
    def add_record(self, image_name, image_path, ocr_result):
        cursor = self.conn.cursor()
        timestamp = get_timestamp()
        cursor.execute(f'''
            INSERT INTO {HISTORY_TABLE} (timestamp, image_name, image_path, ocr_result)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, image_name, image_path, ocr_result))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_records(self):
        cursor = self.conn.cursor()
        cursor.execute(f'''
            SELECT id, timestamp, image_name, image_path, ocr_result
            FROM {HISTORY_TABLE}
            ORDER BY id DESC
        ''')
        return cursor.fetchall()
    
    def get_record(self, record_id):
        cursor = self.conn.cursor()
        cursor.execute(f'''
            SELECT id, timestamp, image_name, image_path, ocr_result
            FROM {HISTORY_TABLE}
            WHERE id = ?
        ''', (record_id,))
        return cursor.fetchone()
    
    def delete_record(self, record_id):
        cursor = self.conn.cursor()
        cursor.execute(f'''
            DELETE FROM {HISTORY_TABLE}
            WHERE id = ?
        ''', (record_id,))
        self.conn.commit()
    
    def clear_all_records(self):
        cursor = self.conn.cursor()
        cursor.execute(f'DELETE FROM {HISTORY_TABLE}')
        self.conn.commit()
    
    def close(self):
        if self.conn:
            self.conn.close()

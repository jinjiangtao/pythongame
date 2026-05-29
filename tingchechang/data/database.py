import sqlite3
import os
import json
from datetime import datetime
from config import DATABASE_FILE, DEFAULT_CONFIG

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self._init_database()
    
    def _connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(DATABASE_FILE)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def _init_database(self):
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parking_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plate_number TEXT NOT NULL,
                vehicle_type TEXT NOT NULL,
                area TEXT NOT NULL,
                entry_time TEXT NOT NULL,
                exit_time TEXT,
                duration INTEGER,
                fee REAL,
                status TEXT NOT NULL DEFAULT 'parking'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS parking_spaces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area TEXT NOT NULL,
                space_number INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'available',
                plate_number TEXT,
                occupied_since TEXT
            )
        ''')
        
        self._init_default_config(cursor)
        self._init_parking_spaces(cursor)
        
        conn.commit()
    
    def _init_default_config(self, cursor):
        cursor.execute("SELECT COUNT(*) FROM system_config")
        if cursor.fetchone()[0] == 0:
            for key, value in DEFAULT_CONFIG.items():
                cursor.execute("INSERT INTO system_config (key, value) VALUES (?, ?)", 
                            (key, json.dumps(value)))
    
    def _init_parking_spaces(self, cursor):
        cursor.execute("SELECT COUNT(*) FROM parking_spaces")
        if cursor.fetchone()[0] == 0:
            areas = DEFAULT_CONFIG['areas']
            spaces_per_area = DEFAULT_CONFIG['total_spaces'] // len(areas)
            for area in areas:
                for i in range(1, spaces_per_area + 1):
                    cursor.execute("INSERT INTO parking_spaces (area, space_number, status) VALUES (?, ?, ?)",
                                (area, i, 'available'))
    
    def get_config(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM system_config")
        config = {}
        for row in cursor.fetchall():
            config[row['key']] = json.loads(row['value'])
        return config
    
    def update_config(self, key, value):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("REPLACE INTO system_config (key, value) VALUES (?, ?)", 
                    (key, json.dumps(value)))
        conn.commit()
    
    def add_parking_record(self, plate_number, vehicle_type, area):
        conn = self._connect()
        cursor = conn.cursor()
        entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO parking_records 
            (plate_number, vehicle_type, area, entry_time, status)
            VALUES (?, ?, ?, ?, 'parking')
        ''', (plate_number, vehicle_type, area, entry_time))
        
        record_id = cursor.lastrowid
        self._occupy_space(area, plate_number, entry_time)
        conn.commit()
        return record_id
    
    def _occupy_space(self, area, plate_number, entry_time):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE parking_spaces 
            SET status = 'occupied', plate_number = ?, occupied_since = ?
            WHERE id = (
                SELECT id FROM parking_spaces 
                WHERE area = ? AND status = 'available'
                LIMIT 1
            )
        ''', (plate_number, entry_time, area))
    
    def get_active_parking(self, plate_number=None):
        conn = self._connect()
        cursor = conn.cursor()
        if plate_number:
            cursor.execute('''
                SELECT * FROM parking_records 
                WHERE plate_number = ? AND status = 'parking'
            ''', (plate_number,))
        else:
            cursor.execute('''
                SELECT * FROM parking_records 
                WHERE status = 'parking'
            ''')
        return [dict(row) for row in cursor.fetchall()]
    
    def complete_parking(self, record_id, duration, fee):
        conn = self._connect()
        cursor = conn.cursor()
        exit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            SELECT plate_number, area FROM parking_records WHERE id = ?
        ''', (record_id,))
        record = cursor.fetchone()
        
        cursor.execute('''
            UPDATE parking_records 
            SET exit_time = ?, duration = ?, fee = ?, status = 'completed'
            WHERE id = ?
        ''', (exit_time, duration, fee, record_id))
        
        self._release_space(record['area'], record['plate_number'])
        conn.commit()
    
    def _release_space(self, area, plate_number):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE parking_spaces 
            SET status = 'available', plate_number = NULL, occupied_since = NULL
            WHERE area = ? AND plate_number = ?
        ''', (area, plate_number))
    
    def get_completed_records(self, start_date=None, end_date=None, plate_number=None, vehicle_type=None):
        conn = self._connect()
        cursor = conn.cursor()
        
        query = '''SELECT * FROM parking_records WHERE status = 'completed' '''
        params = []
        
        if start_date:
            query += '''AND entry_time >= ? '''
            params.append(start_date)
        if end_date:
            query += '''AND entry_time <= ? '''
            params.append(end_date)
        if plate_number:
            query += '''AND plate_number LIKE ? '''
            params.append(f'%{plate_number}%')
        if vehicle_type:
            query += '''AND vehicle_type = ? '''
            params.append(vehicle_type)
        
        query += '''ORDER BY entry_time DESC'''
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_space_status(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM parking_spaces ORDER BY area, space_number')
        return [dict(row) for row in cursor.fetchall()]
    
    def get_space_count(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('SELECT status, COUNT(*) FROM parking_spaces GROUP BY status')
        result = cursor.fetchall()
        count = {'total': 0, 'available': 0, 'occupied': 0}
        for row in result:
            count[row['status']] = row['COUNT(*)']
            count['total'] += row['COUNT(*)']
        return count
    
    def delete_record(self, record_id):
        conn = self._connect()
        cursor = conn.cursor()
        
        cursor.execute('SELECT plate_number, area, status FROM parking_records WHERE id = ?', (record_id,))
        record = cursor.fetchone()
        
        if record and record['status'] == 'parking':
            self._release_space(record['area'], record['plate_number'])
        
        cursor.execute('DELETE FROM parking_records WHERE id = ?', (record_id,))
        conn.commit()
    
    def backup_database(self, backup_path):
        conn = self._connect()
        with open(backup_path, 'w') as f:
            for line in conn.iterdump():
                f.write(line + '\n')
    
    def restore_database(self, backup_path):
        if self.conn:
            self.conn.close()
        self.conn = None
        
        with open(backup_path, 'r') as f:
            sql_content = f.read()
        
        conn = sqlite3.connect(DATABASE_FILE)
        conn.executescript(sql_content)
        conn.close()
        
        self.conn = None
    
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
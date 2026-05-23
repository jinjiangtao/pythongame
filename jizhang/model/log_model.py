from model.db import Database
from datetime import datetime


class LogModel:
    def __init__(self):
        self.db = Database()

    def add_log(self, user_id, username, operation_type, operation_desc, ip_address=None):
        self.db.execute(
            "INSERT INTO operation_logs (user_id, username, operation_type, operation_desc, ip_address) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, username, operation_type, operation_desc, ip_address)
        )
        return True

    def get_logs(self, user_id=None, operation_type=None, start_date=None, end_date=None, page=None, page_size=None):
        query = "SELECT id, user_id, username, operation_type, operation_desc, ip_address, created_at " \
                "FROM operation_logs " \
                "WHERE 1=1"
        params = []

        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)

        if operation_type:
            query += " AND operation_type = ?"
            params.append(operation_type)

        if start_date:
            query += " AND created_at >= ?"
            params.append(start_date)

        if end_date:
            query += " AND created_at <= ?"
            params.append(end_date)

        query += " ORDER BY created_at DESC"

        if page is not None and page_size is not None:
            offset = (page - 1) * page_size
            query += " LIMIT ? OFFSET ?"
            params.append(page_size)
            params.append(offset)

        return self.db.query(query, params)

    def get_logs_count(self, user_id=None, operation_type=None, start_date=None, end_date=None):
        query = "SELECT COUNT(*) FROM operation_logs WHERE 1=1"
        params = []

        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)

        if operation_type:
            query += " AND operation_type = ?"
            params.append(operation_type)

        if start_date:
            query += " AND created_at >= ?"
            params.append(start_date)

        if end_date:
            query += " AND created_at <= ?"
            params.append(end_date)

        result = self.db.query_one(query, params)
        return result[0] if result else 0
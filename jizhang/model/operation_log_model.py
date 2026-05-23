from model.db import Database
from datetime import datetime


class OperationLogModel:
    OPERATION_TYPES = {
        "LOGIN": "登录",
        "LOGOUT": "退出登录",
        "ADD_BILL": "添加账单",
        "UPDATE_BILL": "更新账单",
        "DELETE_BILL": "删除账单",
        "QUERY_BILL": "查询账单",
        "ADD_CATEGORY": "添加分类",
        "UPDATE_CATEGORY": "更新分类",
        "DELETE_CATEGORY": "删除分类",
        "QUERY_CATEGORY": "查询分类",
        "EXPORT_DATA": "导出数据",
        "BACKUP_DATA": "备份数据",
        "RESTORE_DATA": "恢复数据",
        "THEME_CHANGE": "切换主题"
    }

    def __init__(self):
        self.db = Database()

    def add_log(self, user_id, operation_type, description=None, details=None):
        if operation_type not in self.OPERATION_TYPES:
            return False, "无效的操作类型"

        operation_name = self.OPERATION_TYPES[operation_type]
        if description is None:
            description = operation_name

        self.db.execute(
            "INSERT INTO operation_logs (user_id, operation_type, operation_name, description, details) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, operation_type, operation_name, description, details)
        )
        return True, "日志记录成功"

    def get_logs(self, user_id, operation_type=None, start_date=None, end_date=None, page=None, page_size=None):
        query = "SELECT id, user_id, operation_type, operation_name, description, details, created_at " \
                "FROM operation_logs WHERE user_id = ?"
        params = [user_id]

        if operation_type:
            query += " AND operation_type = ?"
            params.append(operation_type)

        if start_date:
            query += " AND date(created_at) >= ?"
            params.append(start_date)

        if end_date:
            query += " AND date(created_at) <= ?"
            params.append(end_date)

        query += " ORDER BY created_at DESC"

        if page is not None and page_size is not None:
            offset = (page - 1) * page_size
            query += " LIMIT ? OFFSET ?"
            params.append(page_size)
            params.append(offset)

        return self.db.query(query, params)

    def get_logs_count(self, user_id, operation_type=None, start_date=None, end_date=None):
        query = "SELECT COUNT(*) FROM operation_logs WHERE user_id = ?"
        params = [user_id]

        if operation_type:
            query += " AND operation_type = ?"
            params.append(operation_type)

        if start_date:
            query += " AND date(created_at) >= ?"
            params.append(start_date)

        if end_date:
            query += " AND date(created_at) <= ?"
            params.append(end_date)

        result = self.db.query_one(query, params)
        return result[0] if result else 0

    def get_log_by_id(self, log_id, user_id):
        return self.db.query_one(
            "SELECT id, user_id, operation_type, operation_name, description, details, created_at "
            "FROM operation_logs WHERE id = ? AND user_id = ?",
            (log_id, user_id)
        )

    def delete_old_logs(self, user_id, days=30):
        self.db.execute(
            "DELETE FROM operation_logs WHERE user_id = ? AND date(created_at) < date('now', ? || ' days')",
            (user_id, -days)
        )
        return True, "清理成功"

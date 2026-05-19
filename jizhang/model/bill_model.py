from model.db import Database
from datetime import datetime


class BillModel:
    def __init__(self):
        self.db = Database()

    def add_bill(self, user_id, type_, category_id, amount, remark, payment_method, date):
        if type_ not in ('income', 'expense'):
            return False, "收支类型无效"
        
        if amount <= 0:
            return False, "金额必须大于0"
        
        if not payment_method:
            return False, "付款方式不能为空"
        
        if not date:
            return False, "日期不能为空"

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return False, "日期格式不正确，应为YYYY-MM-DD"

        category = self.db.query_one(
            "SELECT id FROM categories WHERE id = ? AND user_id = ?",
            (category_id, user_id)
        )
        if not category:
            return False, "分类不存在或无权限"

        self.db.execute(
            "INSERT INTO bills (user_id, type, category_id, amount, remark, payment_method, date) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, type_, category_id, amount, remark, payment_method, date)
        )
        return True, "添加成功"

    def update_bill(self, bill_id, user_id, type_, category_id, amount, remark, payment_method, date):
        if type_ not in ('income', 'expense'):
            return False, "收支类型无效"
        
        if amount <= 0:
            return False, "金额必须大于0"
        
        if not payment_method:
            return False, "付款方式不能为空"
        
        if not date:
            return False, "日期不能为空"

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return False, "日期格式不正确，应为YYYY-MM-DD"

        existing = self.db.query_one(
            "SELECT id FROM bills WHERE id = ? AND user_id = ?",
            (bill_id, user_id)
        )
        if not existing:
            return False, "账单不存在或无权限"

        category = self.db.query_one(
            "SELECT id FROM categories WHERE id = ? AND user_id = ?",
            (category_id, user_id)
        )
        if not category:
            return False, "分类不存在或无权限"

        self.db.execute(
            "UPDATE bills SET type = ?, category_id = ?, amount = ?, remark = ?, "
            "payment_method = ?, date = ? WHERE id = ? AND user_id = ?",
            (type_, category_id, amount, remark, payment_method, date, bill_id, user_id)
        )
        return True, "更新成功"

    def delete_bill(self, bill_id, user_id):
        existing = self.db.query_one(
            "SELECT id FROM bills WHERE id = ? AND user_id = ?",
            (bill_id, user_id)
        )
        if not existing:
            return False, "账单不存在或无权限"

        self.db.execute(
            "DELETE FROM bills WHERE id = ? AND user_id = ?",
            (bill_id, user_id)
        )
        return True, "删除成功"

    def get_bills(self, user_id, type_=None, start_date=None, end_date=None):
        query = "SELECT b.id, b.type, b.category_id, c.name as category_name, " \
                "b.amount, b.remark, b.payment_method, b.date, b.created_at " \
                "FROM bills b JOIN categories c ON b.category_id = c.id " \
                "WHERE b.user_id = ?"
        params = [user_id]

        if type_:
            query += " AND b.type = ?"
            params.append(type_)
        
        if start_date:
            query += " AND b.date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND b.date <= ?"
            params.append(end_date)

        query += " ORDER BY b.date DESC, b.created_at DESC"

        return self.db.query(query, params)

    def get_bill_by_id(self, bill_id, user_id):
        return self.db.query_one(
            "SELECT b.id, b.type, b.category_id, c.name as category_name, " \
            "b.amount, b.remark, b.payment_method, b.date " \
            "FROM bills b JOIN categories c ON b.category_id = c.id " \
            "WHERE b.id = ? AND b.user_id = ?",
            (bill_id, user_id)
        )

    def get_summary(self, user_id, start_date=None, end_date=None):
        query = "SELECT type, SUM(amount) FROM bills WHERE user_id = ?"
        params = [user_id]

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)

        query += " GROUP BY type"

        result = self.db.query(query, params)
        summary = {"income": 0, "expense": 0}
        for row in result:
            summary[row[0]] = row[1]
        
        return summary
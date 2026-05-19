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

    def get_bills(self, user_id, type_=None, start_date=None, end_date=None, category_id=None, page=None, page_size=None):
        query = "SELECT b.id, b.type, b.category_id, c.name as category_name, " \
                "b.amount, b.remark, b.payment_method, b.date, b.created_at " \
                "FROM bills b JOIN categories c ON b.category_id = c.id " \
                "WHERE b.user_id = ?"
        params = [user_id]

        if type_:
            query += " AND b.type = ?"
            params.append(type_)
        
        if category_id:
            query += " AND b.category_id = ?"
            params.append(category_id)
        
        if start_date:
            query += " AND b.date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND b.date <= ?"
            params.append(end_date)

        query += " ORDER BY b.date DESC, b.created_at DESC"

        if page is not None and page_size is not None:
            offset = (page - 1) * page_size
            query += " LIMIT ? OFFSET ?"
            params.append(page_size)
            params.append(offset)

        return self.db.query(query, params)

    def get_bills_count(self, user_id, type_=None, start_date=None, end_date=None, category_id=None):
        query = "SELECT COUNT(*) FROM bills b JOIN categories c ON b.category_id = c.id WHERE b.user_id = ?"
        params = [user_id]

        if type_:
            query += " AND b.type = ?"
            params.append(type_)
        
        if category_id:
            query += " AND b.category_id = ?"
            params.append(category_id)
        
        if start_date:
            query += " AND b.date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND b.date <= ?"
            params.append(end_date)

        result = self.db.query_one(query, params)
        return result[0] if result else 0

    def get_bill_by_id(self, bill_id, user_id):
        return self.db.query_one(
            "SELECT b.id, b.type, b.category_id, c.name as category_name, " \
            "b.amount, b.remark, b.payment_method, b.date " \
            "FROM bills b JOIN categories c ON b.category_id = c.id " \
            "WHERE b.id = ? AND b.user_id = ?",
            (bill_id, user_id)
        )

    def get_summary(self, user_id, type_=None, category_id=None, start_date=None, end_date=None):
        query = "SELECT type, SUM(amount) FROM bills WHERE user_id = ?"
        params = [user_id]

        if type_:
            query += " AND type = ?"
            params.append(type_)
        
        if category_id:
            query += " AND category_id = ?"
            params.append(category_id)
        
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

    def get_total_summary(self, user_id):
        query = "SELECT type, SUM(amount) FROM bills WHERE user_id = ? GROUP BY type"
        result = self.db.query(query, [user_id])
        summary = {"income": 0, "expense": 0}
        for row in result:
            summary[row[0]] = row[1]
        return summary

    def get_monthly_statistics(self, user_id, year=None):
        if year is None:
            year = datetime.now().year
        
        query = """
            SELECT strftime('%m', date) as month, 
                   SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
                   SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expense
            FROM bills 
            WHERE user_id = ? AND strftime('%Y', date) = ?
            GROUP BY month
            ORDER BY month
        """
        result = self.db.query(query, (user_id, str(year)))
        monthly_data = []
        for row in result:
            monthly_data.append((int(row[0]), row[1], row[2]))
        return monthly_data

    def get_yearly_statistics(self, user_id):
        query = """
            SELECT strftime('%Y', date) as year, 
                   SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
                   SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expense
            FROM bills 
            WHERE user_id = ?
            GROUP BY year
            ORDER BY year DESC
        """
        result = self.db.query(query, [user_id])
        yearly_data = []
        for row in result:
            yearly_data.append((int(row[0]), row[1], row[2]))
        return yearly_data

    def get_expense_category_statistics(self, user_id):
        query = """
            SELECT c.name as category_name, SUM(b.amount) as total_amount
            FROM bills b
            JOIN categories c ON b.category_id = c.id
            WHERE b.user_id = ? AND b.type = 'expense'
            GROUP BY c.id, c.name
            ORDER BY total_amount DESC
        """
        result = self.db.query(query, [user_id])
        category_data = []
        for row in result:
            category_data.append((row[0], row[1]))
        return category_data
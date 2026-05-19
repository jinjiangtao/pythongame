import random
from datetime import datetime, timedelta
from model.db import Database
from config import PAYMENT_METHODS

EXPENSE_CATEGORIES = ["餐饮", "交通", "购物", "娱乐", "医疗", "教育", "住房", "其他"]
INCOME_CATEGORIES = ["工资", "奖金", "投资收益", "兼职", "其他"]

def generate_test_data(user_id, count=100):
    db = Database()
    
    expense_cat_ids = []
    income_cat_ids = []
    
    for cat_name in EXPENSE_CATEGORIES:
        existing = db.query_one("SELECT id FROM categories WHERE user_id = ? AND name = ? AND type = 'expense'", (user_id, cat_name))
        if existing:
            expense_cat_ids.append(existing[0])
        else:
            db.execute("INSERT INTO categories (user_id, name, type) VALUES (?, ?, 'expense')", (user_id, cat_name))
            expense_cat_ids.append(db.get_last_insert_id())
    
    for cat_name in INCOME_CATEGORIES:
        existing = db.query_one("SELECT id FROM categories WHERE user_id = ? AND name = ? AND type = 'income'", (user_id, cat_name))
        if existing:
            income_cat_ids.append(existing[0])
        else:
            db.execute("INSERT INTO categories (user_id, name, type) VALUES (?, ?, 'income')", (user_id, cat_name))
            income_cat_ids.append(db.get_last_insert_id())
    
    today = datetime.now()
    
    for i in range(count):
        if random.random() < 0.7:
            type_ = "expense"
            category_ids = expense_cat_ids
            max_amount = 5000
        else:
            type_ = "income"
            category_ids = income_cat_ids
            max_amount = 20000
        
        category_id = random.choice(category_ids)
        amount = round(random.uniform(1, max_amount), 2)
        payment_method = random.choice(PAYMENT_METHODS)
        
        days_ago = random.randint(0, 30)
        date = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        remarks = ["日常消费", "购物支出", "工资收入", "投资回报", "生活开销", "娱乐消费", "医疗费用", "教育支出", "交通费用", ""]
        remark = random.choice(remarks)
        
        created_at = (today - timedelta(days=days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))).strftime("%Y-%m-%d %H:%M:%S")
        
        db.execute(
            "INSERT INTO bills (user_id, type, category_id, amount, remark, payment_method, date, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, type_, category_id, amount, remark, payment_method, date, created_at)
        )
    
    db.close()
    print(f"成功生成 {count} 条测试数据")

if __name__ == "__main__":
    generate_test_data(24, 100)
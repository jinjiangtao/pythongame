import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from model.user_model import UserModel
from model.category_model import CategoryModel
from model.bill_model import BillModel
from model.db import Database


class TestBillModel(unittest.TestCase):
    def setUp(self):
        self.user_model = UserModel()
        self.category_model = CategoryModel()
        self.bill_model = BillModel()
        
        self.test_username = "testuser_bill_123"
        self.test_password = "password123"
        
        success, _ = self.user_model.register(self.test_username, self.test_password)
        user, _ = self.user_model.login(self.test_username, self.test_password)
        self.user_id = user["id"]
        
        categories = self.category_model.get_categories(self.user_id, "expense")
        self.category_id = categories[0][0]

    def test_add_bill(self):
        success, message = self.bill_model.add_bill(
            self.user_id, "expense", self.category_id, 100.0, "测试备注", "现金", "2024-01-01"
        )
        self.assertTrue(success)
        self.assertEqual(message, "添加成功")

    def test_add_bill_invalid_amount(self):
        success, message = self.bill_model.add_bill(
            self.user_id, "expense", self.category_id, -100.0, "", "现金", "2024-01-01"
        )
        self.assertFalse(success)
        self.assertEqual(message, "金额必须大于0")

    def test_add_bill_invalid_type(self):
        success, message = self.bill_model.add_bill(
            self.user_id, "invalid", self.category_id, 100.0, "", "现金", "2024-01-01"
        )
        self.assertFalse(success)
        self.assertEqual(message, "收支类型无效")

    def test_add_bill_invalid_date(self):
        success, message = self.bill_model.add_bill(
            self.user_id, "expense", self.category_id, 100.0, "", "现金", "2024/01/01"
        )
        self.assertFalse(success)
        self.assertEqual(message, "日期格式不正确，应为YYYY-MM-DD")

    def test_update_bill(self):
        self.bill_model.add_bill(
            self.user_id, "expense", self.category_id, 100.0, "原备注", "现金", "2024-01-01"
        )
        bills = self.bill_model.get_bills(self.user_id)
        bill_id = bills[0][0]
        
        success, message = self.bill_model.update_bill(
            bill_id, self.user_id, "expense", self.category_id, 200.0, "修改后备注", "支付宝", "2024-02-02"
        )
        self.assertTrue(success)
        self.assertEqual(message, "更新成功")

    def test_delete_bill(self):
        self.bill_model.add_bill(
            self.user_id, "expense", self.category_id, 100.0, "", "现金", "2024-01-01"
        )
        bills = self.bill_model.get_bills(self.user_id)
        bill_id = bills[0][0]
        
        success, message = self.bill_model.delete_bill(bill_id, self.user_id)
        self.assertTrue(success)
        self.assertEqual(message, "删除成功")

    def test_get_bills(self):
        bills = self.bill_model.get_bills(self.user_id)
        self.assertIsInstance(bills, list)

    def test_get_bills_by_type(self):
        bills = self.bill_model.get_bills(self.user_id, type_="expense")
        self.assertIsInstance(bills, list)

    def test_get_summary(self):
        self.bill_model.add_bill(
            self.user_id, "income", self.category_id, 5000.0, "", "银行卡", "2024-01-01"
        )
        self.bill_model.add_bill(
            self.user_id, "expense", self.category_id, 1000.0, "", "现金", "2024-01-02"
        )
        
        summary = self.bill_model.get_summary(self.user_id)
        self.assertEqual(summary["income"], 5000.0)
        self.assertEqual(summary["expense"], 1000.0)

    def tearDown(self):
        db = Database()
        db.execute("DELETE FROM bills WHERE user_id = ?", (self.user_id,))
        db.execute("DELETE FROM users WHERE username = ?", (self.test_username,))


if __name__ == "__main__":
    unittest.main()
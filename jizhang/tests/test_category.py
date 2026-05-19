import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from model.user_model import UserModel
from model.category_model import CategoryModel
from model.db import Database


class TestCategoryModel(unittest.TestCase):
    def setUp(self):
        self.user_model = UserModel()
        self.category_model = CategoryModel()
        self.test_username = "testuser_cat_123"
        self.test_password = "password123"
        
        success, _ = self.user_model.register(self.test_username, self.test_password)
        user, _ = self.user_model.login(self.test_username, self.test_password)
        self.user_id = user["id"]

    def test_add_category(self):
        success, message = self.category_model.add_category(self.user_id, "测试分类", "expense")
        self.assertTrue(success)
        self.assertEqual(message, "添加成功")

    def test_add_category_empty_name(self):
        success, message = self.category_model.add_category(self.user_id, "", "expense")
        self.assertFalse(success)
        self.assertEqual(message, "分类名称不能为空")

    def test_add_category_invalid_type(self):
        success, message = self.category_model.add_category(self.user_id, "测试", "invalid")
        self.assertFalse(success)
        self.assertEqual(message, "分类类型无效")

    def test_add_duplicate_category(self):
        self.category_model.add_category(self.user_id, "重复分类", "expense")
        success, message = self.category_model.add_category(self.user_id, "重复分类", "expense")
        self.assertFalse(success)
        self.assertEqual(message, "该分类已存在")

    def test_update_category(self):
        success, _ = self.category_model.add_category(self.user_id, "原分类", "expense")
        categories = self.category_model.get_categories(self.user_id, "expense")
        cat_id = categories[-1][0]
        
        success, message = self.category_model.update_category(cat_id, self.user_id, "修改后分类")
        self.assertTrue(success)
        self.assertEqual(message, "更新成功")

    def test_update_nonexistent_category(self):
        success, message = self.category_model.update_category(99999, self.user_id, "测试")
        self.assertFalse(success)
        self.assertEqual(message, "分类不存在或无权限")

    def test_delete_category(self):
        success, _ = self.category_model.add_category(self.user_id, "删除测试", "expense")
        categories = self.category_model.get_categories(self.user_id, "expense")
        cat_id = categories[-1][0]
        
        success, message = self.category_model.delete_category(cat_id, self.user_id)
        self.assertTrue(success)
        self.assertEqual(message, "删除成功")

    def test_delete_nonexistent_category(self):
        success, message = self.category_model.delete_category(99999, self.user_id)
        self.assertFalse(success)
        self.assertEqual(message, "分类不存在或无权限")

    def test_get_categories(self):
        categories = self.category_model.get_categories(self.user_id)
        self.assertIsInstance(categories, list)

    def test_get_categories_by_type(self):
        expense_cats = self.category_model.get_categories(self.user_id, "expense")
        income_cats = self.category_model.get_categories(self.user_id, "income")
        self.assertIsInstance(expense_cats, list)
        self.assertIsInstance(income_cats, list)

    def tearDown(self):
        db = Database()
        db.execute("DELETE FROM categories WHERE user_id = ?", (self.user_id,))
        db.execute("DELETE FROM users WHERE username = ?", (self.test_username,))


if __name__ == "__main__":
    unittest.main()
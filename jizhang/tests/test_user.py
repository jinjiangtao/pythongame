import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from model.user_model import UserModel
from model.db import Database


class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.user_model = UserModel()
        self.test_username = "testuser_12345"
        self.test_password = "password123"

    def test_register_success(self):
        success, message = self.user_model.register(self.test_username, self.test_password)
        self.assertTrue(success)
        self.assertEqual(message, "注册成功")

    def test_register_empty_username(self):
        success, message = self.user_model.register("", self.test_password)
        self.assertFalse(success)
        self.assertEqual(message, "用户名和密码不能为空")

    def test_register_empty_password(self):
        success, message = self.user_model.register(self.test_username, "")
        self.assertFalse(success)
        self.assertEqual(message, "用户名和密码不能为空")

    def test_register_short_username(self):
        success, message = self.user_model.register("ab", self.test_password)
        self.assertFalse(success)
        self.assertEqual(message, "用户名长度至少为3个字符")

    def test_register_short_password(self):
        success, message = self.user_model.register(self.test_username, "12345")
        self.assertFalse(success)
        self.assertEqual(message, "密码长度至少为6个字符")

    def test_register_duplicate(self):
        self.user_model.register(self.test_username, self.test_password)
        success, message = self.user_model.register(self.test_username, self.test_password)
        self.assertFalse(success)
        self.assertEqual(message, "用户名已存在")

    def test_login_success(self):
        self.user_model.register(self.test_username, self.test_password)
        user, message = self.user_model.login(self.test_username, self.test_password)
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], self.test_username)
        self.assertEqual(message, "登录成功")

    def test_login_invalid_username(self):
        user, message = self.user_model.login("nonexistent", self.test_password)
        self.assertIsNone(user)
        self.assertEqual(message, "用户名或密码错误")

    def test_login_invalid_password(self):
        self.user_model.register(self.test_username, self.test_password)
        user, message = self.user_model.login(self.test_username, "wrongpassword")
        self.assertIsNone(user)
        self.assertEqual(message, "用户名或密码错误")

    def test_hash_password(self):
        password = "test123"
        hashed = self.user_model.hash_password(password)
        self.assertEqual(len(hashed), 64)
        self.assertEqual(hashed, self.user_model.hash_password(password))

    def tearDown(self):
        db = Database()
        db.execute("DELETE FROM users WHERE username LIKE 'testuser_%'")


if __name__ == "__main__":
    unittest.main()
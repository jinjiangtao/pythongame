import hashlib
from model.db import Database
from config import EXPENSE_DEFAULT_CATEGORIES, INCOME_DEFAULT_CATEGORIES


class UserModel:
    def __init__(self):
        self.db = Database()

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def register(self, username, password):
        if not username or not password:
            return False, "用户名和密码不能为空"
        
        if len(username) < 3:
            return False, "用户名长度至少为3个字符"
        
        if len(password) < 6:
            return False, "密码长度至少为6个字符"

        existing_user = self.db.query_one("SELECT id FROM users WHERE username = ?", (username,))
        if existing_user:
            return False, "用户名已存在"

        password_hash = self.hash_password(password)
        self.db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                       (username, password_hash))
        
        user_id = self.db.get_last_insert_id()
        self._init_default_categories(user_id)
        
        return True, "注册成功"

    def login(self, username, password):
        if not username or not password:
            return None, "用户名和密码不能为空"

        user = self.db.query_one("SELECT id, username, password_hash FROM users WHERE username = ?", 
                               (username,))
        
        if not user:
            return None, "用户名或密码错误"

        password_hash = self.hash_password(password)
        if user[2] == password_hash:
            return {"id": user[0], "username": user[1]}, "登录成功"
        else:
            return None, "用户名或密码错误"

    def _init_default_categories(self, user_id):
        for name in EXPENSE_DEFAULT_CATEGORIES:
            self.db.execute("INSERT INTO categories (user_id, name, type) VALUES (?, ?, 'expense')",
                           (user_id, name))
        
        for name in INCOME_DEFAULT_CATEGORIES:
            self.db.execute("INSERT INTO categories (user_id, name, type) VALUES (?, ?, 'income')",
                           (user_id, name))

    def get_user_by_id(self, user_id):
        user = self.db.query_one("SELECT id, username FROM users WHERE id = ?", (user_id,))
        if user:
            return {"id": user[0], "username": user[1]}
        return None
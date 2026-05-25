# -*- coding: utf-8 -*-

class UserModel:
    def __init__(self):
        self.users = {}
    
    def register(self, username, password):
        if username in self.users:
            return False, "用户名已存在"
        self.users[username] = password
        return True, "注册成功"
    
    def login(self, username, password):
        if username not in self.users:
            return False, "用户不存在"
        if self.users[username] != password:
            return False, "密码错误"
        return True, "登录成功"
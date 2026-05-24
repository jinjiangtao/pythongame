# -*- coding: utf-8 -*-
"""
Model层：负责数据管理
"""


class UserModel:
    """用户数据模型"""
    
    def __init__(self):
        self.users = {}
    
    def register(self, username, password):
        """注册新用户"""
        if username in self.users:
            return False, "用户名已存在"
        self.users[username] = password
        return True, "注册成功"
    
    def login(self, username, password):
        """用户登录"""
        if username not in self.users:
            return False, "用户不存在"
        if self.users[username] != password:
            return False, "密码错误"
        return True, "登录成功"


class StudentModel:
    """学生数据模型"""
    
    def __init__(self):
        self.students = []
    
    def add_student(self, student):
        """添加学生"""
        for s in self.students:
            if s['id'] == student['id']:
                return False, "学号已存在"
        self.students.append(student)
        return True, "添加成功"
    
    def delete_student(self, student_id):
        """删除学生"""
        for i, s in enumerate(self.students):
            if s['id'] == student_id:
                del self.students[i]
                return True, "删除成功"
        return False, "未找到该学生"
    
    def update_student(self, student_id, new_data):
        """更新学生信息"""
        for i, s in enumerate(self.students):
            if s['id'] == student_id:
                if new_data['id'] != student_id:
                    for other in self.students:
                        if other['id'] == new_data['id'] and other != s:
                            return False, "新学号已存在"
                self.students[i] = new_data
                return True, "更新成功"
        return False, "未找到该学生"
    
    def search_students(self, keyword):
        """搜索学生"""
        results = []
        for s in self.students:
            if keyword in s['id'] or keyword in s['name']:
                results.append(s)
        return results
    
    def get_all_students(self):
        """获取所有学生"""
        return self.students

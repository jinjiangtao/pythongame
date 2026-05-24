# -*- coding: utf-8 -*-
"""
Controller层：负责业务逻辑控制
"""
from model import UserModel, StudentModel
from view import LoginView, RegisterView, MainView


class Controller:
    """控制器"""
    
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        
        self.user_model = UserModel()
        self.student_model = StudentModel()
        
        self.current_user = None
        
        self.login_view = None
        self.register_view = None
        self.main_view = None
        
        self.show_login()
    
    def show_login(self):
        """显示登录界面"""
        self.login_view = LoginView(self.root, self.handle_login, self.show_register)
    
    def show_register(self):
        """显示注册界面"""
        self.register_view = RegisterView(self.root, self.handle_register, self.show_login)
    
    def show_main(self):
        """显示主界面"""
        self.main_view = MainView(self.root, self.handle_logout)
        self.bind_main_events()
        self.refresh_table()
    
    def handle_login(self, username, password):
        """处理登录"""
        if not username or not password:
            self.login_view.show_message("错误", "用户名和密码不能为空", "error")
            return
        
        success, message = self.user_model.login(username, password)
        if success:
            self.current_user = username
            self.login_view.close()
            self.show_main()
        else:
            self.login_view.show_message("登录失败", message, "error")
    
    def handle_register(self, username, password, confirm_password):
        """处理注册"""
        if not username or not password:
            self.register_view.show_message("错误", "用户名和密码不能为空", "error")
            return
        
        if password != confirm_password:
            self.register_view.show_message("错误", "两次密码输入不一致", "error")
            return
        
        success, message = self.user_model.register(username, password)
        if success:
            self.register_view.show_message("注册成功", message, "info")
            self.register_view.close()
            self.show_login()
        else:
            self.register_view.show_message("注册失败", message, "error")
    
    def handle_logout(self):
        """处理登出"""
        self.current_user = None
        self.show_login()
    
    def bind_main_events(self):
        """绑定主界面事件"""
        self.main_view.add_btn.config(command=self.add_student)
        self.main_view.delete_btn.config(command=self.delete_student)
        self.main_view.update_btn.config(command=self.update_student)
        self.main_view.clear_btn.config(command=self.main_view.clear_input)
        self.main_view.search_btn.config(command=self.search_students)
        self.main_view.refresh_btn.config(command=self.refresh_table)
        self.main_view.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
    
    def add_student(self):
        """添加学生"""
        data = self.main_view.get_input_data()
        
        if not data['id'] or not data['name']:
            self.main_view.show_message("错误", "学号和姓名不能为空", "error")
            return
        
        try:
            age = int(data['age'])
            if age <= 0:
                raise ValueError
        except ValueError:
            self.main_view.show_message("错误", "年龄必须是正整数", "error")
            return
        
        try:
            score = float(data['score'])
            if score < 0 or score > 100:
                raise ValueError
        except ValueError:
            self.main_view.show_message("错误", "成绩必须是0-100之间的数字", "error")
            return
        
        student = {
            'id': data['id'],
            'name': data['name'],
            'gender': data['gender'],
            'age': str(age),
            'class': data['class'],
            'score': str(score)
        }
        
        success, message = self.student_model.add_student(student)
        if success:
            self.main_view.show_message("成功", message, "info")
            self.main_view.clear_input()
            self.refresh_table()
        else:
            self.main_view.show_message("失败", message, "error")
    
    def delete_student(self):
        """删除学生"""
        selected = self.main_view.get_selected_item()
        if not selected:
            self.main_view.show_message("警告", "请先选中要删除的学生", "warning")
            return
        
        student_id = selected[0]
        success, message = self.student_model.delete_student(student_id)
        if success:
            self.main_view.show_message("成功", message, "info")
            self.main_view.clear_input()
            self.refresh_table()
        else:
            self.main_view.show_message("失败", message, "error")
    
    def update_student(self):
        """更新学生"""
        selected = self.main_view.get_selected_item()
        if not selected:
            self.main_view.show_message("警告", "请先选中要修改的学生", "warning")
            return
        
        data = self.main_view.get_input_data()
        
        if not data['id'] or not data['name']:
            self.main_view.show_message("错误", "学号和姓名不能为空", "error")
            return
        
        try:
            age = int(data['age'])
            if age <= 0:
                raise ValueError
        except ValueError:
            self.main_view.show_message("错误", "年龄必须是正整数", "error")
            return
        
        try:
            score = float(data['score'])
            if score < 0 or score > 100:
                raise ValueError
        except ValueError:
            self.main_view.show_message("错误", "成绩必须是0-100之间的数字", "error")
            return
        
        new_student = {
            'id': data['id'],
            'name': data['name'],
            'gender': data['gender'],
            'age': str(age),
            'class': data['class'],
            'score': str(score)
        }
        
        old_id = selected[0]
        success, message = self.student_model.update_student(old_id, new_student)
        if success:
            self.main_view.show_message("成功", message, "info")
            self.main_view.clear_input()
            self.refresh_table()
        else:
            self.main_view.show_message("失败", message, "error")
    
    def search_students(self):
        """搜索学生"""
        keyword = self.main_view.get_search_keyword()
        if not keyword:
            self.refresh_table()
            return
        
        students = self.student_model.search_students(keyword)
        self.main_view.update_table(students)
    
    def refresh_table(self):
        """刷新表格"""
        students = self.student_model.get_all_students()
        self.main_view.update_table(students)
    
    def on_tree_select(self, event):
        """表格选中事件"""
        selected = self.main_view.get_selected_item()
        if selected:
            data = {
                'id': selected[0],
                'name': selected[1],
                'gender': selected[2],
                'age': selected[3],
                'class': selected[4],
                'score': selected[5]
            }
            self.main_view.set_input_data(data)

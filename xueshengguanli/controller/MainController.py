# -*- coding: utf-8 -*-
from model.UserModel import UserModel
from model.StudentModel import StudentModel
from model.SubjectModel import SubjectModel
from view.LoginView import LoginView
from view.RegisterView import RegisterView
from view.MainView import MainView

class MainController:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        
        self.user_model = UserModel()
        self.student_model = StudentModel()
        self.subject_model = SubjectModel()
        
        self.current_user = None
        
        self.login_view = None
        self.register_view = None
        self.main_view = None
        
        self.show_login()
    
    def show_login(self):
        self.login_view = LoginView(self.root, self.handle_login, self.show_register)
    
    def show_register(self):
        self.register_view = RegisterView(self.root, self.handle_register, self.show_login)
    
    def show_main(self):
        self.main_view = MainView(self.root, self.handle_logout)
        self.bind_main_events()
        self.refresh_subjects()
        self.refresh_table()
        self.update_stats()
    
    def handle_login(self, username, password):
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
        self.current_user = None
        self.show_login()
    
    def bind_main_events(self):
        self.main_view.add_btn.config(command=self.add_student)
        self.main_view.delete_btn.config(command=self.delete_student)
        self.main_view.update_btn.config(command=self.update_student)
        self.main_view.clear_btn.config(command=self.main_view.clear_input)
        self.main_view.search_btn.config(command=self.search_students)
        self.main_view.refresh_btn.config(command=self.refresh_table)
        self.main_view.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        self.main_view.add_subject_btn.config(command=self.add_subject)
        self.main_view.delete_subject_btn.config(command=self.delete_subject)
    
    def add_subject(self):
        subject_name = self.main_view.get_new_subject_name()
        
        if not subject_name.strip():
            self.main_view.show_message("错误", "学科名称不能为空", "error")
            return
        
        success, message = self.subject_model.add_subject(subject_name)
        if success:
            self.main_view.show_message("成功", message, "info")
            self.main_view.clear_subject_input()
            self.refresh_subjects()
        else:
            self.main_view.show_message("失败", message, "error")
    
    def delete_subject(self):
        subject_name = self.main_view.get_selected_subject()
        
        if not subject_name:
            self.main_view.show_message("警告", "请先选中要删除的学科", "warning")
            return
        
        success, message = self.subject_model.delete_subject(subject_name)
        if success:
            self.main_view.show_message("成功", message, "info")
            self.refresh_subjects()
        else:
            self.main_view.show_message("失败", message, "error")
    
    def refresh_subjects(self):
        subjects = self.subject_model.get_all_subjects()
        self.main_view.update_subject_list(subjects)
        self.main_view.update_score_fields(subjects)
        self.main_view.update_table_columns(subjects)
        self.refresh_table()
        self.update_stats()
    
    def add_student(self):
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
        
        subjects = self.subject_model.get_all_subjects()
        for subject in subjects:
            score = data['scores'].get(subject, '')
            if score:
                try:
                    score_val = float(score)
                    if score_val < 0 or score_val > 100:
                        raise ValueError
                except ValueError:
                    self.main_view.show_message("错误", f"{subject}成绩必须是0-100之间的数字", "error")
                    return
        
        student = {
            'id': data['id'],
            'name': data['name'],
            'gender': data['gender'],
            'age': str(age),
            'class': data['class'],
            'scores': data['scores']
        }
        
        success, message = self.student_model.add_student(student)
        if success:
            self.main_view.show_message("成功", message, "info")
            self.main_view.clear_input()
            self.refresh_table()
            self.update_stats()
        else:
            self.main_view.show_message("失败", message, "error")
    
    def delete_student(self):
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
            self.update_stats()
        else:
            self.main_view.show_message("失败", message, "error")
    
    def update_student(self):
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
        
        subjects = self.subject_model.get_all_subjects()
        for subject in subjects:
            score = data['scores'].get(subject, '')
            if score:
                try:
                    score_val = float(score)
                    if score_val < 0 or score_val > 100:
                        raise ValueError
                except ValueError:
                    self.main_view.show_message("错误", f"{subject}成绩必须是0-100之间的数字", "error")
                    return
        
        new_student = {
            'id': data['id'],
            'name': data['name'],
            'gender': data['gender'],
            'age': str(age),
            'class': data['class'],
            'scores': data['scores']
        }
        
        old_id = selected[0]
        success, message = self.student_model.update_student(old_id, new_student)
        if success:
            self.main_view.show_message("成功", message, "info")
            self.main_view.clear_input()
            self.refresh_table()
            self.update_stats()
        else:
            self.main_view.show_message("失败", message, "error")
    
    def search_students(self):
        keyword = self.main_view.get_search_keyword()
        if not keyword:
            self.refresh_table()
            return
        
        students = self.student_model.search_students(keyword)
        self.main_view.update_table(students)
    
    def refresh_table(self):
        students = self.student_model.get_all_students()
        self.main_view.update_table(students)
    
    def update_stats(self):
        total_count = self.student_model.get_total_count()
        class_dist = self.student_model.get_class_distribution()
        subjects = self.subject_model.get_all_subjects()
        subject_avg = self.student_model.get_subject_averages(subjects)
        self.main_view.update_stats(total_count, class_dist, subject_avg)
    
    def on_tree_select(self, event):
        selected = self.main_view.get_selected_item()
        if selected:
            data = {
                'id': selected[0],
                'name': selected[1],
                'gender': selected[2],
                'age': selected[3],
                'class': selected[4],
                'scores': {}
            }
            subjects = self.subject_model.get_all_subjects()
            for i, subject in enumerate(subjects):
                if i + 5 < len(selected):
                    data['scores'][subject] = selected[i + 5]
            self.main_view.set_input_data(data)
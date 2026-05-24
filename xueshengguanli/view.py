# -*- coding: utf-8 -*-
"""
View层：负责界面显示
"""
import tkinter as tk
from tkinter import ttk, messagebox


class LoginView:
    """登录界面"""
    
    def __init__(self, parent, on_login, on_register):
        self.parent = parent
        self.on_login = on_login
        self.on_register = on_register
        self.window = tk.Toplevel(parent)
        self.window.title("学生信息管理系统 - 登录")
        self.window.geometry("400x300")
        self.center_window()
        self.create_widgets()
    
    def center_window(self):
        """窗口居中"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def create_widgets(self):
        """创建界面控件"""
        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(expand=True)
        
        tk.Label(frame, text="学生信息管理系统", font=("微软雅黑", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(frame, text="用户名：", font=("微软雅黑", 12)).grid(row=1, column=0, sticky=tk.E, pady=5)
        self.username_entry = tk.Entry(frame, font=("微软雅黑", 12))
        self.username_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(frame, text="密  码：", font=("微软雅黑", 12)).grid(row=2, column=0, sticky=tk.E, pady=5)
        self.password_entry = tk.Entry(frame, font=("微软雅黑", 12), show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        
        button_frame = tk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        tk.Button(button_frame, text="登录", font=("微软雅黑", 12), width=10, command=self.login).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="注册", font=("微软雅黑", 12), width=10, command=self.register).pack(side=tk.LEFT, padx=5)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.on_login(username, password)
    
    def register(self):
        self.window.destroy()
        self.on_register()
    
    def show_message(self, title, message, msg_type="info"):
        if msg_type == "error":
            messagebox.showerror(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)
    
    def close(self):
        self.window.destroy()


class RegisterView:
    """注册界面"""
    
    def __init__(self, parent, on_register, on_back):
        self.parent = parent
        self.on_register = on_register
        self.on_back = on_back
        self.window = tk.Toplevel(parent)
        self.window.title("学生信息管理系统 - 注册")
        self.window.geometry("400x350")
        self.center_window()
        self.create_widgets()
    
    def center_window(self):
        """窗口居中"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def create_widgets(self):
        """创建界面控件"""
        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(expand=True)
        
        tk.Label(frame, text="用户注册", font=("微软雅黑", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        tk.Label(frame, text="用户名：", font=("微软雅黑", 12)).grid(row=1, column=0, sticky=tk.E, pady=5)
        self.username_entry = tk.Entry(frame, font=("微软雅黑", 12))
        self.username_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(frame, text="密  码：", font=("微软雅黑", 12)).grid(row=2, column=0, sticky=tk.E, pady=5)
        self.password_entry = tk.Entry(frame, font=("微软雅黑", 12), show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(frame, text="确认密码：", font=("微软雅黑", 12)).grid(row=3, column=0, sticky=tk.E, pady=5)
        self.confirm_password_entry = tk.Entry(frame, font=("微软雅黑", 12), show="*")
        self.confirm_password_entry.grid(row=3, column=1, pady=5)
        
        button_frame = tk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        tk.Button(button_frame, text="注册", font=("微软雅黑", 12), width=10, command=self.register).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="返回", font=("微软雅黑", 12), width=10, command=self.back).pack(side=tk.LEFT, padx=5)
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        self.on_register(username, password, confirm_password)
    
    def back(self):
        self.window.destroy()
        self.on_back()
    
    def show_message(self, title, message, msg_type="info"):
        if msg_type == "error":
            messagebox.showerror(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)
    
    def close(self):
        self.window.destroy()


class MainView:
    """主界面"""
    
    def __init__(self, parent, on_logout):
        self.parent = parent
        self.on_logout = on_logout
        self.window = tk.Toplevel(parent)
        self.window.title("学生信息管理系统")
        self.window.geometry("900x600")
        self.center_window()
        self.create_widgets()
    
    def center_window(self):
        """窗口居中"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def create_widgets(self):
        """创建主界面控件"""
        top_frame = tk.Frame(self.window, padx=10, pady=10)
        top_frame.pack(fill=tk.X)
        
        tk.Label(top_frame, text="学生信息管理系统", font=("微软雅黑", 18, "bold")).pack(side=tk.LEFT)
        tk.Button(top_frame, text="登出", font=("微软雅黑", 10), command=self.logout).pack(side=tk.RIGHT)
        
        input_frame = tk.LabelFrame(self.window, text="学生信息", font=("微软雅黑", 12), padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        field_frame = tk.Frame(input_frame)
        field_frame.pack(fill=tk.X)
        
        tk.Label(field_frame, text="学号：", font=("微软雅黑", 11)).grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.id_entry = tk.Entry(field_frame, font=("微软雅黑", 11))
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(field_frame, text="姓名：", font=("微软雅黑", 11)).grid(row=0, column=2, sticky=tk.E, padx=5, pady=5)
        self.name_entry = tk.Entry(field_frame, font=("微软雅黑", 11))
        self.name_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(field_frame, text="性别：", font=("微软雅黑", 11)).grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.gender_var = tk.StringVar()
        self.gender_combo = ttk.Combobox(field_frame, textvariable=self.gender_var, font=("微软雅黑", 11), state="readonly")
        self.gender_combo['values'] = ("男", "女")
        self.gender_combo.current(0)
        self.gender_combo.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(field_frame, text="年龄：", font=("微软雅黑", 11)).grid(row=1, column=2, sticky=tk.E, padx=5, pady=5)
        self.age_entry = tk.Entry(field_frame, font=("微软雅黑", 11))
        self.age_entry.grid(row=1, column=3, padx=5, pady=5)
        
        tk.Label(field_frame, text="班级：", font=("微软雅黑", 11)).grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.class_entry = tk.Entry(field_frame, font=("微软雅黑", 11))
        self.class_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(field_frame, text="成绩：", font=("微软雅黑", 11)).grid(row=2, column=2, sticky=tk.E, padx=5, pady=5)
        self.score_entry = tk.Entry(field_frame, font=("微软雅黑", 11))
        self.score_entry.grid(row=2, column=3, padx=5, pady=5)
        
        button_frame1 = tk.Frame(input_frame)
        button_frame1.pack(fill=tk.X, pady=10)
        
        self.add_btn = tk.Button(button_frame1, text="新增", font=("微软雅黑", 11), width=8)
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = tk.Button(button_frame1, text="删除", font=("微软雅黑", 11), width=8)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        self.update_btn = tk.Button(button_frame1, text="修改", font=("微软雅黑", 11), width=8)
        self.update_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(button_frame1, text="清空", font=("微软雅黑", 11), width=8)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        search_frame = tk.Frame(input_frame)
        search_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(search_frame, text="搜索：", font=("微软雅黑", 11)).pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, font=("微软雅黑", 11), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_btn = tk.Button(search_frame, text="查询", font=("微软雅黑", 11), width=8)
        self.search_btn.pack(side=tk.LEFT, padx=5)
        self.refresh_btn = tk.Button(search_frame, text="刷新", font=("微软雅黑", 11), width=8)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        table_frame = tk.Frame(self.window, padx=10, pady=5)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("id", "name", "gender", "age", "class", "score")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="学号")
        self.tree.heading("name", text="姓名")
        self.tree.heading("gender", text="性别")
        self.tree.heading("age", text="年龄")
        self.tree.heading("class", text="班级")
        self.tree.heading("score", text="成绩")
        
        self.tree.column("id", width=120, anchor=tk.CENTER)
        self.tree.column("name", width=120, anchor=tk.CENTER)
        self.tree.column("gender", width=80, anchor=tk.CENTER)
        self.tree.column("age", width=80, anchor=tk.CENTER)
        self.tree.column("class", width=120, anchor=tk.CENTER)
        self.tree.column("score", width=120, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def get_input_data(self):
        """获取输入框数据"""
        return {
            'id': self.id_entry.get(),
            'name': self.name_entry.get(),
            'gender': self.gender_var.get(),
            'age': self.age_entry.get(),
            'class': self.class_entry.get(),
            'score': self.score_entry.get()
        }
    
    def set_input_data(self, data):
        """设置输入框数据"""
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, data.get('id', ''))
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, data.get('name', ''))
        self.gender_var.set(data.get('gender', '男'))
        self.age_entry.delete(0, tk.END)
        self.age_entry.insert(0, data.get('age', ''))
        self.class_entry.delete(0, tk.END)
        self.class_entry.insert(0, data.get('class', ''))
        self.score_entry.delete(0, tk.END)
        self.score_entry.insert(0, data.get('score', ''))
    
    def clear_input(self):
        """清空输入框"""
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.gender_var.set('男')
        self.age_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)
        self.score_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
    
    def get_search_keyword(self):
        """获取搜索关键词"""
        return self.search_entry.get()
    
    def get_selected_item(self):
        """获取选中的行"""
        selected = self.tree.selection()
        if not selected:
            return None
        item = self.tree.item(selected[0])
        return item['values']
    
    def update_table(self, students):
        """更新表格数据"""
        # 清除所有选择
        self.tree.selection_remove(self.tree.selection())
        # 删除所有现有项目
        for item in self.tree.get_children():
            self.tree.delete(item)
        # 插入新数据
        for student in students:
            self.tree.insert('', tk.END, values=(
                student['id'], student['name'], student['gender'],
                student['age'], student['class'], student['score']
            ))
    
    def show_message(self, title, message, msg_type="info"):
        if msg_type == "error":
            messagebox.showerror(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)
    
    def logout(self):
        self.window.destroy()
        self.on_logout()
    
    def close(self):
        self.window.destroy()

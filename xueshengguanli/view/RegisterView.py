# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

class RegisterView:
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
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def create_widgets(self):
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
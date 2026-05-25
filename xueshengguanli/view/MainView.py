# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox

class MainView:
    def __init__(self, parent, on_logout):
        self.parent = parent
        self.on_logout = on_logout
        self.window = tk.Toplevel(parent)
        self.window.title("学生信息管理系统")
        self.window.geometry("1200x700")
        self.center_window()
        
        self.subjects = []
        self.score_entries = {}
        
        self.create_widgets()
    
    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def create_widgets(self):
        top_frame = tk.Frame(self.window, padx=10, pady=10)
        top_frame.pack(fill=tk.X)
        
        tk.Label(top_frame, text="学生信息管理系统", font=("微软雅黑", 18, "bold")).pack(side=tk.LEFT)
        tk.Button(top_frame, text="登出", font=("微软雅黑", 10), command=self.logout).pack(side=tk.RIGHT)
        
        main_paned = ttk.PanedWindow(self.window, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        left_frame = tk.Frame(main_paned, width=300)
        main_paned.add(left_frame, weight=1)
        
        right_frame = tk.Frame(main_paned, width=900)
        main_paned.add(right_frame, weight=3)
        
        self.create_subject_panel(left_frame)
        
        self.create_stats_panel(left_frame)
        
        self.create_student_panel(right_frame)
    
    def create_subject_panel(self, parent):
        subject_frame = tk.LabelFrame(parent, text="学科管理", font=("微软雅黑", 12), padx=10, pady=10)
        subject_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(subject_frame, text="学科名称：", font=("微软雅黑", 11)).grid(row=0, column=0, sticky=tk.W)
        self.subject_entry = tk.Entry(subject_frame, font=("微软雅黑", 11), width=15)
        self.subject_entry.grid(row=0, column=1, padx=5)
        
        button_frame = tk.Frame(subject_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.add_subject_btn = tk.Button(button_frame, text="新增学科", font=("微软雅黑", 10), width=8)
        self.add_subject_btn.pack(side=tk.LEFT, padx=2)
        
        self.delete_subject_btn = tk.Button(button_frame, text="删除学科", font=("微软雅黑", 10), width=8)
        self.delete_subject_btn.pack(side=tk.LEFT, padx=2)
        
        self.subject_listbox = tk.Listbox(subject_frame, font=("微软雅黑", 11), height=6)
        self.subject_listbox.grid(row=2, column=0, columnspan=2, sticky=tk.EW)
        
        subject_frame.grid_columnconfigure(0, weight=1)
        subject_frame.grid_columnconfigure(1, weight=1)
    
    def create_stats_panel(self, parent):
        stats_frame = tk.LabelFrame(parent, text="数据统计", font=("微软雅黑", 12), padx=10, pady=10)
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.total_count_label = tk.Label(stats_frame, text="总学生人数：0", font=("微软雅黑", 11))
        self.total_count_label.pack(anchor=tk.W, pady=2)
        
        self.class_dist_label = tk.Label(stats_frame, text="班级分布：", font=("微软雅黑", 11))
        self.class_dist_label.pack(anchor=tk.W, pady=2)
        
        self.class_dist_text = tk.Text(stats_frame, font=("微软雅黑", 10), height=4, width=30, state=tk.DISABLED)
        self.class_dist_text.pack(fill=tk.X, pady=2)
        
        self.subject_avg_label = tk.Label(stats_frame, text="学科平均分：", font=("微软雅黑", 11))
        self.subject_avg_label.pack(anchor=tk.W, pady=2)
        
        self.subject_avg_text = tk.Text(stats_frame, font=("微软雅黑", 10), height=6, width=30, state=tk.DISABLED)
        self.subject_avg_text.pack(fill=tk.X, pady=2)
    
    def create_student_panel(self, parent):
        input_frame = tk.LabelFrame(parent, text="学生信息", font=("微软雅黑", 12), padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=5)
        
        field_frame = tk.Frame(input_frame)
        field_frame.pack(fill=tk.X)
        
        tk.Label(field_frame, text="学号：", font=("微软雅黑", 11)).grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.id_entry = tk.Entry(field_frame, font=("微软雅黑", 11), width=12)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(field_frame, text="姓名：", font=("微软雅黑", 11)).grid(row=0, column=2, sticky=tk.E, padx=5, pady=5)
        self.name_entry = tk.Entry(field_frame, font=("微软雅黑", 11), width=12)
        self.name_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(field_frame, text="性别：", font=("微软雅黑", 11)).grid(row=0, column=4, sticky=tk.E, padx=5, pady=5)
        self.gender_var = tk.StringVar()
        self.gender_combo = ttk.Combobox(field_frame, textvariable=self.gender_var, font=("微软雅黑", 11), state="readonly", width=10)
        self.gender_combo['values'] = ("男", "女")
        self.gender_combo.current(0)
        self.gender_combo.grid(row=0, column=5, padx=5, pady=5)
        
        tk.Label(field_frame, text="年龄：", font=("微软雅黑", 11)).grid(row=0, column=6, sticky=tk.E, padx=5, pady=5)
        self.age_entry = tk.Entry(field_frame, font=("微软雅黑", 11), width=8)
        self.age_entry.grid(row=0, column=7, padx=5, pady=5)
        
        tk.Label(field_frame, text="班级：", font=("微软雅黑", 11)).grid(row=0, column=8, sticky=tk.E, padx=5, pady=5)
        self.class_entry = tk.Entry(field_frame, font=("微软雅黑", 11), width=12)
        self.class_entry.grid(row=0, column=9, padx=5, pady=5)
        
        self.scores_frame = tk.Frame(input_frame)
        self.scores_frame.pack(fill=tk.X, pady=5)
        
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
        
        table_frame = tk.Frame(parent, padx=10, pady=5)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(table_frame, columns=("id", "name", "gender", "age", "class"), show="headings", height=15)
        self.tree.heading("id", text="学号")
        self.tree.heading("name", text="姓名")
        self.tree.heading("gender", text="性别")
        self.tree.heading("age", text="年龄")
        self.tree.heading("class", text="班级")
        
        self.tree.column("id", width=100, anchor=tk.CENTER)
        self.tree.column("name", width=100, anchor=tk.CENTER)
        self.tree.column("gender", width=80, anchor=tk.CENTER)
        self.tree.column("age", width=80, anchor=tk.CENTER)
        self.tree.column("class", width=100, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def update_score_fields(self, subjects):
        self.subjects = subjects
        for widget in self.scores_frame.winfo_children():
            widget.destroy()
        
        self.score_entries = {}
        
        if subjects:
            tk.Label(self.scores_frame, text="学科成绩：", font=("微软雅黑", 11)).pack(side=tk.LEFT)
            for i, subject in enumerate(subjects):
                tk.Label(self.scores_frame, text=f"{subject}：", font=("微软雅黑", 11)).pack(side=tk.LEFT, padx=(5, 0))
                entry = tk.Entry(self.scores_frame, font=("微软雅黑", 11), width=8)
                entry.pack(side=tk.LEFT, padx=2)
                self.score_entries[subject] = entry
        else:
            tk.Label(self.scores_frame, text="请先在左侧添加学科", font=("微软雅黑", 11), fg="gray").pack(side=tk.LEFT)
    
    def update_table_columns(self, subjects):
        table_frame = self.tree.master
        self.tree.destroy()
        
        columns = ("id", "name", "gender", "age", "class") + tuple(subjects)
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("id", text="学号")
        self.tree.heading("name", text="姓名")
        self.tree.heading("gender", text="性别")
        self.tree.heading("age", text="年龄")
        self.tree.heading("class", text="班级")
        
        self.tree.column("id", width=100, anchor=tk.CENTER)
        self.tree.column("name", width=100, anchor=tk.CENTER)
        self.tree.column("gender", width=80, anchor=tk.CENTER)
        self.tree.column("age", width=80, anchor=tk.CENTER)
        self.tree.column("class", width=100, anchor=tk.CENTER)
        
        for subject in subjects:
            self.tree.heading(subject, text=subject)
            self.tree.column(subject, width=100, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
    
    def get_input_data(self):
        scores = {}
        for subject, entry in self.score_entries.items():
            scores[subject] = entry.get()
        
        return {
            'id': self.id_entry.get(),
            'name': self.name_entry.get(),
            'gender': self.gender_var.get(),
            'age': self.age_entry.get(),
            'class': self.class_entry.get(),
            'scores': scores
        }
    
    def set_input_data(self, data):
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, data.get('id', ''))
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, data.get('name', ''))
        self.gender_var.set(data.get('gender', '男'))
        self.age_entry.delete(0, tk.END)
        self.age_entry.insert(0, data.get('age', ''))
        self.class_entry.delete(0, tk.END)
        self.class_entry.insert(0, data.get('class', ''))
        
        scores = data.get('scores', {})
        for subject, entry in self.score_entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, scores.get(subject, ''))
    
    def clear_input(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.gender_var.set('男')
        self.age_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
        
        for entry in self.score_entries.values():
            entry.delete(0, tk.END)
    
    def get_search_keyword(self):
        return self.search_entry.get()
    
    def get_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            return None
        item = self.tree.item(selected[0])
        return item['values']
    
    def update_table(self, students):
        self.tree.selection_remove(self.tree.selection())
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        columns = list(self.tree["columns"])
        for student in students:
            values = [student.get(col, '') for col in columns[:5]]
            for subject in columns[5:]:
                values.append(student.get('scores', {}).get(subject, ''))
            self.tree.insert('', tk.END, values=values)
    
    def update_stats(self, total_count, class_dist, subject_avg):
        self.total_count_label.config(text=f"总学生人数：{total_count}")
        
        self.class_dist_text.config(state=tk.NORMAL)
        self.class_dist_text.delete(1.0, tk.END)
        if class_dist:
            for class_name, count in class_dist.items():
                self.class_dist_text.insert(tk.END, f"{class_name}: {count}人\n")
        else:
            self.class_dist_text.insert(tk.END, "暂无数据")
        self.class_dist_text.config(state=tk.DISABLED)
        
        self.subject_avg_text.config(state=tk.NORMAL)
        self.subject_avg_text.delete(1.0, tk.END)
        if subject_avg:
            for subject, avg in subject_avg.items():
                self.subject_avg_text.insert(tk.END, f"{subject}: {avg}分\n")
        else:
            self.subject_avg_text.insert(tk.END, "暂无数据")
        self.subject_avg_text.config(state=tk.DISABLED)
    
    def update_subject_list(self, subjects):
        self.subject_listbox.delete(0, tk.END)
        for subject in subjects:
            self.subject_listbox.insert(tk.END, subject)
    
    def get_selected_subject(self):
        selected = self.subject_listbox.curselection()
        if selected:
            return self.subject_listbox.get(selected[0])
        return None
    
    def get_new_subject_name(self):
        return self.subject_entry.get()
    
    def clear_subject_input(self):
        self.subject_entry.delete(0, tk.END)
    
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
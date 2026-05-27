import tkinter as tk
from tkinter import ttk, messagebox, Menu

class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("员工考勤管理系统")
        self.root.geometry("900x600")
        self.center_window()
        
        self.create_menu()
        self.create_widgets()
        
    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 600) // 2
        self.root.geometry(f"900x600+{x}+{y}")
        
    def create_menu(self):
        menubar = Menu(self.root)
        
        sys_menu = Menu(menubar, tearoff=0)
        sys_menu.add_command(label="退出", command=self.on_exit)
        menubar.add_cascade(label="系统", menu=sys_menu)
        
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.on_about)
        menubar.add_cascade(label="帮助", menu=help_menu)
        
        self.root.config(menu=menubar)
        
    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.left_frame = ttk.Frame(self.main_frame, width=150)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        self.emp_btn = ttk.Button(self.left_frame, text="员工管理", width=12)
        self.emp_btn.pack(pady=10)
        
        self.check_btn = ttk.Button(self.left_frame, text="考勤打卡", width=12)
        self.check_btn.pack(pady=10)
        
        self.query_btn = ttk.Button(self.left_frame, text="记录查询", width=12)
        self.query_btn.pack(pady=10)
        
        self.exit_btn = ttk.Button(self.left_frame, text="退出系统", width=12)
        self.exit_btn.pack(pady=10)
        
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.status_bar = ttk.Label(self.root, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def show_employee_panel(self):
        self.clear_right_frame()
        
        panel = ttk.Frame(self.right_frame)
        panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        top_frame = ttk.Frame(panel)
        top_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(top_frame, text="工号:").pack(side=tk.LEFT, padx=5)
        self.emp_id_entry = ttk.Entry(top_frame, width=15)
        self.emp_id_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(top_frame, text="姓名:").pack(side=tk.LEFT, padx=5)
        self.emp_name_entry = ttk.Entry(top_frame, width=15)
        self.emp_name_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(top_frame, text="部门:").pack(side=tk.LEFT, padx=5)
        self.emp_dept_entry = ttk.Entry(top_frame, width=15)
        self.emp_dept_entry.pack(side=tk.LEFT, padx=5)
        
        self.add_emp_btn = ttk.Button(top_frame, text="新增员工")
        self.add_emp_btn.pack(side=tk.LEFT, padx=10)
        
        self.del_emp_btn = ttk.Button(top_frame, text="删除员工")
        self.del_emp_btn.pack(side=tk.LEFT, padx=5)
        
        self.emp_tree = ttk.Treeview(panel, columns=('工号', '姓名', '部门'), show='headings')
        self.emp_tree.heading('工号', text='工号')
        self.emp_tree.heading('姓名', text='姓名')
        self.emp_tree.heading('部门', text='部门')
        self.emp_tree.column('工号', width=100)
        self.emp_tree.column('姓名', width=100)
        self.emp_tree.column('部门', width=150)
        
        scrollbar = ttk.Scrollbar(panel, orient=tk.VERTICAL, command=self.emp_tree.yview)
        self.emp_tree.configure(yscroll=scrollbar.set)
        
        self.emp_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def show_checkin_panel(self):
        self.clear_right_frame()
        
        panel = ttk.Frame(self.right_frame)
        panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        top_frame = ttk.Frame(panel)
        top_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(top_frame, text="工号:").pack(side=tk.LEFT, padx=5)
        self.check_id_entry = ttk.Entry(top_frame, width=20)
        self.check_id_entry.pack(side=tk.LEFT, padx=5)
        
        self.check_in_btn = ttk.Button(top_frame, text="签到", width=10)
        self.check_in_btn.pack(side=tk.LEFT, padx=20)
        
        self.check_out_btn = ttk.Button(top_frame, text="签退", width=10)
        self.check_out_btn.pack(side=tk.LEFT, padx=5)
        
        self.check_status = ttk.Label(panel, text="", font=('Arial', 14))
        self.check_status.pack(pady=20)
        
        info_frame = ttk.Frame(panel)
        info_frame.pack(fill=tk.X, pady=10)
        
        self.check_info = ttk.Label(info_frame, text="")
        self.check_info.pack()
        
    def show_query_panel(self):
        self.clear_right_frame()
        
        panel = ttk.Frame(self.right_frame)
        panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        top_frame = ttk.Frame(panel)
        top_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(top_frame, text="工号筛选:").pack(side=tk.LEFT, padx=5)
        self.query_id_entry = ttk.Entry(top_frame, width=15)
        self.query_id_entry.pack(side=tk.LEFT, padx=5)
        
        self.query_btn = ttk.Button(top_frame, text="查询")
        self.query_btn.pack(side=tk.LEFT, padx=10)
        
        self.reset_btn = ttk.Button(top_frame, text="重置")
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        self.att_tree = ttk.Treeview(panel, columns=('工号', '签到时间', '签退时间', '状态'), show='headings')
        self.att_tree.heading('工号', text='工号')
        self.att_tree.heading('签到时间', text='签到时间')
        self.att_tree.heading('签退时间', text='签退时间')
        self.att_tree.heading('状态', text='状态')
        self.att_tree.column('工号', width=100)
        self.att_tree.column('签到时间', width=150)
        self.att_tree.column('签退时间', width=150)
        self.att_tree.column('状态', width=80)
        
        scrollbar = ttk.Scrollbar(panel, orient=tk.VERTICAL, command=self.att_tree.yview)
        self.att_tree.configure(yscroll=scrollbar.set)
        
        self.att_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
    def set_status(self, text):
        self.status_bar.config(text=text)
        
    def show_message(self, title, message, type='info'):
        if type == 'error':
            messagebox.showerror(title, message)
        elif type == 'warning':
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)
            
    def on_exit(self):
        if messagebox.askyesno("退出", "确定要退出系统吗？"):
            self.root.quit()
            
    def on_about(self):
        messagebox.showinfo("关于", "员工考勤管理系统 V1.0\n\n基于 Python + Tkinter 开发")
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk, messagebox, Menu
import datetime
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'attendance.db')

def init_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            check_in_time TEXT,
            check_out_time TEXT,
            status TEXT DEFAULT '正常'
        )
    ''')
    conn.commit()
    conn.close()

class EmployeeDAO:
    def add_employee(self, emp_id, name, dept):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO employees (employee_id, name, department) VALUES (?, ?, ?)',
                          (emp_id, name, dept))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_all_employees(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM employees')
            return cursor.fetchall()
        finally:
            conn.close()
    
    def get_employee(self, emp_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM employees WHERE employee_id = ?', (emp_id,))
            return cursor.fetchone()
        finally:
            conn.close()
    
    def delete_employee(self, emp_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM employees WHERE employee_id = ?', (emp_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

class AttendanceDAO:
    def add_checkin(self, emp_id, check_in_time, status):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO attendance (employee_id, check_in_time, status) VALUES (?, ?, ?)',
                          (emp_id, check_in_time, status))
            conn.commit()
            return True
        finally:
            conn.close()
    
    def get_today_attendance(self, emp_id, today):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM attendance WHERE employee_id = ? AND check_in_time LIKE ?',
                          (emp_id, f'{today}%'))
            return cursor.fetchone()
        finally:
            conn.close()
    
    def update_checkout(self, attendance_id, check_out_time, status):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE attendance SET check_out_time = ?, status = ? WHERE id = ?',
                          (check_out_time, status, attendance_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def get_all_attendance(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM attendance ORDER BY check_in_time DESC')
            return cursor.fetchall()
        finally:
            conn.close()
    
    def get_attendance_by_emp_id(self, emp_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM attendance WHERE employee_id = ? ORDER BY check_in_time DESC',
                          (emp_id,))
            return cursor.fetchall()
        finally:
            conn.close()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("员工考勤管理系统")
        self.root.geometry("900x600")
        self.center_window()
        
        self.emp_dao = EmployeeDAO()
        self.att_dao = AttendanceDAO()
        
        self.create_menu()
        self.create_widgets()
        self.show_employee_panel()
    
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
        
        self.emp_btn = ttk.Button(self.left_frame, text="员工管理", width=12, command=self.show_employee_panel)
        self.emp_btn.pack(pady=10)
        
        self.check_btn = ttk.Button(self.left_frame, text="考勤打卡", width=12, command=self.show_checkin_panel)
        self.check_btn.pack(pady=10)
        
        self.query_btn = ttk.Button(self.left_frame, text="记录查询", width=12, command=self.show_query_panel)
        self.query_btn.pack(pady=10)
        
        self.exit_btn = ttk.Button(self.left_frame, text="退出系统", width=12, command=self.on_exit)
        self.exit_btn.pack(pady=10)
        
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.status_bar = ttk.Label(self.root, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
    
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
        
        self.add_emp_btn = ttk.Button(top_frame, text="新增员工", command=self.add_employee)
        self.add_emp_btn.pack(side=tk.LEFT, padx=10)
        
        self.del_emp_btn = ttk.Button(top_frame, text="删除员工", command=self.delete_employee)
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
        
        self.load_employees()
        self.status_bar.config(text="员工管理面板已打开")
    
    def add_employee(self):
        emp_id = self.emp_id_entry.get().strip()
        name = self.emp_name_entry.get().strip()
        dept = self.emp_dept_entry.get().strip()
        
        if not emp_id or not name or not dept:
            messagebox.showwarning("警告", "请填写完整信息")
            return
        
        if self.emp_dao.add_employee(emp_id, name, dept):
            messagebox.showinfo("成功", "员工添加成功")
            self.emp_id_entry.delete(0, 'end')
            self.emp_name_entry.delete(0, 'end')
            self.emp_dept_entry.delete(0, 'end')
            self.load_employees()
            self.status_bar.config(text=f"员工 {name} 添加成功")
        else:
            messagebox.showerror("错误", "工号已存在")
            self.status_bar.config(text="员工添加失败，工号重复")
    
    def delete_employee(self):
        selected = self.emp_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请选择要删除的员工")
            return
        
        item = self.emp_tree.item(selected[0])
        emp_id = item['values'][0]
        name = item['values'][1]
        
        if self.emp_dao.delete_employee(emp_id):
            messagebox.showinfo("成功", "员工删除成功")
            self.load_employees()
            self.status_bar.config(text=f"员工 {name} 删除成功")
        else:
            messagebox.showerror("错误", "删除失败")
    
    def load_employees(self):
        for item in self.emp_tree.get_children():
            self.emp_tree.delete(item)
        
        employees = self.emp_dao.get_all_employees()
        for emp in employees:
            self.emp_tree.insert('', 'end', values=(emp[1], emp[2], emp[3]))
    
    def show_checkin_panel(self):
        self.clear_right_frame()
        
        panel = ttk.Frame(self.right_frame)
        panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        top_frame = ttk.Frame(panel)
        top_frame.pack(fill=tk.X, pady=20)
        
        ttk.Label(top_frame, text="工号:").pack(side=tk.LEFT, padx=5)
        self.check_id_entry = ttk.Entry(top_frame, width=20)
        self.check_id_entry.pack(side=tk.LEFT, padx=5)
        
        self.check_in_btn = ttk.Button(top_frame, text="签到", width=10, command=self.check_in)
        self.check_in_btn.pack(side=tk.LEFT, padx=20)
        
        self.check_out_btn = ttk.Button(top_frame, text="签退", width=10, command=self.check_out)
        self.check_out_btn.pack(side=tk.LEFT, padx=5)
        
        self.check_status = ttk.Label(panel, text="", font=('Arial', 14))
        self.check_status.pack(pady=20)
        
        info_frame = ttk.Frame(panel)
        info_frame.pack(fill=tk.X, pady=10)
        
        self.check_info = ttk.Label(info_frame, text="")
        self.check_info.pack()
        
        self.status_bar.config(text="考勤打卡面板已打开")
    
    def check_in(self):
        emp_id = self.check_id_entry.get().strip()
        
        if not emp_id:
            messagebox.showwarning("警告", "请输入工号")
            return
        
        employee = self.emp_dao.get_employee(emp_id)
        if not employee:
            messagebox.showerror("错误", "工号不存在")
            return
        
        today = datetime.date.today().strftime('%Y-%m-%d')
        today_attendance = self.att_dao.get_today_attendance(emp_id, today)
        
        if today_attendance and today_attendance[2]:
            messagebox.showwarning("警告", "今日已签到")
            self.check_status.config(text=f"今日已签到: {today_attendance[2]}")
            return
        
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        check_in_time = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        work_start = check_in_time.replace(hour=9, minute=0, second=0)
        status = '迟到' if check_in_time > work_start else '正常'
        
        self.att_dao.add_checkin(emp_id, now, status)
        
        self.check_status.config(text="签到成功!", foreground='green')
        self.check_info.config(text=f"工号: {emp_id} | 姓名: {employee[2]} | 签到时间: {now} | 状态: {status}")
        self.status_bar.config(text=f"员工 {employee[2]} 已签到")
    
    def check_out(self):
        emp_id = self.check_id_entry.get().strip()
        
        if not emp_id:
            messagebox.showwarning("警告", "请输入工号")
            return
        
        employee = self.emp_dao.get_employee(emp_id)
        if not employee:
            messagebox.showerror("错误", "工号不存在")
            return
        
        today = datetime.date.today().strftime('%Y-%m-%d')
        today_attendance = self.att_dao.get_today_attendance(emp_id, today)
        
        if not today_attendance or not today_attendance[2]:
            messagebox.showwarning("警告", "今日未签到")
            return
        
        if today_attendance[3]:
            messagebox.showwarning("警告", "今日已签退")
            self.check_status.config(text=f"今日已签退: {today_attendance[3]}")
            return
        
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        check_out_time = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        work_end = check_out_time.replace(hour=18, minute=0, second=0)
        
        status = today_attendance[4]
        if check_out_time < work_end:
            status = '早退'
        
        self.att_dao.update_checkout(today_attendance[0], now, status)
        
        self.check_status.config(text="签退成功!", foreground='green')
        self.check_info.config(text=f"工号: {emp_id} | 姓名: {employee[2]} | 签退时间: {now} | 状态: {status}")
        self.status_bar.config(text=f"员工 {employee[2]} 已签退")
    
    def show_query_panel(self):
        self.clear_right_frame()
        
        panel = ttk.Frame(self.right_frame)
        panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        top_frame = ttk.Frame(panel)
        top_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(top_frame, text="工号筛选:").pack(side=tk.LEFT, padx=5)
        self.query_id_entry = ttk.Entry(top_frame, width=15)
        self.query_id_entry.pack(side=tk.LEFT, padx=5)
        
        self.query_btn = ttk.Button(top_frame, text="查询", command=self.query_attendance)
        self.query_btn.pack(side=tk.LEFT, padx=10)
        
        self.reset_btn = ttk.Button(top_frame, text="重置", command=self.reset_query)
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
        
        self.load_all_attendance()
        self.status_bar.config(text="记录查询面板已打开")
    
    def query_attendance(self):
        emp_id = self.query_id_entry.get().strip()
        
        for item in self.att_tree.get_children():
            self.att_tree.delete(item)
        
        if emp_id:
            records = self.att_dao.get_attendance_by_emp_id(emp_id)
        else:
            records = self.att_dao.get_all_attendance()
        
        for record in records:
            self.att_tree.insert('', 'end', values=(
                record[1],
                record[2] if record[2] else '-',
                record[3] if record[3] else '-',
                record[4]
            ))
        
        self.status_bar.config(text=f"查询到 {len(records)} 条记录")
    
    def reset_query(self):
        self.query_id_entry.delete(0, 'end')
        self.load_all_attendance()
    
    def load_all_attendance(self):
        for item in self.att_tree.get_children():
            self.att_tree.delete(item)
        
        records = self.att_dao.get_all_attendance()
        for record in records:
            self.att_tree.insert('', 'end', values=(
                record[1],
                record[2] if record[2] else '-',
                record[3] if record[3] else '-',
                record[4]
            ))
    
    def on_exit(self):
        if messagebox.askyesno("退出", "确定要退出系统吗？"):
            self.root.quit()
    
    def on_about(self):
        messagebox.showinfo("关于", "员工考勤管理系统 V1.0\n\n基于 Python + Tkinter 开发")

def main():
    init_database()
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
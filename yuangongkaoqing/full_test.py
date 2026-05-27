import os
os.chdir('d:/trae/pythongame/yuangongkaoqing')

import tkinter as tk
from tkinter import ttk, messagebox

print("Testing full application flow...")

try:
    from database.db_init import init_database, DB_PATH
    print(f"DB_PATH: {DB_PATH}")
    init_database()
    print("Database initialized")
except Exception as e:
    print(f"DB init error: {e}")

try:
    from model.employee import Employee
    from dao.employee_dao import EmployeeDAO
    
    dao = EmployeeDAO()
    
    def on_add():
        emp_id = emp_id_entry.get().strip()
        name = name_entry.get().strip()
        dept = dept_entry.get().strip()
        
        print(f"Add clicked: emp_id='{emp_id}', name='{name}', dept='{dept}'")
        
        if not emp_id or not name or not dept:
            messagebox.showwarning("警告", "请填写完整信息")
            return
            
        try:
            employee = Employee(emp_id, name, dept)
            print(f"Employee object: {employee.to_dict()}")
            
            result = dao.add_employee(employee)
            print(f"Add result: {result}")
            
            if result:
                messagebox.showinfo("成功", "员工添加成功")
                emp_id_entry.delete(0, 'end')
                name_entry.delete(0, 'end')
                dept_entry.delete(0, 'end')
                refresh_list()
            else:
                messagebox.showerror("错误", "工号已存在")
        except Exception as e:
            print(f"Error in add: {e}")
            messagebox.showerror("错误", f"添加失败: {e}")
    
    def refresh_list():
        for item in tree.get_children():
            tree.delete(item)
        employees = dao.get_all_employees()
        print(f"Loaded {len(employees)} employees")
        for emp in employees:
            tree.insert('', 'end', values=(emp.employee_id, emp.name, emp.department))
    
    root = tk.Tk()
    root.title("完整测试 - 员工管理")
    root.geometry("600x400")
    
    main_frame = ttk.Frame(root, padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(fill=tk.X, pady=5)
    
    ttk.Label(input_frame, text="工号:").pack(side=tk.LEFT, padx=5)
    emp_id_entry = ttk.Entry(input_frame, width=15)
    emp_id_entry.pack(side=tk.LEFT, padx=5)
    
    ttk.Label(input_frame, text="姓名:").pack(side=tk.LEFT, padx=5)
    name_entry = ttk.Entry(input_frame, width=15)
    name_entry.pack(side=tk.LEFT, padx=5)
    
    ttk.Label(input_frame, text="部门:").pack(side=tk.LEFT, padx=5)
    dept_entry = ttk.Entry(input_frame, width=15)
    dept_entry.pack(side=tk.LEFT, padx=5)
    
    add_btn = ttk.Button(input_frame, text="新增员工", command=on_add)
    add_btn.pack(side=tk.LEFT, padx=10)
    
    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    
    tree = ttk.Treeview(tree_frame, columns=('工号', '姓名', '部门'), show='headings')
    tree.heading('工号', text='工号')
    tree.heading('姓名', text='姓名')
    tree.heading('部门', text='部门')
    tree.column('工号', width=100)
    tree.column('姓名', width=100)
    tree.column('部门', width=150)
    
    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    refresh_list()
    
    print("GUI created successfully, running mainloop...")
    root.mainloop()
    
except Exception as e:
    print(f"Fatal error: {e}")
    import traceback
    traceback.print_exc()
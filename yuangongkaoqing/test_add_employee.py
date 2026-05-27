import os
os.chdir('d:/trae/pythongame/yuangongkaoqing')

import tkinter as tk
from tkinter import ttk, messagebox

def test_add_employee():
    root = tk.Tk()
    root.title("Test Add Employee")
    root.geometry("400x200")
    
    def on_add():
        emp_id = emp_id_entry.get().strip()
        name = name_entry.get().strip()
        dept = dept_entry.get().strip()
        
        print(f"Input values: emp_id='{emp_id}', name='{name}', dept='{dept}'")
        
        if not emp_id or not name or not dept:
            messagebox.showwarning("警告", "请填写完整信息")
            return
            
        try:
            from model.employee import Employee
            from dao.employee_dao import EmployeeDAO
            
            employee = Employee(emp_id, name, dept)
            dao = EmployeeDAO()
            
            if dao.add_employee(employee):
                messagebox.showinfo("成功", "员工添加成功")
                emp_id_entry.delete(0, 'end')
                name_entry.delete(0, 'end')
                dept_entry.delete(0, 'end')
            else:
                messagebox.showerror("错误", "工号已存在")
        except Exception as e:
            print(f"Error: {str(e)}")
            messagebox.showerror("错误", f"添加失败: {str(e)}")
    
    frame = ttk.Frame(root, padding=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(frame, text="工号:").grid(row=0, column=0, padx=5, pady=5)
    emp_id_entry = ttk.Entry(frame, width=20)
    emp_id_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(frame, text="姓名:").grid(row=1, column=0, padx=5, pady=5)
    name_entry = ttk.Entry(frame, width=20)
    name_entry.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(frame, text="部门:").grid(row=2, column=0, padx=5, pady=5)
    dept_entry = ttk.Entry(frame, width=20)
    dept_entry.grid(row=2, column=1, padx=5, pady=5)
    
    add_btn = ttk.Button(frame, text="新增员工", command=on_add)
    add_btn.grid(row=3, column=0, columnspan=2, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    test_add_employee()
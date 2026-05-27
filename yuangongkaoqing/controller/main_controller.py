import datetime
from model.employee import Employee
from model.attendance import Attendance
from dao.employee_dao import EmployeeDAO
from dao.attendance_dao import AttendanceDAO

class MainController:
    def __init__(self, view):
        self.view = view
        self.emp_dao = EmployeeDAO()
        self.att_dao = AttendanceDAO()
        self.bind_events()
        
    def bind_events(self):
        self.view.emp_btn.config(command=self.show_employee_panel)
        self.view.check_btn.config(command=self.show_checkin_panel)
        self.view.query_btn.config(command=self.show_query_panel)
        self.view.exit_btn.config(command=self.view.on_exit)
        
    def show_employee_panel(self):
        self.view.show_employee_panel()
        self.view.add_emp_btn.config(command=self.add_employee)
        self.view.del_emp_btn.config(command=self.delete_employee)
        self.load_employees()
        self.view.set_status("员工管理面板已打开")
        
    def show_checkin_panel(self):
        self.view.show_checkin_panel()
        self.view.check_in_btn.config(command=self.check_in)
        self.view.check_out_btn.config(command=self.check_out)
        self.view.set_status("考勤打卡面板已打开")
        
    def show_query_panel(self):
        self.view.show_query_panel()
        self.view.query_btn.config(command=self.query_attendance)
        self.view.reset_btn.config(command=self.reset_query)
        self.load_all_attendance()
        self.view.set_status("记录查询面板已打开")
        
    def add_employee(self):
        emp_id = self.view.emp_id_entry.get().strip()
        name = self.view.emp_name_entry.get().strip()
        dept = self.view.emp_dept_entry.get().strip()
        
        if not emp_id or not name or not dept:
            self.view.show_message("警告", "请填写完整信息", 'warning')
            return
            
        employee = Employee(emp_id, name, dept)
        
        if self.emp_dao.add_employee(employee):
            self.view.show_message("成功", "员工添加成功")
            self.load_employees()
            self.view.emp_id_entry.delete(0, 'end')
            self.view.emp_name_entry.delete(0, 'end')
            self.view.emp_dept_entry.delete(0, 'end')
            self.view.set_status(f"员工 {name} 添加成功")
        else:
            self.view.show_message("错误", "工号已存在", 'error')
            self.view.set_status("员工添加失败，工号重复")
            
    def delete_employee(self):
        selected = self.view.emp_tree.selection()
        if not selected:
            self.view.show_message("警告", "请选择要删除的员工", 'warning')
            return
            
        item = self.view.emp_tree.item(selected[0])
        emp_id = item['values'][0]
        name = item['values'][1]
        
        if self.emp_dao.delete_employee(emp_id):
            self.view.show_message("成功", "员工删除成功")
            self.load_employees()
            self.view.set_status(f"员工 {name} 删除成功")
        else:
            self.view.show_message("错误", "删除失败", 'error')
            
    def load_employees(self):
        for item in self.view.emp_tree.get_children():
            self.view.emp_tree.delete(item)
            
        employees = self.emp_dao.get_all_employees()
        for emp in employees:
            self.view.emp_tree.insert('', 'end', values=(emp.employee_id, emp.name, emp.department))
            
    def check_in(self):
        emp_id = self.view.check_id_entry.get().strip()
        
        if not emp_id:
            self.view.show_message("警告", "请输入工号", 'warning')
            return
            
        employee = self.emp_dao.get_employee_by_id(emp_id)
        if not employee:
            self.view.show_message("错误", "工号不存在", 'error')
            return
            
        today = datetime.date.today().strftime('%Y-%m-%d')
        today_attendance = self.att_dao.get_today_attendance(emp_id, today)
        
        if today_attendance and today_attendance.check_in_time:
            self.view.show_message("警告", "今日已签到", 'warning')
            self.view.check_status.config(text=f"今日已签到: {today_attendance.check_in_time}")
            return
            
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        check_in_time = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        work_start = check_in_time.replace(hour=9, minute=0, second=0)
        
        status = '迟到' if check_in_time > work_start else '正常'
        
        attendance = Attendance(emp_id, now, None, status)
        self.att_dao.add_attendance(attendance)
        
        self.view.check_status.config(text=f"签到成功!", foreground='green')
        self.view.check_info.config(text=f"工号: {emp_id} | 姓名: {employee.name} | 签到时间: {now} | 状态: {status}")
        self.view.set_status(f"员工 {employee.name} 已签到")
        
    def check_out(self):
        emp_id = self.view.check_id_entry.get().strip()
        
        if not emp_id:
            self.view.show_message("警告", "请输入工号", 'warning')
            return
            
        employee = self.emp_dao.get_employee_by_id(emp_id)
        if not employee:
            self.view.show_message("错误", "工号不存在", 'error')
            return
            
        today = datetime.date.today().strftime('%Y-%m-%d')
        today_attendance = self.att_dao.get_today_attendance(emp_id, today)
        
        if not today_attendance or not today_attendance.check_in_time:
            self.view.show_message("警告", "今日未签到", 'warning')
            return
            
        if today_attendance.check_out_time:
            self.view.show_message("警告", "今日已签退", 'warning')
            self.view.check_status.config(text=f"今日已签退: {today_attendance.check_out_time}")
            return
            
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        check_out_time = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        work_end = check_out_time.replace(hour=18, minute=0, second=0)
        
        status = today_attendance.status
        if check_out_time < work_end:
            status = '早退'
            
        today_attendance.check_out_time = now
        today_attendance.status = status
        self.att_dao.update_attendance(today_attendance)
        
        self.view.check_status.config(text=f"签退成功!", foreground='green')
        self.view.check_info.config(text=f"工号: {emp_id} | 姓名: {employee.name} | 签退时间: {now} | 状态: {status}")
        self.view.set_status(f"员工 {employee.name} 已签退")
        
    def query_attendance(self):
        emp_id = self.view.query_id_entry.get().strip()
        
        for item in self.view.att_tree.get_children():
            self.view.att_tree.delete(item)
            
        if emp_id:
            records = self.att_dao.get_attendance_by_employee_id(emp_id)
        else:
            records = self.att_dao.get_all_attendance()
            
        for record in records:
            self.view.att_tree.insert('', 'end', values=(
                record.employee_id,
                record.check_in_time if record.check_in_time else '-',
                record.check_out_time if record.check_out_time else '-',
                record.status
            ))
            
        self.view.set_status(f"查询到 {len(records)} 条记录")
        
    def reset_query(self):
        self.view.query_id_entry.delete(0, 'end')
        self.load_all_attendance()
        
    def load_all_attendance(self):
        for item in self.view.att_tree.get_children():
            self.view.att_tree.delete(item)
            
        records = self.att_dao.get_all_attendance()
        for record in records:
            self.view.att_tree.insert('', 'end', values=(
                record.employee_id,
                record.check_in_time if record.check_in_time else '-',
                record.check_out_time if record.check_out_time else '-',
                record.status
            ))
import datetime
import os
import shutil
from model.employee import Employee
from model.attendance import Attendance
from dao.employee_dao import EmployeeDAO
from dao.attendance_dao import AttendanceDAO
from dao.log_dao import LogDAO

class MainController:
    WORK_START = datetime.time(9, 0, 0)
    WORK_END = datetime.time(18, 0, 0)
    LATE_THRESHOLD = 30
    EARLY_LEAVE_THRESHOLD = 30
    
    def __init__(self, view):
        self.view = view
        self.emp_dao = EmployeeDAO()
        self.att_dao = AttendanceDAO()
        self.log_dao = LogDAO()
        self.bind_events()
        self.load_employees()
        self.load_attendance()
        self.update_today_stats()
        self.update_department_combo()
        
    def bind_events(self):
        self.view.search_emp_btn.config(command=self.search_employees)
        self.view.reset_emp_btn.config(command=self.reset_employee_search)
        self.view.add_emp_btn.config(command=self.add_employee)
        self.view.modify_emp_btn.config(command=self.modify_employee)
        self.view.del_emp_btn.config(command=self.delete_employee)
        self.view.emp_tree.bind('<Double-1>', self.on_emp_tree_double_click)
        
        self.view.check_in_btn.config(command=self.check_in)
        self.view.check_out_btn.config(command=self.check_out)
        self.view.apply_leave_btn.config(command=self.apply_leave)
        
        self.view.search_att_btn.config(command=self.search_attendance)
        self.view.reset_att_btn.config(command=self.reset_attendance_search)
        
        self.view.personal_stat_btn.config(command=self.get_personal_statistics)
        self.view.department_stat_btn.config(command=self.get_department_statistics)
        
        self.view.on_backup = self.backup_database
        self.view.on_clear_data = self.clear_all_data
        self.view.on_logs = self.show_logs
        
    def load_employees(self):
        for item in self.view.emp_tree.get_children():
            self.view.emp_tree.delete(item)
        
        employees = self.emp_dao.get_all_employees()
        for emp in employees:
            self.view.emp_tree.insert('', 'end', values=(
                emp.employee_id, emp.name, emp.department, emp.position,
                emp.phone, emp.email, emp.hire_date, emp.status
            ))
        
        self.view.set_status(f"已加载 {len(employees)} 名员工")
        
    def search_employees(self):
        emp_id = self.view.emp_id_entry.get().strip()
        name = self.view.emp_name_entry.get().strip()
        department = self.view.emp_dept_combo.get()
        
        for item in self.view.emp_tree.get_children():
            self.view.emp_tree.delete(item)
        
        employees = self.emp_dao.search_employees(emp_id, name, department)
        for emp in employees:
            self.view.emp_tree.insert('', 'end', values=(
                emp.employee_id, emp.name, emp.department, emp.position,
                emp.phone, emp.email, emp.hire_date, emp.status
            ))
        
        self.view.set_status(f"查询到 {len(employees)} 名员工")
        
    def reset_employee_search(self):
        self.view.emp_id_entry.delete(0, 'end')
        self.view.emp_name_entry.delete(0, 'end')
        self.view.emp_dept_combo.set('')
        self.load_employees()
        
    def add_employee(self):
        emp_id = self.view.emp_form_entries['emp_id_form'].get().strip()
        name = self.view.emp_form_entries['emp_name_form'].get().strip()
        department = self.view.emp_form_entries['emp_dept_form'].get().strip()
        position = self.view.emp_form_entries['emp_pos_form'].get().strip()
        phone = self.view.emp_form_entries['emp_phone_form'].get().strip()
        email = self.view.emp_form_entries['emp_email_form'].get().strip()
        hire_date = self.view.emp_form_entries['emp_hire_form'].get().strip()
        status = self.view.emp_form_entries['emp_status_combo'].get() or '在职'
        
        if not emp_id or not name or not department:
            self.view.show_message("警告", "请填写工号、姓名和部门", 'warning')
            return
        
        employee = Employee(emp_id, name, department, position, phone, email, hire_date, status)
        
        if self.emp_dao.add_employee(employee):
            self.view.show_message("成功", "员工添加成功")
            self.log_dao.add_log("管理员", "新增员工", emp_id)
            self.load_employees()
            self.clear_emp_form()
            self.view.set_status(f"员工 {name} 添加成功")
        else:
            self.view.show_message("错误", "工号已存在", 'error')
            self.log_dao.add_log("管理员", "新增员工失败", emp_id, "FAILED")
            
    def modify_employee(self):
        selected = self.view.emp_tree.selection()
        if not selected:
            self.view.show_message("警告", "请选择要修改的员工", 'warning')
            return
        
        item = self.view.emp_tree.item(selected[0])
        emp_id = item['values'][0]
        
        name = self.view.emp_form_entries['emp_name_form'].get().strip()
        department = self.view.emp_form_entries['emp_dept_form'].get().strip()
        position = self.view.emp_form_entries['emp_pos_form'].get().strip()
        phone = self.view.emp_form_entries['emp_phone_form'].get().strip()
        email = self.view.emp_form_entries['emp_email_form'].get().strip()
        hire_date = self.view.emp_form_entries['emp_hire_form'].get().strip()
        status = self.view.emp_form_entries['emp_status_combo'].get() or '在职'
        
        if not name or not department:
            self.view.show_message("警告", "请填写姓名和部门", 'warning')
            return
        
        employee = Employee(emp_id, name, department, position, phone, email, hire_date, status)
        
        if self.emp_dao.update_employee(employee):
            self.view.show_message("成功", "员工信息修改成功")
            self.log_dao.add_log("管理员", "修改员工", emp_id)
            self.load_employees()
            self.clear_emp_form()
            self.view.set_status(f"员工 {name} 信息已更新")
        else:
            self.view.show_message("错误", "修改失败", 'error')
            
    def delete_employee(self):
        selected = self.view.emp_tree.selection()
        if not selected:
            self.view.show_message("警告", "请选择要删除的员工", 'warning')
            return
        
        item = self.view.emp_tree.item(selected[0])
        emp_id = item['values'][0]
        name = item['values'][1]
        
        if not self.view.show_confirm("确认删除", f"确定要删除员工 {name} ({emp_id}) 吗？"):
            return
        
        if self.emp_dao.delete_employee(emp_id):
            self.view.show_message("成功", "员工删除成功")
            self.log_dao.add_log("管理员", "删除员工", emp_id)
            self.load_employees()
            self.clear_emp_form()
            self.view.set_status(f"员工 {name} 已删除")
        else:
            self.view.show_message("错误", "删除失败", 'error')
            
    def on_emp_tree_double_click(self, event):
        selected = self.view.emp_tree.selection()
        if selected:
            item = self.view.emp_tree.item(selected[0])
            values = item['values']
            self.view.emp_form_entries['emp_id_form'].delete(0, 'end')
            self.view.emp_form_entries['emp_id_form'].insert(0, values[0])
            self.view.emp_form_entries['emp_id_form'].config(state='disabled')
            
            self.view.emp_form_entries['emp_name_form'].delete(0, 'end')
            self.view.emp_form_entries['emp_name_form'].insert(0, values[1])
            
            self.view.emp_form_entries['emp_dept_form'].delete(0, 'end')
            self.view.emp_form_entries['emp_dept_form'].insert(0, values[2])
            
            self.view.emp_form_entries['emp_pos_form'].delete(0, 'end')
            self.view.emp_form_entries['emp_pos_form'].insert(0, values[3])
            
            self.view.emp_form_entries['emp_phone_form'].delete(0, 'end')
            self.view.emp_form_entries['emp_phone_form'].insert(0, values[4])
            
            self.view.emp_form_entries['emp_email_form'].delete(0, 'end')
            self.view.emp_form_entries['emp_email_form'].insert(0, values[5])
            
            self.view.emp_form_entries['emp_hire_form'].delete(0, 'end')
            self.view.emp_form_entries['emp_hire_form'].insert(0, values[6])
            
            self.view.emp_form_entries['emp_status_combo'].set(values[7])
            
    def clear_emp_form(self):
        self.view.emp_form_entries['emp_id_form'].config(state='normal')
        for key in self.view.emp_form_entries:
            if key == 'emp_status_combo':
                self.view.emp_form_entries[key].set('')
            else:
                self.view.emp_form_entries[key].delete(0, 'end')
                
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
            self.view.check_status_label.config(text=f"今日已签到: {today_attendance.check_in_time}", foreground='orange')
            return
        
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        
        check_in_time = now.time()
        status = '正常'
        
        if check_in_time > self.WORK_START:
            delta = datetime.datetime.combine(datetime.date.today(), check_in_time) - \
                    datetime.datetime.combine(datetime.date.today(), self.WORK_START)
            if delta.total_seconds() / 60 > self.LATE_THRESHOLD:
                status = '迟到'
        
        attendance = Attendance(emp_id, now_str, None, status)
        self.att_dao.add_attendance(attendance)
        
        self.view.check_status_label.config(text="签到成功!", foreground='green')
        info_text = f"工号: {emp_id}\n姓名: {employee.name}\n部门: {employee.department}\n签到时间: {now_str}\n状态: {status}"
        self.view.check_info_text.config(state=tk.NORMAL)
        self.view.check_info_text.delete(1.0, tk.END)
        self.view.check_info_text.insert(tk.END, info_text)
        self.view.check_info_text.config(state=tk.DISABLED)
        
        self.log_dao.add_log("系统", "签到", emp_id)
        self.load_attendance()
        self.update_today_stats()
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
            self.view.check_status_label.config(text=f"今日已签退: {today_attendance.check_out_time}", foreground='orange')
            return
        
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        
        check_out_time = now.time()
        status = today_attendance.status
        
        if check_out_time < self.WORK_END:
            delta = datetime.datetime.combine(datetime.date.today(), self.WORK_END) - \
                    datetime.datetime.combine(datetime.date.today(), check_out_time)
            if delta.total_seconds() / 60 > self.EARLY_LEAVE_THRESHOLD:
                status = '早退'
        
        check_in_dt = datetime.datetime.strptime(today_attendance.check_in_time, '%Y-%m-%d %H:%M:%S')
        check_out_dt = now
        work_hours = (check_out_dt - check_in_dt).total_seconds() / 3600
        
        overtime_hours = 0.0
        if check_out_time > self.WORK_END:
            overtime_start = datetime.datetime.combine(datetime.date.today(), self.WORK_END)
            overtime_hours = (check_out_dt - overtime_start).total_seconds() / 3600
            if status == '正常':
                status = '加班'
        
        today_attendance.check_out_time = now_str
        today_attendance.status = status
        today_attendance.work_hours = round(work_hours, 2)
        today_attendance.overtime_hours = round(overtime_hours, 2)
        self.att_dao.update_attendance(today_attendance)
        
        self.view.check_status_label.config(text="签退成功!", foreground='green')
        info_text = f"工号: {emp_id}\n姓名: {employee.name}\n签退时间: {now_str}\n状态: {status}\n工作时长: {work_hours:.2f}小时\n加班时长: {overtime_hours:.2f}小时"
        self.view.check_info_text.config(state=tk.NORMAL)
        self.view.check_info_text.delete(1.0, tk.END)
        self.view.check_info_text.insert(tk.END, info_text)
        self.view.check_info_text.config(state=tk.DISABLED)
        
        self.log_dao.add_log("系统", "签退", emp_id)
        self.load_attendance()
        self.update_today_stats()
        self.view.set_status(f"员工 {employee.name} 已签退")
        
    def apply_leave(self):
        emp_id = self.view.check_id_entry.get().strip()
        
        if not emp_id:
            self.view.show_message("警告", "请输入工号", 'warning')
            return
        
        employee = self.emp_dao.get_employee_by_id(emp_id)
        if not employee:
            self.view.show_message("错误", "工号不存在", 'error')
            return
        
        leave_type = self.view.leave_type_combo.get()
        if not leave_type:
            self.view.show_message("警告", "请选择请假类型", 'warning')
            return
        
        today = datetime.date.today().strftime('%Y-%m-%d')
        today_attendance = self.att_dao.get_today_attendance(emp_id, today)
        
        if today_attendance:
            self.view.show_message("警告", "今日已有考勤记录", 'warning')
            return
        
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        attendance = Attendance(emp_id, now, now, '请假', leave_type)
        self.att_dao.add_attendance(attendance)
        
        self.view.show_message("成功", f"{leave_type}申请成功")
        self.log_dao.add_log("系统", "请假申请", f"{emp_id}-{leave_type}")
        self.load_attendance()
        self.update_today_stats()
        self.view.set_status(f"员工 {employee.name} {leave_type}申请成功")
        
    def load_attendance(self):
        for item in self.view.att_tree.get_children():
            self.view.att_tree.delete(item)
        
        records = self.att_dao.get_all_attendance()
        for record in records:
            employee = self.emp_dao.get_employee_by_id(record.employee_id)
            name = employee.name if employee else '未知'
            
            values = (
                record.employee_id,
                name,
                record.check_in_time if record.check_in_time else '-',
                record.check_out_time if record.check_out_time else '-',
                record.status,
                record.leave_type if record.leave_type else '-',
                f"{record.work_hours:.2f}" if record.work_hours else '-',
                f"{record.overtime_hours:.2f}" if record.overtime_hours else '-'
            )
            
            item_id = self.view.att_tree.insert('', 'end', values=values)
            
            if record.status in ['迟到', '早退', '缺勤']:
                self.view.att_tree.tag_configure('warning', foreground='#E74C3C')
                self.view.att_tree.item(item_id, tags=('warning',))
            elif record.status == '请假':
                self.view.att_tree.tag_configure('info', foreground='#1ABC9C')
                self.view.att_tree.item(item_id, tags=('info',))
            elif record.status == '加班':
                self.view.att_tree.tag_configure('success', foreground='#3498DB')
                self.view.att_tree.item(item_id, tags=('success',))
        
        self.view.set_status(f"已加载 {len(records)} 条考勤记录")
        
    def search_attendance(self):
        emp_id = self.view.att_emp_id_entry.get().strip()
        start_date = self.view.att_start_date.get().strip()
        end_date = self.view.att_end_date.get().strip()
        status = self.view.att_status_combo.get()
        
        if not start_date or not end_date:
            self.view.show_message("警告", "请选择日期范围", 'warning')
            return
        
        try:
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            self.view.show_message("警告", "日期格式错误", 'warning')
            return
        
        for item in self.view.att_tree.get_children():
            self.view.att_tree.delete(item)
        
        records = self.att_dao.get_attendance_by_date_range(start_date, end_date, emp_id)
        
        if status != '全部':
            records = [r for r in records if r.status == status]
        
        for record in records:
            employee = self.emp_dao.get_employee_by_id(record.employee_id)
            name = employee.name if employee else '未知'
            
            values = (
                record.employee_id,
                name,
                record.check_in_time if record.check_in_time else '-',
                record.check_out_time if record.check_out_time else '-',
                record.status,
                record.leave_type if record.leave_type else '-',
                f"{record.work_hours:.2f}" if record.work_hours else '-',
                f"{record.overtime_hours:.2f}" if record.overtime_hours else '-'
            )
            
            item_id = self.view.att_tree.insert('', 'end', values=values)
            
            if record.status in ['迟到', '早退', '缺勤']:
                self.view.att_tree.tag_configure('warning', foreground='#E74C3C')
                self.view.att_tree.item(item_id, tags=('warning',))
            elif record.status == '请假':
                self.view.att_tree.tag_configure('info', foreground='#1ABC9C')
                self.view.att_tree.item(item_id, tags=('info',))
            elif record.status == '加班':
                self.view.att_tree.tag_configure('success', foreground='#3498DB')
                self.view.att_tree.item(item_id, tags=('success',))
        
        self.view.set_status(f"查询到 {len(records)} 条考勤记录")
        
    def reset_attendance_search(self):
        self.view.att_emp_id_entry.delete(0, 'end')
        today = datetime.date.today().strftime('%Y-%m-%d')
        self.view.att_start_date.delete(0, 'end')
        self.view.att_start_date.insert(0, today)
        self.view.att_end_date.delete(0, 'end')
        self.view.att_end_date.insert(0, today)
        self.view.att_status_combo.current(0)
        self.load_attendance()
        
    def update_today_stats(self):
        today = datetime.date.today().strftime('%Y-%m-%d')
        all_attendance = self.att_dao.get_all_attendance()
        today_records = [r for r in all_attendance if r.check_in_time and r.check_in_time.startswith(today)]
        
        attendance_count = len(today_records)
        late_count = sum(1 for r in today_records if r.status == '迟到')
        early_count = sum(1 for r in today_records if r.status == '早退')
        absent_count = 0
        
        all_employees = self.emp_dao.get_all_employees()
        emp_ids_with_attendance = set(r.employee_id for r in today_records)
        absent_count = len([e for e in all_employees if e.employee_id not in emp_ids_with_attendance])
        
        self.view.today_stats_labels['today_attendance'].config(text=str(attendance_count))
        self.view.today_stats_labels['today_late'].config(text=str(late_count))
        self.view.today_stats_labels['today_early'].config(text=str(early_count))
        self.view.today_stats_labels['today_absent'].config(text=str(absent_count))
        
    def get_personal_statistics(self):
        emp_id = self.view.personal_emp_id_entry.get().strip()
        month_str = self.view.personal_month_entry.get().strip()
        
        if not emp_id:
            self.view.show_message("警告", "请输入工号", 'warning')
            return
        
        try:
            year, month = map(int, month_str.split('-'))
        except ValueError:
            self.view.show_message("警告", "月份格式错误", 'warning')
            return
        
        stats = self.att_dao.get_monthly_statistics(emp_id, year, month)
        
        if stats:
            self.view.personal_cards['attendance_days'].config(text=str(stats['正常']))
            self.view.personal_cards['late_count'].config(text=str(stats['迟到']))
            self.view.personal_cards['early_count'].config(text=str(stats['早退']))
            self.view.personal_cards['absent_count'].config(text=str(stats['缺勤']))
            self.view.personal_cards['leave_count'].config(text=str(stats['请假']))
            self.view.personal_cards['overtime_hours'].config(text=f"{stats['total_overtime_hours']:.2f}")
            
            employee = self.emp_dao.get_employee_by_id(emp_id)
            name = employee.name if employee else emp_id
            self.view.set_status(f"{name} {month_str} 月统计已更新")
        else:
            self.view.show_message("错误", "获取统计失败", 'error')
            
    def get_department_statistics(self):
        department = self.view.department_combo.get()
        month_str = self.view.department_month_entry.get().strip()
        
        if not department:
            self.view.show_message("警告", "请选择部门", 'warning')
            return
        
        try:
            year, month = map(int, month_str.split('-'))
        except ValueError:
            self.view.show_message("警告", "月份格式错误", 'warning')
            return
        
        stats = self.att_dao.get_department_monthly_statistics(department, year, month)
        
        if stats:
            self.view.department_cards['attendance_days'].config(text=str(stats['正常']))
            self.view.department_cards['late_count'].config(text=str(stats['迟到']))
            self.view.department_cards['early_count'].config(text=str(stats['早退']))
            self.view.department_cards['absent_count'].config(text=str(stats['缺勤']))
            self.view.department_cards['leave_count'].config(text=str(stats['请假']))
            self.view.department_cards['overtime_hours'].config(text=str(stats['加班']))
            
            self.view.set_status(f"{department} {month_str} 月统计已更新")
        else:
            self.view.show_message("错误", "获取统计失败", 'error')
            
    def update_department_combo(self):
        departments = self.emp_dao.get_departments()
        self.view.emp_dept_combo['values'] = [''] + departments
        self.view.department_combo['values'] = departments
        
    def backup_database(self):
        db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'attendance.db')
        backup_path = os.path.join(os.path.dirname(__file__), '..', 'database', 
                                   f'attendance_backup_{datetime.date.today().strftime("%Y%m%d")}.db')
        
        try:
            shutil.copy2(db_path, backup_path)
            self.view.show_message("成功", f"数据备份成功\n备份文件: {backup_path}")
            self.log_dao.add_log("管理员", "数据备份", backup_path)
            self.view.set_status("数据备份成功")
        except Exception as e:
            self.view.show_message("错误", f"备份失败: {str(e)}", 'error')
            self.log_dao.add_log("管理员", "数据备份失败", str(e), "FAILED")
            
    def clear_all_data(self):
        if not self.view.show_confirm("确认清空", "确定要清空所有考勤数据吗？此操作不可恢复！"):
            return
        
        if not self.view.show_confirm("再次确认", "这是最后一次确认，确定要清空吗？"):
            return
        
        if self.att_dao.clear_all_attendance():
            self.view.show_message("成功", "考勤数据已清空")
            self.log_dao.add_log("管理员", "清空考勤数据", "ALL")
            self.load_attendance()
            self.update_today_stats()
            self.view.set_status("考勤数据已清空")
        else:
            self.view.show_message("错误", "清空失败", 'error')
            
    def show_logs(self):
        logs = self.log_dao.get_all_logs()
        
        log_window = tk.Toplevel(self.view.root)
        log_window.title("操作日志")
        log_window.geometry("800x400")
        
        log_tree = ttk.Treeview(log_window, columns=('时间', '操作人', '操作', '目标', '结果'), show='headings')
        log_tree.heading('时间', text='时间')
        log_tree.heading('操作人', text='操作人')
        log_tree.heading('操作', text='操作')
        log_tree.heading('目标', text='目标')
        log_tree.heading('结果', text='结果')
        
        log_tree.column('时间', width=150)
        log_tree.column('操作人', width=100)
        log_tree.column('操作', width=120)
        log_tree.column('目标', width=200)
        log_tree.column('结果', width=80)
        
        scrollbar = ttk.Scrollbar(log_window, orient=tk.VERTICAL, command=log_tree.yview)
        log_tree.configure(yscroll=scrollbar.set)
        
        for log in logs:
            log_tree.insert('', 'end', values=(log[4], log[1], log[2], log[3], log[5]))
        
        log_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def on_tab_change(self, event):
        current_tab = self.view.notebook.index(self.view.notebook.select())
        if current_tab == 0:
            self.load_employees()
        elif current_tab == 1:
            self.update_today_stats()
        elif current_tab == 2:
            self.load_attendance()
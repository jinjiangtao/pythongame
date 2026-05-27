import time
from tkinter import messagebox
from models.registration import Registration
from utils.storage import StorageManager

class RegistrationController:
    def __init__(self):
        self.storage = StorageManager()
        self.registrations = []
        self.view = None
        self.form_panel = None
        self.list_panel = None

    def set_view(self, view):
        self.view = view

    def set_form_panel(self, form_panel):
        self.form_panel = form_panel

    def set_list_panel(self, list_panel):
        self.list_panel = list_panel

    def load_registrations(self):
        try:
            self.registrations = self.storage.load_data()
            if self.list_panel:
                self.list_panel.update_list(self.registrations)
            if self.view:
                self.view.set_status_message(f"已加载 {len(self.registrations)} 条挂号记录")
        except Exception as e:
            messagebox.showerror("错误", f"加载数据失败: {str(e)}")
            if self.view:
                self.view.set_status_message("加载数据失败")

    def submit_registration(self, data):
        try:
            if not data['name']:
                messagebox.showwarning("提示", "请输入患者姓名")
                return

            if not data['phone']:
                messagebox.showwarning("提示", "请输入联系电话")
                return

            if len(data['phone']) < 11:
                messagebox.showwarning("提示", "请输入有效的手机号码（至少11位）")
                return

            new_id = self.storage.get_next_id()
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            new_reg = Registration(
                id=new_id,
                name=data['name'],
                gender=data['gender'],
                department=data['department'],
                doctor=data['doctor'],
                phone=data['phone'],
                create_time=create_time
            )

            self.registrations.append(new_reg)

            if self.storage.save_data(self.registrations):
                messagebox.showinfo("成功", "挂号成功！")
                if self.form_panel:
                    self.form_panel.clear_form()
                self.load_registrations()
                if self.view:
                    self.view.set_status_message("挂号成功，数据已保存")
            else:
                messagebox.showerror("错误", "保存失败，请重试")
                self.registrations.pop()

        except Exception as e:
            messagebox.showerror("错误", f"提交失败: {str(e)}")
            if self.view:
                self.view.set_status_message("提交失败")

    def delete_registration(self, reg_id):
        try:
            self.registrations = [reg for reg in self.registrations if reg.id != reg_id]

            if self.storage.save_data(self.registrations):
                messagebox.showinfo("成功", "取消挂号成功！")
                self.load_registrations()
                if self.view:
                    self.view.set_status_message("已取消挂号")
            else:
                messagebox.showerror("错误", "删除失败，请重试")
                self.load_registrations()

        except Exception as e:
            messagebox.showerror("错误", f"删除失败: {str(e)}")
            if self.view:
                self.view.set_status_message("删除失败")

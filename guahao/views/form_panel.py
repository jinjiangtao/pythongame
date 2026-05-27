import customtkinter as ctk

class FormPanel(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=10)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.form_title = ctk.CTkLabel(self, text="📝 挂号信息录入", font=ctk.CTkFont(size=16, weight="bold"))
        self.form_title.grid(row=0, column=0, columnspan=2, padx=15, pady=15)

        self.name_label = ctk.CTkLabel(self, text="患者姓名：")
        self.name_label.grid(row=1, column=0, padx=15, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(self, placeholder_text="请输入姓名")
        self.name_entry.grid(row=1, column=1, padx=15, pady=10, sticky="ew")

        self.gender_label = ctk.CTkLabel(self, text="性别：")
        self.gender_label.grid(row=2, column=0, padx=15, pady=10, sticky="w")
        self.gender_var = ctk.StringVar(value="男")
        self.gender_frame = ctk.CTkFrame(self)
        self.gender_frame.grid(row=2, column=1, padx=15, pady=10, sticky="ew")
        self.male_radio = ctk.CTkRadioButton(self.gender_frame, text="男", variable=self.gender_var, value="男")
        self.male_radio.pack(side="left", padx=20)
        self.female_radio = ctk.CTkRadioButton(self.gender_frame, text="女", variable=self.gender_var, value="女")
        self.female_radio.pack(side="left", padx=20)

        self.department_label = ctk.CTkLabel(self, text="就诊科室：")
        self.department_label.grid(row=3, column=0, padx=15, pady=10, sticky="w")
        self.department_combobox = ctk.CTkComboBox(self, values=["内科", "外科", "妇产科", "儿科", "骨科", "眼科", "耳鼻喉科", "皮肤科"])
        self.department_combobox.set("内科")
        self.department_combobox.grid(row=3, column=1, padx=15, pady=10, sticky="ew")

        self.doctor_label = ctk.CTkLabel(self, text="接诊医生：")
        self.doctor_label.grid(row=4, column=0, padx=15, pady=10, sticky="w")
        self.doctor_combobox = ctk.CTkComboBox(self, values=["张医生", "李医生", "王医生", "赵医生", "刘医生", "陈医生"])
        self.doctor_combobox.set("张医生")
        self.doctor_combobox.grid(row=4, column=1, padx=15, pady=10, sticky="ew")

        self.phone_label = ctk.CTkLabel(self, text="联系电话：")
        self.phone_label.grid(row=5, column=0, padx=15, pady=10, sticky="w")
        self.phone_entry = ctk.CTkEntry(self, placeholder_text="请输入手机号")
        self.phone_entry.grid(row=5, column=1, padx=15, pady=10, sticky="ew")

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=6, column=0, columnspan=2, padx=15, pady=15, sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        self.submit_btn = ctk.CTkButton(self.button_frame, text="提交挂号", command=self.submit_form, fg_color="#22c55e", hover_color="#16a34a")
        self.submit_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.clear_btn = ctk.CTkButton(self.button_frame, text="清空表单", command=self.clear_form, fg_color="#f59e0b", hover_color="#d97706")
        self.clear_btn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    def get_form_data(self):
        return {
            'name': self.name_entry.get().strip(),
            'gender': self.gender_var.get(),
            'department': self.department_combobox.get(),
            'doctor': self.doctor_combobox.get(),
            'phone': self.phone_entry.get().strip()
        }

    def clear_form(self):
        self.name_entry.delete(0, 'end')
        self.gender_var.set("男")
        self.department_combobox.set("内科")
        self.doctor_combobox.set("张医生")
        self.phone_entry.delete(0, 'end')

    def submit_form(self):
        self.controller.submit_registration(self.get_form_data())

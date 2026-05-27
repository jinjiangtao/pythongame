import customtkinter as ctk
from tkinter import messagebox

class ListPanel(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=10)
        self.controller = controller
        self.selected_item = None
        self.create_widgets()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.list_title = ctk.CTkLabel(self, text="📋 挂号记录列表", font=ctk.CTkFont(size=16, weight="bold"))
        self.list_title.grid(row=0, column=0, padx=15, pady=15, sticky="w")

        self.listbox_frame = ctk.CTkFrame(self)
        self.listbox_frame.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")
        self.listbox_frame.grid_columnconfigure(0, weight=1)
        self.listbox_frame.grid_rowconfigure(0, weight=1)

        self.listbox = ctk.CTkScrollableFrame(self.listbox_frame)
        self.listbox.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.listbox.grid_columnconfigure(0, weight=1)

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, padx=15, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        self.delete_btn = ctk.CTkButton(self.button_frame, text="删除选中", command=self.delete_selected, fg_color="#ef4444", hover_color="#dc2626")
        self.delete_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.refresh_btn = ctk.CTkButton(self.button_frame, text="刷新列表", command=self.refresh_list, fg_color="#3b82f6", hover_color="#2563eb")
        self.refresh_btn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.empty_label = ctk.CTkLabel(self.listbox, text="暂无挂号记录", text_color="gray")
        self.empty_label.grid(row=0, column=0, padx=10, pady=50)

    def update_list(self, registrations):
        for widget in self.listbox.winfo_children():
            widget.destroy()

        if not registrations:
            self.empty_label = ctk.CTkLabel(self.listbox, text="暂无挂号记录", text_color="gray")
            self.empty_label.grid(row=0, column=0, padx=10, pady=50)
            return

        for i, reg in enumerate(registrations):
            item_frame = ctk.CTkFrame(self.listbox, corner_radius=8)
            item_frame.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
            item_frame.grid_columnconfigure(0, weight=1)
            item_frame.bind("<Button-1>", lambda e, rf=item_frame, rid=reg.id: self.select_item(rf, rid))

            info_text = f"📌 姓名：{reg.name} | {reg.gender}\n🏥 科室：{reg.department} | 医生：{reg.doctor}\n📱 电话：{reg.phone}\n⏰ {reg.create_time}"
            item_label = ctk.CTkLabel(item_frame, text=info_text, justify="left", anchor="w")
            item_label.grid(row=0, column=0, padx=10, pady=8, sticky="ew")

            item_frame.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

    def select_item(self, frame, reg_id):
        for widget in self.listbox.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

        frame.configure(fg_color="#3b82f6")
        self.selected_item = reg_id

    def delete_selected(self):
        if self.selected_item is None:
            messagebox.showwarning("提示", "请先选择要删除的挂号记录")
            return

        if messagebox.askyesno("确认删除", "确定要取消该挂号吗？"):
            self.controller.delete_registration(self.selected_item)
            self.selected_item = None

    def refresh_list(self):
        self.controller.load_registrations()

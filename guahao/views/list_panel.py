import customtkinter as ctk
from tkinter import messagebox

class ListPanel(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=10)
        self.controller = controller
        self.registrations = []
        self.all_registrations = []
        self.sort_column = None
        self.sort_reverse = False
        self.selected_item = None
        self.search_name = ""
        self.search_department = ""
        self.search_doctor = ""
        self.search_phone = ""
        self.create_widgets()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.search_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#f8f9fa")
        self.search_frame.grid(row=0, column=0, padx=15, pady=10, sticky="ew")
        self.search_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.search_title = ctk.CTkLabel(self.search_frame, text="🔍 搜索筛选", font=ctk.CTkFont(size=14, weight="bold"), text_color="#1f2937")
        self.search_title.grid(row=0, column=0, columnspan=5, padx=10, pady=8, sticky="w")

        self.name_search = ctk.CTkEntry(self.search_frame, placeholder_text="按姓名搜索", width=130, height=32, font=ctk.CTkFont(size=13))
        self.name_search.grid(row=1, column=0, padx=8, pady=8)
        self.name_search.bind("<KeyRelease>", lambda e: self.on_search_change())

        self.dept_search = ctk.CTkComboBox(self.search_frame, values=["全部科室", "内科", "外科", "妇产科", "儿科", "骨科", "眼科", "耳鼻喉科", "皮肤科"], 
                                          width=130, height=32, font=ctk.CTkFont(size=13), state="readonly")
        self.dept_search.grid(row=1, column=1, padx=8, pady=8)
        self.dept_search.set("全部科室")
        self.dept_search.bind("<<ComboboxSelected>>", lambda e: self.on_search_change())

        self.doctor_search = ctk.CTkComboBox(self.search_frame, values=["全部医生", "张医生", "李医生", "王医生", "赵医生", "刘医生", "陈医生"], 
                                            width=130, height=32, font=ctk.CTkFont(size=13), state="readonly")
        self.doctor_search.grid(row=1, column=2, padx=8, pady=8)
        self.doctor_search.set("全部医生")
        self.doctor_search.bind("<<ComboboxSelected>>", lambda e: self.on_search_change())

        self.phone_search = ctk.CTkEntry(self.search_frame, placeholder_text="按电话搜索", width=130, height=32, font=ctk.CTkFont(size=13))
        self.phone_search.grid(row=1, column=3, padx=8, pady=8)
        self.phone_search.bind("<KeyRelease>", lambda e: self.on_search_change())

        self.clear_search_btn = ctk.CTkButton(self.search_frame, text="清空", width=70, height=32, 
                                              fg_color="#6b7280", hover_color="#4b5563", 
                                              font=ctk.CTkFont(size=12, weight="bold"),
                                              command=self.clear_search)
        self.clear_search_btn.grid(row=1, column=4, padx=8, pady=8)

        self.list_title_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.list_title_frame.grid(row=1, column=0, padx=15, pady=(5, 0), sticky="ew")

        self.list_container = ctk.CTkFrame(self, corner_radius=10, fg_color="#ffffff")
        self.list_container.grid(row=2, column=0, padx=15, pady=5, sticky="nsew")
        self.list_container.grid_rowconfigure(0, weight=1)
        self.list_container.grid_columnconfigure(0, weight=1)

        self.header_frame = ctk.CTkFrame(self.list_container, corner_radius=0, height=40, fg_color="#1e3a5f")
        self.header_frame.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="ew")
        self.header_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.header_frame.grid_columnconfigure(7, weight=0)
        self.header_frame.pack_propagate(False)

        self.header_labels = []
        headers = [
            ("序号", 60),
            ("姓名", 90),
            ("性别", 60),
            ("科室", 110),
            ("医生", 90),
            ("联系电话", 130),
            ("挂号时间", 150),
            ("操作", 80)
        ]

        total_width = sum(w for _, w in headers)
        self.scroll_frame_min_width = total_width

        for idx, (text, width) in enumerate(headers):
            label = ctk.CTkLabel(
                self.header_frame,
                text=text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#ffffff",
                anchor="center"
            )
            label.grid(row=0, column=idx, padx=1, sticky="nsew")
            self.header_frame.grid_columnconfigure(idx, minsize=width)
            self.header_labels.append((label, text, width))

        for label, text, _ in self.header_labels:
            if text in ["姓名", "科室", "挂号时间"]:
                label.bind("<Button-1>", lambda e, col=text: self.on_header_click(col))
                label.configure(cursor="hand2")

        self.canvas_frame = ctk.CTkCanvas(self.list_container, bg="#ffffff", highlightthickness=0)
        self.scrollbar_y = ctk.CTkScrollbar(self.list_container, orientation="vertical", command=self.canvas_yview)
        self.scrollbar_x = ctk.CTkScrollbar(self.list_container, orientation="horizontal", command=self.canvas_xview)

        self.scroll_frame = ctk.CTkFrame(self.canvas_frame, corner_radius=0, fg_color="transparent")

        self.canvas_frame.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns", padx=(0, 5), pady=(45, 5))
        self.scrollbar_x.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5))
        self.canvas_frame.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=(45, 0))

        self.scroll_window = self.canvas_frame.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind("<Configure>", lambda e: self.on_frame_configure())
        self.canvas_frame.bind("<Configure>", lambda e: self.on_canvas_configure())
        self.scroll_frame.bind("<MouseWheel>", lambda e: self.canvas_yview("scroll", int(-1 * (e.delta / 120)), "units"))

        self.empty_label = ctk.CTkLabel(
            self.scroll_frame,
            text="",
            text_color="#6b7280",
            font=ctk.CTkFont(size=14)
        )
        self.empty_label.pack(pady=50)

        self.button_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, padx=15, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        self.delete_btn = ctk.CTkButton(
            self.button_frame,
            text="删除选中",
            command=self.delete_selected,
            fg_color="#ef4444",
            hover_color="#dc2626",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.delete_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.refresh_btn = ctk.CTkButton(
            self.button_frame,
            text="刷新列表",
            command=self.refresh_list,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.refresh_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    def on_frame_configure(self):
        self.canvas_frame.configure(scrollregion=self.canvas_frame.bbox("all"))

    def on_canvas_configure(self, event=None):
        canvas_width = self.canvas_frame.winfo_width()
        frame_width = self.scroll_frame.winfo_width()
        new_width = max(canvas_width, frame_width, self.scroll_frame_min_width)
        self.canvas_frame.itemconfig(self.scroll_window, width=new_width)

    def canvas_yview(self, *args):
        self.canvas_frame.yview(*args)

    def canvas_xview(self, *args):
        self.canvas_frame.xview(*args)

    def on_header_click(self, column):
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False

        self.update_sort_indicators()
        self.apply_filter_and_sort()

    def update_sort_indicators(self):
        for label, text, _ in self.header_labels:
            if text == self.sort_column:
                arrow = " ▲" if not self.sort_reverse else " ▼"
                label.configure(text=text + arrow)
            else:
                label.configure(text=text)

    def on_search_change(self):
        self.search_name = self.name_search.get().strip().lower()
        self.search_department = self.dept_search.get()
        self.search_doctor = self.doctor_search.get()
        self.search_phone = self.phone_search.get().strip().lower()
        self.apply_filter_and_sort()

    def clear_search(self):
        self.name_search.delete(0, "end")
        self.dept_search.set("全部科室")
        self.doctor_search.set("全部医生")
        self.phone_search.delete(0, "end")
        self.search_name = ""
        self.search_department = ""
        self.search_doctor = ""
        self.search_phone = ""
        self.apply_filter_and_sort()

    def apply_filter_and_sort(self):
        filtered = []

        for reg in self.all_registrations:
            match = True

            if self.search_name and self.search_name not in reg.name.lower():
                match = False
            if self.search_department != "全部科室" and reg.department != self.search_department:
                match = False
            if self.search_doctor != "全部医生" and reg.doctor != self.search_doctor:
                match = False
            if self.search_phone and self.search_phone not in reg.phone.lower():
                match = False

            if match:
                filtered.append(reg)

        if self.sort_column:
            reverse = self.sort_reverse
            if self.sort_column == "姓名":
                filtered.sort(key=lambda x: x.name, reverse=reverse)
            elif self.sort_column == "科室":
                filtered.sort(key=lambda x: x.department, reverse=reverse)
            elif self.sort_column == "挂号时间":
                filtered.sort(key=lambda x: x.create_time, reverse=reverse)

        self.registrations = filtered
        self.update_list()

    def update_list(self, registrations=None):
        if registrations is not None:
            self.all_registrations = registrations
            self.apply_filter_and_sort()
            return

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not self.registrations:
            self.empty_label.configure(text="未找到匹配的挂号记录\n请尝试调整搜索条件")
            self.empty_label.pack(pady=50)
            return

        self.empty_label.pack_forget()

        for i, reg in enumerate(self.registrations):
            bg_color = "#f8f9fa" if i % 2 == 0 else "#ffffff"

            row_frame = ctk.CTkFrame(self.scroll_frame, corner_radius=0, height=42, fg_color=bg_color)
            row_frame.grid(row=i, column=0, sticky="ew")
            row_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
            row_frame.grid_columnconfigure(7, weight=0)
            row_frame.grid_columnconfigure(0, minsize=60)
            row_frame.grid_columnconfigure(1, minsize=90)
            row_frame.grid_columnconfigure(2, minsize=60)
            row_frame.grid_columnconfigure(3, minsize=110)
            row_frame.grid_columnconfigure(4, minsize=90)
            row_frame.grid_columnconfigure(5, minsize=130)
            row_frame.grid_columnconfigure(6, minsize=150)
            row_frame.grid_columnconfigure(7, minsize=80)
            row_frame.pack_propagate(False)

            row_data = [
                str(reg.id),
                reg.name,
                reg.gender,
                reg.department,
                reg.doctor,
                reg.phone,
                reg.create_time
            ]

            for j, text in enumerate(row_data):
                label = ctk.CTkLabel(
                    row_frame,
                    text=text,
                    anchor="center",
                    font=ctk.CTkFont(size=12),
                    text_color="#374151",
                    wraplength=0
                )
                label.grid(row=0, column=j, padx=2, pady=8, sticky="nsew")

            action_frame = ctk.CTkFrame(row_frame, fg_color=bg_color)
            action_frame.grid(row=0, column=7, padx=2, pady=4, sticky="nsew")
            action_frame.grid_columnconfigure(0, weight=1)

            delete_btn = ctk.CTkButton(
                action_frame,
                text="删除",
                width=60,
                height=26,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="#ef4444",
                hover_color="#dc2626",
                command=lambda rid=reg.id: self.controller.delete_registration(rid)
            )
            delete_btn.grid(row=0, column=0, padx=5)

            row_frame.bind("<Button-1>", lambda e, rf=row_frame, rid=reg.id: self.select_item(rf, rid))
            action_frame.bind("<Button-1>", lambda e: e.widget.focus_set())

            for child in row_frame.winfo_children():
                if isinstance(child, ctk.CTkLabel):
                    child.bind("<Button-1>", lambda e, rf=row_frame, rid=reg.id: self.select_item(rf, rid))
                elif isinstance(child, ctk.CTkFrame):
                    child.bind("<Button-1>", lambda e: e.widget.focus_set())

    def select_item(self, frame, reg_id):
        children = self.scroll_frame.winfo_children()
        for idx, widget in enumerate(children):
            if isinstance(widget, ctk.CTkFrame):
                bg_color = "#f8f9fa" if idx % 2 == 0 else "#ffffff"
                widget.configure(fg_color=bg_color)

        frame.configure(fg_color="#dbeafe")
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
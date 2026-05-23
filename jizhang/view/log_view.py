import customtkinter as ctk
from config import ACCENT_COLOR


class LogView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        self.header_frame = ctk.CTkFrame(self.frame)
        self.header_frame.pack(fill=ctk.X, pady=10)

        self.type_var = ctk.StringVar(value="all")
        self.all_radio = ctk.CTkRadioButton(self.header_frame, text="全部",
                                            variable=self.type_var, value="all")
        self.all_radio.pack(side=ctk.LEFT, padx=5)
        self.login_radio = ctk.CTkRadioButton(self.header_frame, text="登录",
                                              variable=self.type_var, value="login")
        self.login_radio.pack(side=ctk.LEFT, padx=5)
        self.add_radio = ctk.CTkRadioButton(self.header_frame, text="新增",
                                            variable=self.type_var, value="add")
        self.add_radio.pack(side=ctk.LEFT, padx=5)
        self.edit_radio = ctk.CTkRadioButton(self.header_frame, text="编辑",
                                             variable=self.type_var, value="edit")
        self.edit_radio.pack(side=ctk.LEFT, padx=5)
        self.delete_radio = ctk.CTkRadioButton(self.header_frame, text="删除",
                                               variable=self.type_var, value="delete")
        self.delete_radio.pack(side=ctk.LEFT, padx=5)
        self.export_radio = ctk.CTkRadioButton(self.header_frame, text="导出",
                                               variable=self.type_var, value="export")
        self.export_radio.pack(side=ctk.LEFT, padx=5)
        self.backup_radio = ctk.CTkRadioButton(self.header_frame, text="备份",
                                               variable=self.type_var, value="backup")
        self.backup_radio.pack(side=ctk.LEFT, padx=5)

        self.start_date_label = ctk.CTkLabel(self.header_frame, text="开始时间:")
        self.start_date_label.pack(side=ctk.LEFT, padx=20)
        self.start_date_entry = ctk.CTkEntry(self.header_frame, width=120)
        self.start_date_entry.pack(side=ctk.LEFT, padx=5)

        self.end_date_label = ctk.CTkLabel(self.header_frame, text="结束时间:")
        self.end_date_label.pack(side=ctk.LEFT, padx=10)
        self.end_date_entry = ctk.CTkEntry(self.header_frame, width=120)
        self.end_date_entry.pack(side=ctk.LEFT, padx=5)

        self.search_button = ctk.CTkButton(self.header_frame, text="查询", width=80, height=25,
                                           fg_color="#95a5a6", hover_color="#7f8c8d")
        self.search_button.pack(side=ctk.RIGHT, padx=10)

        self.tree_frame = ctk.CTkFrame(self.frame)
        self.tree_frame.pack(fill=ctk.BOTH, expand=True)

        self.header_row = ctk.CTkFrame(self.tree_frame, fg_color="#3498db")
        self.header_row.pack(fill=ctk.X)

        user_header = ctk.CTkLabel(self.header_row, text="操作人", width=120, anchor=ctk.CENTER,
                                   text_color="white", font=ctk.CTkFont(weight="bold"))
        user_header.pack(side=ctk.LEFT, padx=5)

        type_header = ctk.CTkLabel(self.header_row, text="操作类型", width=100, anchor=ctk.CENTER,
                                   text_color="white", font=ctk.CTkFont(weight="bold"))
        type_header.pack(side=ctk.LEFT, padx=5)

        desc_header = ctk.CTkLabel(self.header_row, text="操作描述", width=300, anchor=ctk.CENTER,
                                   text_color="white", font=ctk.CTkFont(weight="bold"))
        desc_header.pack(side=ctk.LEFT, padx=5)

        ip_header = ctk.CTkLabel(self.header_row, text="IP地址", width=120, anchor=ctk.CENTER,
                                 text_color="white", font=ctk.CTkFont(weight="bold"))
        ip_header.pack(side=ctk.LEFT, padx=5)

        time_header = ctk.CTkLabel(self.header_row, text="操作时间", width=150, anchor=ctk.CENTER,
                                   text_color="white", font=ctk.CTkFont(weight="bold"))
        time_header.pack(side=ctk.RIGHT, padx=5)

        self.tree = ctk.CTkScrollableFrame(self.tree_frame)
        self.tree.pack(fill=ctk.BOTH, expand=True)

        self.message_label = ctk.CTkLabel(self.frame, text="", text_color="#27ae60", font=ctk.CTkFont(size=12))
        self.message_label.pack(pady=10)

        self.pagination_frame = ctk.CTkFrame(self.frame)
        self.pagination_frame.pack(fill=ctk.X, pady=10)

        self.prev_button = ctk.CTkButton(self.pagination_frame, text="上一页", width=80, height=25,
                                         fg_color="#95a5a6", hover_color="#7f8c8d", state=ctk.DISABLED)
        self.prev_button.pack(side=ctk.LEFT, padx=5)

        self.page_label = ctk.CTkLabel(self.pagination_frame, text="第 1 / 1 页")
        self.page_label.pack(side=ctk.LEFT, padx=10)

        self.next_button = ctk.CTkButton(self.pagination_frame, text="下一页", width=80, height=25,
                                         fg_color="#95a5a6", hover_color="#7f8c8d", state=ctk.DISABLED)
        self.next_button.pack(side=ctk.LEFT, padx=5)

        self.total_label = ctk.CTkLabel(self.pagination_frame, text="共 0 条记录")
        self.total_label.pack(side=ctk.RIGHT, padx=10)

        self.logs = []
        self.current_page = 1
        self.total_pages = 1
        self.total_count = 0
        self.page_size = 20

    def get_filter_params(self):
        return {
            "operation_type": self.type_var.get() if self.type_var.get() != "all" else None,
            "start_date": self.start_date_entry.get().strip() or None,
            "end_date": self.end_date_entry.get().strip() or None
        }

    def set_search_command(self, command):
        self.search_button.configure(command=command)

    def set_prev_page_command(self, command):
        self.prev_button.configure(command=command)

    def set_next_page_command(self, command):
        self.next_button.configure(command=command)

    def set_type_change_command(self, command):
        self.all_radio.configure(command=command)
        self.login_radio.configure(command=command)
        self.add_radio.configure(command=command)
        self.edit_radio.configure(command=command)
        self.delete_radio.configure(command=command)
        self.export_radio.configure(command=command)
        self.backup_radio.configure(command=command)

    def clear_logs(self):
        for widget in self.tree.winfo_children():
            widget.destroy()

    def update_pagination(self, current_page, total_pages, total_count):
        self.current_page = current_page
        self.total_pages = total_pages
        self.total_count = total_count

        self.page_label.configure(text=f"第 {current_page} / {total_pages} 页")
        self.total_label.configure(text=f"共 {total_count} 条记录")

        self.prev_button.configure(state=ctk.NORMAL if current_page > 1 else ctk.DISABLED)
        self.next_button.configure(state=ctk.NORMAL if current_page < total_pages else ctk.DISABLED)

    def get_current_page(self):
        return self.current_page

    def get_page_size(self):
        return self.page_size

    def reset_page(self):
        self.current_page = 1

    def display_logs(self, logs):
        self.clear_logs()
        self.logs = logs

        for log in logs:
            log_id, user_id, username, operation_type, operation_desc, ip_address, created_at = log

            row_frame = ctk.CTkFrame(self.tree)
            row_frame.pack(fill=ctk.X, pady=2)

            user_label = ctk.CTkLabel(row_frame, text=username, width=120)
            user_label.pack(side=ctk.LEFT, padx=5)

            type_label = ctk.CTkLabel(row_frame, text=self.get_type_name(operation_type), width=100,
                                      text_color=self.get_type_color(operation_type))
            type_label.pack(side=ctk.LEFT, padx=5)

            desc_label = ctk.CTkLabel(row_frame, text=operation_desc, width=300, anchor=ctk.W)
            desc_label.pack(side=ctk.LEFT, padx=5)

            ip_label = ctk.CTkLabel(row_frame, text=ip_address or "-", width=120)
            ip_label.pack(side=ctk.LEFT, padx=5)

            time_label = ctk.CTkLabel(row_frame, text=created_at, width=150)
            time_label.pack(side=ctk.RIGHT, padx=5)

    def get_type_name(self, operation_type):
        type_names = {
            "login": "登录",
            "add": "新增",
            "edit": "编辑",
            "delete": "删除",
            "export": "导出",
            "backup": "备份",
            "restore": "恢复"
        }
        return type_names.get(operation_type, operation_type)

    def get_type_color(self, operation_type):
        type_colors = {
            "login": "#3498db",
            "add": "#27ae60",
            "edit": "#f39c12",
            "delete": "#e74c3c",
            "export": "#9b59b6",
            "backup": "#1abc9c",
            "restore": "#00bcd4"
        }
        return type_colors.get(operation_type, "#333333")

    def get_frame(self):
        return self.frame
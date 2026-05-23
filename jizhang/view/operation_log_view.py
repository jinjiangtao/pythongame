import customtkinter as ctk
from config import ACCENT_COLOR


class OperationLogView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        self.header_frame = ctk.CTkFrame(self.frame)
        self.header_frame.pack(fill=ctk.X, pady=10)

        self.title_label = ctk.CTkLabel(self.header_frame, text="操作日志", 
                                        font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(side=ctk.LEFT, padx=10)

        self.filter_container = ctk.CTkFrame(self.header_frame)
        self.filter_container.pack(fill=ctk.X, pady=10, padx=10)

        self.type_label = ctk.CTkLabel(self.filter_container, text="操作类型:")
        self.type_label.pack(side=ctk.LEFT, padx=10)

        self.type_var = ctk.StringVar(value="全部")
        self.type_combobox = ctk.CTkComboBox(self.filter_container, variable=self.type_var, width=150)
        self.type_combobox.pack(side=ctk.LEFT, padx=5)

        self.start_date_label = ctk.CTkLabel(self.filter_container, text="开始日期:")
        self.start_date_label.pack(side=ctk.LEFT, padx=10)
        self.start_date_entry = ctk.CTkEntry(self.filter_container, width=100)
        self.start_date_entry.pack(side=ctk.LEFT, padx=5)

        self.end_date_label = ctk.CTkLabel(self.filter_container, text="结束日期:")
        self.end_date_label.pack(side=ctk.LEFT, padx=10)
        self.end_date_entry = ctk.CTkEntry(self.filter_container, width=100)
        self.end_date_entry.pack(side=ctk.LEFT, padx=5)

        self.search_button = ctk.CTkButton(self.filter_container, text="查询", width=80, height=30,
                                           fg_color="#95a5a6", hover_color="#7f8c8d")
        self.search_button.pack(side=ctk.LEFT, padx=10)

        self.refresh_button = ctk.CTkButton(self.filter_container, text="刷新", width=80, height=30,
                                            fg_color=ACCENT_COLOR, hover_color="#2980b9")
        self.refresh_button.pack(side=ctk.LEFT, padx=5)

        self.tree_frame = ctk.CTkFrame(self.frame)
        self.tree_frame.pack(fill=ctk.BOTH, expand=True)

        self.header_row = ctk.CTkFrame(self.tree_frame, fg_color="#3498db")
        self.header_row.pack(fill=ctk.X)

        time_header = ctk.CTkLabel(self.header_row, text="操作时间", width=180, anchor=ctk.CENTER,
                                    text_color="white", font=ctk.CTkFont(weight="bold"))
        time_header.pack(side=ctk.LEFT, padx=5)

        type_header = ctk.CTkLabel(self.header_row, text="操作类型", width=120, anchor=ctk.CENTER,
                                   text_color="white", font=ctk.CTkFont(weight="bold"))
        type_header.pack(side=ctk.LEFT, padx=5)

        desc_header = ctk.CTkLabel(self.header_row, text="描述", width=300, anchor=ctk.W,
                                   text_color="white", font=ctk.CTkFont(weight="bold"))
        desc_header.pack(side=ctk.LEFT, padx=5)

        details_header = ctk.CTkLabel(self.header_row, text="详细信息", width=200, anchor=ctk.W,
                                      text_color="white", font=ctk.CTkFont(weight="bold"))
        details_header.pack(side=ctk.LEFT, padx=5)

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

        self.set_operation_types(["全部"] + list(self.get_operation_types().values()))

    def get_operation_types(self):
        return {
            "LOGIN": "登录",
            "LOGOUT": "退出登录",
            "ADD_BILL": "添加账单",
            "UPDATE_BILL": "更新账单",
            "DELETE_BILL": "删除账单",
            "QUERY_BILL": "查询账单",
            "ADD_CATEGORY": "添加分类",
            "UPDATE_CATEGORY": "更新分类",
            "DELETE_CATEGORY": "删除分类",
            "QUERY_CATEGORY": "查询分类",
            "EXPORT_DATA": "导出数据",
            "BACKUP_DATA": "备份数据",
            "RESTORE_DATA": "恢复数据",
            "THEME_CHANGE": "切换主题"
        }

    def set_operation_types(self, types):
        self.type_combobox.configure(values=types)

    def get_filter_params(self):
        selected_type = self.type_var.get()
        operation_type = None
        if selected_type != "全部":
            type_map = {v: k for k, v in self.get_operation_types().items()}
            operation_type = type_map.get(selected_type)

        return {
            "operation_type": operation_type,
            "start_date": self.start_date_entry.get().strip() or None,
            "end_date": self.end_date_entry.get().strip() or None
        }

    def set_search_command(self, command):
        self.search_button.configure(command=command)

    def set_refresh_command(self, command):
        self.refresh_button.configure(command=command)

    def set_prev_page_command(self, command):
        self.prev_button.configure(command=command)

    def set_next_page_command(self, command):
        self.next_button.configure(command=command)

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
            log_id, user_id, operation_type, operation_name, description, details, created_at = log
            row_frame = ctk.CTkFrame(self.tree)
            row_frame.pack(fill=ctk.X, pady=2)

            time_label = ctk.CTkLabel(row_frame, text=created_at, width=180)
            time_label.pack(side=ctk.LEFT, padx=5)

            type_label = ctk.CTkLabel(row_frame, text=operation_name, width=120)
            type_label.pack(side=ctk.LEFT, padx=5)

            desc_text = description if description else ""
            desc_label = ctk.CTkLabel(row_frame, text=desc_text[:30] + "..." if len(desc_text) > 30 else desc_text,
                                     width=300, anchor=ctk.W)
            desc_label.pack(side=ctk.LEFT, padx=5)

            details_text = details if details else ""
            details_label = ctk.CTkLabel(row_frame, text=details_text[:25] + "..." if len(details_text) > 25 else details_text,
                                        width=200, anchor=ctk.W)
            details_label.pack(side=ctk.LEFT, padx=5)

    def show_message(self, message, is_error=False):
        color = "#e74c3c" if is_error else "#27ae60"
        self.message_label.configure(text=message, text_color=color)

    def get_frame(self):
        return self.frame

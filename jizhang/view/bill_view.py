import customtkinter as ctk
from datetime import datetime
from config import ACCENT_COLOR, PAYMENT_METHODS


class BillView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        self.header_frame = ctk.CTkFrame(self.frame)
        self.header_frame.pack(fill=ctk.X, pady=10)

        self.filter_container = ctk.CTkFrame(self.header_frame)
        self.filter_container.pack(fill=ctk.X, pady=5)

        self.type_var = ctk.StringVar(value="all")
        self.all_radio = ctk.CTkRadioButton(self.filter_container, text="全部",
                                            variable=self.type_var, value="all")
        self.all_radio.pack(side=ctk.LEFT, padx=5)
        self.expense_radio = ctk.CTkRadioButton(self.filter_container, text="支出",
                                                variable=self.type_var, value="expense")
        self.expense_radio.pack(side=ctk.LEFT, padx=5)
        self.income_radio = ctk.CTkRadioButton(self.filter_container, text="收入",
                                               variable=self.type_var, value="income")
        self.income_radio.pack(side=ctk.LEFT, padx=5)

        self.category_label = ctk.CTkLabel(self.filter_container, text="分类:")
        self.category_label.pack(side=ctk.LEFT, padx=20)
        self.category_var = ctk.StringVar(value="")
        self.category_combobox = ctk.CTkComboBox(self.filter_container, variable=self.category_var, width=120)
        self.category_combobox.pack(side=ctk.LEFT, padx=5)

        self.start_date_label = ctk.CTkLabel(self.filter_container, text="开始日期:")
        self.start_date_label.pack(side=ctk.LEFT, padx=20)
        self.start_date_entry = ctk.CTkEntry(self.filter_container, width=100)
        self.start_date_entry.pack(side=ctk.LEFT, padx=5)

        self.end_date_label = ctk.CTkLabel(self.filter_container, text="结束日期:")
        self.end_date_label.pack(side=ctk.LEFT, padx=10)
        self.end_date_entry = ctk.CTkEntry(self.filter_container, width=100)
        self.end_date_entry.pack(side=ctk.LEFT, padx=5)

        self.button_container = ctk.CTkFrame(self.header_frame)
        self.button_container.pack(fill=ctk.X, pady=5)

        self.search_button = ctk.CTkButton(self.button_container, text="查询", width=80, height=25,
                                           fg_color="#95a5a6", hover_color="#7f8c8d")
        self.search_button.pack(side=ctk.LEFT, padx=10)

        self.statistics_button = ctk.CTkButton(self.button_container, text="数据统计", width=80, height=25,
                                               fg_color="#f39c12", hover_color="#d68910")
        self.statistics_button.pack(side=ctk.LEFT, padx=10)

        self.add_button = ctk.CTkButton(self.button_container, text="新增账单", width=120, height=35,
                                        fg_color=ACCENT_COLOR, hover_color="#2980b9")
        self.add_button.pack(side=ctk.RIGHT, padx=5)
        
        self.export_button = ctk.CTkButton(self.button_container, text="导出Excel", width=100, height=35,
                                          fg_color="#27ae60", hover_color="#1e8449")
        self.export_button.pack(side=ctk.RIGHT, padx=5)

        self.summary_frame = ctk.CTkFrame(self.frame)
        self.summary_frame.pack(fill=ctk.X, pady=10)

        self.income_label = ctk.CTkLabel(self.summary_frame, text="收入: ¥0.00", 
                                         text_color="#27ae60", font=ctk.CTkFont(size=16, weight="bold"))
        self.income_label.pack(side=ctk.LEFT, padx=20)

        self.expense_label = ctk.CTkLabel(self.summary_frame, text="支出: ¥0.00", 
                                          text_color="#e74c3c", font=ctk.CTkFont(size=16, weight="bold"))
        self.expense_label.pack(side=ctk.LEFT, padx=20)

        self.balance_label = ctk.CTkLabel(self.summary_frame, text="结余: ¥0.00", 
                                          text_color=ACCENT_COLOR, font=ctk.CTkFont(size=16, weight="bold"))
        self.balance_label.pack(side=ctk.LEFT, padx=20)

        self.tree_frame = ctk.CTkFrame(self.frame)
        self.tree_frame.pack(fill=ctk.BOTH, expand=True)

        self.header_row = ctk.CTkFrame(self.tree_frame, fg_color="#3498db")
        self.header_row.pack(fill=ctk.X)

        type_header = ctk.CTkLabel(self.header_row, text="类型", width=60, anchor=ctk.CENTER, 
                                   text_color="white", font=ctk.CTkFont(weight="bold"))
        type_header.pack(side=ctk.LEFT, padx=5)

        date_header = ctk.CTkLabel(self.header_row, text="日期", width=100, anchor=ctk.CENTER, 
                                   text_color="white", font=ctk.CTkFont(weight="bold"))
        date_header.pack(side=ctk.LEFT, padx=5)

        cat_header = ctk.CTkLabel(self.header_row, text="分类", width=100, anchor=ctk.CENTER, 
                                  text_color="white", font=ctk.CTkFont(weight="bold"))
        cat_header.pack(side=ctk.LEFT, padx=5)

        amount_header = ctk.CTkLabel(self.header_row, text="金额", width=100, anchor=ctk.CENTER, 
                                     text_color="white", font=ctk.CTkFont(weight="bold"))
        amount_header.pack(side=ctk.LEFT, padx=5)

        pm_header = ctk.CTkLabel(self.header_row, text="付款方式", width=80, anchor=ctk.CENTER, 
                                  text_color="white", font=ctk.CTkFont(weight="bold"))
        pm_header.pack(side=ctk.LEFT, padx=5)

        remark_header = ctk.CTkLabel(self.header_row, text="备注", width=120, anchor=ctk.CENTER, 
                                     text_color="white", font=ctk.CTkFont(weight="bold"))
        remark_header.pack(side=ctk.LEFT, padx=5)

        action_header = ctk.CTkLabel(self.header_row, text="操作", width=150, anchor=ctk.CENTER, 
                                     text_color="white", font=ctk.CTkFont(weight="bold"))
        action_header.pack(side=ctk.RIGHT, padx=5)

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

        self.bills = []
        self.current_page = 1
        self.total_pages = 1
        self.total_count = 0
        self.page_size = 20

    def get_filter_params(self):
        return {
            "type": self.type_var.get() if self.type_var.get() != "all" else None,
            "category_id": self.category_var.get() if self.category_var.get() else None,
            "start_date": self.start_date_entry.get().strip() or None,
            "end_date": self.end_date_entry.get().strip() or None
        }

    def set_add_command(self, command):
        self.add_button.configure(command=command)

    def set_export_command(self, command):
        self.export_button.configure(command=command)

    def set_search_command(self, command):
        self.search_button.configure(command=command)

    def set_statistics_command(self, command):
        self.statistics_button.configure(command=command)

    def set_prev_page_command(self, command):
        self.prev_button.configure(command=command)

    def set_next_page_command(self, command):
        self.next_button.configure(command=command)

    def set_type_change_command(self, command):
        self.all_radio.configure(command=command)
        self.expense_radio.configure(command=command)
        self.income_radio.configure(command=command)

    def clear_bills(self):
        for widget in self.tree.winfo_children():
            widget.destroy()

    def set_categories(self, categories):
        category_list = [""] + [f"{cat[0]}:{cat[1]}" for cat in categories]
        self.category_combobox.configure(values=category_list)

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

    def display_bills(self, bills):
        self.clear_bills()
        self.bills = bills

        for bill in bills:
            bill_id, type_, category_id, category_name, amount, remark, payment_method, date, created_at = bill
            row_frame = ctk.CTkFrame(self.tree)
            row_frame.pack(fill=ctk.X, pady=2)

            type_label = ctk.CTkLabel(row_frame, text="收入" if type_ == "income" else "支出", 
                                      width=60, text_color="#27ae60" if type_ == "income" else "#e74c3c")
            type_label.pack(side=ctk.LEFT, padx=5)

            date_label = ctk.CTkLabel(row_frame, text=date, width=100)
            date_label.pack(side=ctk.LEFT, padx=5)

            cat_label = ctk.CTkLabel(row_frame, text=category_name, width=100)
            cat_label.pack(side=ctk.LEFT, padx=5)

            amount_label = ctk.CTkLabel(row_frame, text=f"¥{amount:.2f}", width=100, 
                                        text_color="#27ae60" if type_ == "income" else "#e74c3c")
            amount_label.pack(side=ctk.LEFT, padx=5)

            pm_label = ctk.CTkLabel(row_frame, text=payment_method, width=80)
            pm_label.pack(side=ctk.LEFT, padx=5)

            remark_label = ctk.CTkLabel(row_frame, text=remark[:10] + "..." if remark and len(remark) > 10 else remark or "", 
                                        width=120, anchor=ctk.W)
            remark_label.pack(side=ctk.LEFT, padx=5)

            edit_button = ctk.CTkButton(row_frame, text="编辑", width=60, height=25,
                                        fg_color="#f39c12", hover_color="#d68910",
                                        command=lambda bid=bill_id: self.on_edit(bid))
            edit_button.pack(side=ctk.RIGHT, padx=5)

            delete_button = ctk.CTkButton(row_frame, text="删除", width=60, height=25,
                                          fg_color="#e74c3c", hover_color="#c0392b",
                                          command=lambda bid=bill_id: self.on_delete(bid))
            delete_button.pack(side=ctk.RIGHT, padx=5)

    def update_summary(self, summary):
        income = summary.get("income", 0)
        expense = summary.get("expense", 0)
        balance = income - expense

        self.income_label.configure(text=f"收入: ¥{income:.2f}")
        self.expense_label.configure(text=f"支出: ¥{expense:.2f}")
        self.balance_label.configure(text=f"结余: ¥{balance:.2f}")

    def show_message(self, message, is_error=False):
        color = "#e74c3c" if is_error else "#27ae60"
        self.message_label.configure(text=message, text_color=color)

    def show_add_dialog(self, categories, callback, existing_bill=None):
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("新增账单" if not existing_bill else "编辑账单")
        dialog.geometry("420x500")
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()

        type_var = ctk.StringVar(value="expense")
        type_frame = ctk.CTkFrame(dialog)
        type_frame.pack(fill=ctk.X, pady=10, padx=20)
        expense_radio = ctk.CTkRadioButton(type_frame, text="支出", variable=type_var, value="expense")
        expense_radio.pack(side=ctk.LEFT, padx=30)
        income_radio = ctk.CTkRadioButton(type_frame, text="收入", variable=type_var, value="income")
        income_radio.pack(side=ctk.LEFT, padx=30)

        category_label = ctk.CTkLabel(dialog, text="分类")
        category_label.pack(pady=(10, 5))
        category_var = ctk.StringVar()
        category_combobox = ctk.CTkComboBox(dialog, variable=category_var, width=340, 
                                            values=[cat[1] for cat in categories])
        category_combobox.pack(pady=5)

        amount_label = ctk.CTkLabel(dialog, text="金额")
        amount_label.pack(pady=(10, 5))
        amount_entry = ctk.CTkEntry(dialog, width=340)
        amount_entry.pack(pady=5)

        payment_label = ctk.CTkLabel(dialog, text="付款方式")
        payment_label.pack(pady=(10, 5))
        payment_var = ctk.StringVar()
        payment_combobox = ctk.CTkComboBox(dialog, variable=payment_var, width=340,
                                           values=PAYMENT_METHODS)
        payment_combobox.pack(pady=5)

        date_label = ctk.CTkLabel(dialog, text="日期")
        date_label.pack(pady=(10, 5))
        date_entry = ctk.CTkEntry(dialog, width=340)
        date_entry.pack(pady=5)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        remark_label = ctk.CTkLabel(dialog, text="备注")
        remark_label.pack(pady=(10, 5))
        remark_entry = ctk.CTkEntry(dialog, width=340)
        remark_entry.pack(pady=5)

        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(fill=ctk.X, pady=15)

        if existing_bill:
            bill_id, type_, category_id, category_name, amount, remark, payment_method, date = existing_bill
            type_var.set(type_)
            category_var.set(category_name)
            amount_entry.insert(0, str(amount))
            payment_var.set(payment_method)
            date_entry.delete(0, ctk.END)
            date_entry.insert(0, date)
            remark_entry.insert(0, remark or "")

        def on_ok():
            type_val = type_var.get()
            category_name = category_var.get()
            amount_val = amount_entry.get().strip()
            payment_val = payment_var.get()
            date_val = date_entry.get().strip()
            remark_val = remark_entry.get().strip()

            if not category_name:
                self.show_message("请选择分类", is_error=True)
                return
            if not amount_val:
                self.show_message("请输入金额", is_error=True)
                return

            category_id = next((cat[0] for cat in categories if cat[1] == category_name), None)
            callback(type_val, category_id, amount_val, remark_val, payment_val, date_val, 
                     existing_bill[0] if existing_bill else None)
            dialog.destroy()

        ok_button = ctk.CTkButton(button_frame, text="确定", width=120, height=40,
                                  fg_color=ACCENT_COLOR, hover_color="#2980b9",
                                  command=on_ok)
        ok_button.pack(side=ctk.LEFT, padx=40)

        cancel_button = ctk.CTkButton(button_frame, text="取消", width=120, height=40,
                                      fg_color="#95a5a6", hover_color="#7f8c8d",
                                      command=dialog.destroy)
        cancel_button.pack(side=ctk.RIGHT, padx=40)

    def on_edit(self, bill_id):
        if self.edit_callback:
            self.edit_callback(bill_id)

    def on_delete(self, bill_id):
        if self.delete_callback:
            self.delete_callback(bill_id)

    def set_edit_callback(self, callback):
        self.edit_callback = callback

    def set_delete_callback(self, callback):
        self.delete_callback = callback

    def get_frame(self):
        return self.frame

    def show_statistics_dialog(self, statistics_data):
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("数据统计")
        dialog.geometry("900x700")
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()

        notebook = ctk.CTkTabview(dialog, width=880, height=650)
        notebook.pack(pady=10)

        notebook.add("收支概览")
        notebook.add("月度统计")
        notebook.add("年度统计")
        notebook.add("支出分类占比")
        notebook.add("收支趋势")

        summary_frame = ctk.CTkFrame(notebook.tab("收支概览"))
        summary_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        total_income = statistics_data.get('total_income', 0)
        total_expense = statistics_data.get('total_expense', 0)
        balance = total_income - total_expense

        income_card = ctk.CTkFrame(summary_frame, fg_color="#27ae60", corner_radius=10)
        income_card.pack(fill=ctk.X, pady=10)
        income_label = ctk.CTkLabel(income_card, text=f"总收入: ¥{total_income:.2f}", 
                                    text_color="white", font=ctk.CTkFont(size=24, weight="bold"))
        income_label.pack(pady=20, padx=20)

        expense_card = ctk.CTkFrame(summary_frame, fg_color="#e74c3c", corner_radius=10)
        expense_card.pack(fill=ctk.X, pady=10)
        expense_label = ctk.CTkLabel(expense_card, text=f"总支出: ¥{total_expense:.2f}", 
                                     text_color="white", font=ctk.CTkFont(size=24, weight="bold"))
        expense_label.pack(pady=20, padx=20)

        balance_card = ctk.CTkFrame(summary_frame, fg_color=ACCENT_COLOR, corner_radius=10)
        balance_card.pack(fill=ctk.X, pady=10)
        balance_label = ctk.CTkLabel(balance_card, text=f"结余: ¥{balance:.2f}", 
                                     text_color="white", font=ctk.CTkFont(size=24, weight="bold"))
        balance_label.pack(pady=20, padx=20)

        monthly_frame = ctk.CTkFrame(notebook.tab("月度统计"))
        monthly_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
        monthly_scroll = ctk.CTkScrollableFrame(monthly_frame)
        monthly_scroll.pack(fill=ctk.BOTH, expand=True)

        monthly_data = statistics_data.get('monthly_data', [])
        for month_data in monthly_data:
            month, income, expense = month_data
            row_frame = ctk.CTkFrame(monthly_scroll)
            row_frame.pack(fill=ctk.X, pady=5)
            
            month_label = ctk.CTkLabel(row_frame, text=f"{month}月", width=80)
            month_label.pack(side=ctk.LEFT, padx=10)
            
            income_label = ctk.CTkLabel(row_frame, text=f"收入: ¥{income:.2f}", width=150, text_color="#27ae60")
            income_label.pack(side=ctk.LEFT, padx=10)
            
            expense_label = ctk.CTkLabel(row_frame, text=f"支出: ¥{expense:.2f}", width=150, text_color="#e74c3c")
            expense_label.pack(side=ctk.LEFT, padx=10)
            
            balance_label = ctk.CTkLabel(row_frame, text=f"结余: ¥{(income - expense):.2f}", width=150)
            balance_label.pack(side=ctk.LEFT, padx=10)

        yearly_frame = ctk.CTkFrame(notebook.tab("年度统计"))
        yearly_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        yearly_data = statistics_data.get('yearly_data', [])
        for year_data in yearly_data:
            year, income, expense = year_data
            row_frame = ctk.CTkFrame(yearly_frame)
            row_frame.pack(fill=ctk.X, pady=10)
            
            year_label = ctk.CTkLabel(row_frame, text=f"{year}年", width=100, font=ctk.CTkFont(size=16, weight="bold"))
            year_label.pack(side=ctk.LEFT, padx=10)
            
            income_label = ctk.CTkLabel(row_frame, text=f"收入: ¥{income:.2f}", width=200, text_color="#27ae60", font=ctk.CTkFont(size=14))
            income_label.pack(side=ctk.LEFT, padx=10)
            
            expense_label = ctk.CTkLabel(row_frame, text=f"支出: ¥{expense:.2f}", width=200, text_color="#e74c3c", font=ctk.CTkFont(size=14))
            expense_label.pack(side=ctk.LEFT, padx=10)

        category_frame = ctk.CTkFrame(notebook.tab("支出分类占比"))
        category_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
        category_scroll = ctk.CTkScrollableFrame(category_frame)
        category_scroll.pack(fill=ctk.BOTH, expand=True)

        category_data = statistics_data.get('category_data', [])
        total_expense_for_categories = sum(item[1] for item in category_data)
        colors = ["#e74c3c", "#f39c12", "#9b59b6", "#3498db", "#1abc9c", "#2ecc71", "#e91e63", "#00bcd4"]
        
        for i, (category_name, amount) in enumerate(category_data):
            percentage = (amount / total_expense_for_categories * 100) if total_expense_for_categories > 0 else 0
            row_frame = ctk.CTkFrame(category_scroll)
            row_frame.pack(fill=ctk.X, pady=5)
            
            cat_label = ctk.CTkLabel(row_frame, text=category_name, width=120)
            cat_label.pack(side=ctk.LEFT, padx=10)
            
            bar_frame = ctk.CTkFrame(row_frame, width=300, height=20)
            bar_frame.pack(side=ctk.LEFT, padx=10)
            bar_fill = ctk.CTkFrame(bar_frame, width=int(percentage * 3), height=20, fg_color=colors[i % len(colors)])
            bar_fill.pack(side=ctk.LEFT)
            
            amount_label = ctk.CTkLabel(row_frame, text=f"¥{amount:.2f}", width=100)
            amount_label.pack(side=ctk.LEFT, padx=10)
            
            percent_label = ctk.CTkLabel(row_frame, text=f"{percentage:.1f}%", width=60)
            percent_label.pack(side=ctk.LEFT, padx=10)

        trend_frame = ctk.CTkFrame(notebook.tab("收支趋势"))
        trend_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)
        trend_scroll = ctk.CTkScrollableFrame(trend_frame)
        trend_scroll.pack(fill=ctk.BOTH, expand=True)

        monthly_trend = statistics_data.get('monthly_data', [])
        max_amount = max(max(item[1], item[2]) for item in monthly_trend) if monthly_trend else 1
        
        for month, income, expense in monthly_trend:
            row_frame = ctk.CTkFrame(trend_scroll)
            row_frame.pack(fill=ctk.X, pady=10)
            
            month_label = ctk.CTkLabel(row_frame, text=f"{month}月", width=60)
            month_label.pack(side=ctk.LEFT, padx=10)
            
            income_bar_frame = ctk.CTkFrame(row_frame, width=300, height=25, bg_color="#ecf0f1")
            income_bar_frame.pack(side=ctk.LEFT, padx=10)
            income_bar = ctk.CTkFrame(income_bar_frame, width=int(income / max_amount * 300), height=25, fg_color="#27ae60")
            income_bar.pack(side=ctk.LEFT)
            
            expense_bar_frame = ctk.CTkFrame(row_frame, width=300, height=25, bg_color="#ecf0f1")
            expense_bar_frame.pack(side=ctk.LEFT, padx=10)
            expense_bar = ctk.CTkFrame(expense_bar_frame, width=int(expense / max_amount * 300), height=25, fg_color="#e74c3c")
            expense_bar.pack(side=ctk.LEFT)
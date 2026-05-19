import customtkinter as ctk
from config import ACCENT_COLOR


class CategoryView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        self.header_frame = ctk.CTkFrame(self.frame)
        self.header_frame.pack(fill=ctk.X, pady=10)

        self.add_button = ctk.CTkButton(self.header_frame, text="新增分类", width=120, height=35,
                                        fg_color=ACCENT_COLOR, hover_color="#2980b9")
        self.add_button.pack(side=ctk.RIGHT)

        self.type_var = ctk.StringVar(value="expense")
        self.expense_radio = ctk.CTkRadioButton(self.header_frame, text="支出分类", 
                                                variable=self.type_var, value="expense")
        self.expense_radio.pack(side=ctk.LEFT, padx=10)
        self.income_radio = ctk.CTkRadioButton(self.header_frame, text="收入分类",
                                               variable=self.type_var, value="income")
        self.income_radio.pack(side=ctk.LEFT, padx=10)

        self.search_entry = ctk.CTkEntry(self.header_frame, placeholder_text="搜索分类名称", width=150)
        self.search_entry.pack(side=ctk.RIGHT, padx=10)
        
        self.search_button = ctk.CTkButton(self.header_frame, text="搜索", width=60, height=25,
                                           fg_color="#95a5a6", hover_color="#7f8c8d")
        self.search_button.pack(side=ctk.RIGHT, padx=5)

        self.tree_frame = ctk.CTkFrame(self.frame)
        self.tree_frame.pack(fill=ctk.BOTH, expand=True)

        self.tree = ctk.CTkScrollableFrame(self.tree_frame)
        self.tree.pack(fill=ctk.BOTH, expand=True)

        self.message_label = ctk.CTkLabel(self.frame, text="", text_color="#27ae60", font=ctk.CTkFont(size=12))
        self.message_label.pack(pady=10)

        self.categories = []
        self.edit_mode = False
        self.editing_id = None

    def get_selected_type(self):
        return self.type_var.get()

    def get_search_keyword(self):
        return self.search_entry.get().strip()

    def set_add_command(self, command):
        self.add_button.configure(command=command)

    def set_search_command(self, command):
        self.search_button.configure(command=command)

    def set_type_change_command(self, command):
        self.expense_radio.configure(command=command)
        self.income_radio.configure(command=command)

    def clear_categories(self):
        for widget in self.tree.winfo_children():
            widget.destroy()

    def display_categories(self, categories):
        self.clear_categories()
        self.categories = categories
        
        for cat in categories:
            cat_id, name, type_ = cat
            row_frame = ctk.CTkFrame(self.tree)
            row_frame.pack(fill=ctk.X, pady=2)

            name_label = ctk.CTkLabel(row_frame, text=name, width=200, anchor=ctk.W)
            name_label.pack(side=ctk.LEFT, padx=10)

            edit_button = ctk.CTkButton(row_frame, text="编辑", width=60, height=25,
                                        fg_color="#f39c12", hover_color="#d68910",
                                        command=lambda cid=cat_id: self.on_edit(cid))
            edit_button.pack(side=ctk.RIGHT, padx=5)

            delete_button = ctk.CTkButton(row_frame, text="删除", width=60, height=25,
                                          fg_color="#e74c3c", hover_color="#c0392b",
                                          command=lambda cid=cat_id: self.on_delete(cid))
            delete_button.pack(side=ctk.RIGHT, padx=5)

    def show_message(self, message, is_error=False):
        color = "#e74c3c" if is_error else "#27ae60"
        self.message_label.configure(text=message, text_color=color)

    def show_add_dialog(self, callback, existing_name="", category_id=None):
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("新增分类" if not category_id else "编辑分类")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()

        name_label = ctk.CTkLabel(dialog, text="分类名称")
        name_label.pack(pady=(20, 5))
        
        name_entry = ctk.CTkEntry(dialog, width=240)
        name_entry.pack(pady=5)
        if existing_name:
            name_entry.insert(0, existing_name)

        def on_ok():
            name = name_entry.get().strip()
            if name:
                callback(name, category_id)
                dialog.destroy()

        ok_button = ctk.CTkButton(dialog, text="确定", width=100, command=on_ok)
        ok_button.pack(pady=20)

        cancel_button = ctk.CTkButton(dialog, text="取消", width=100, 
                                      fg_color="transparent", border_color="gray",
                                      command=dialog.destroy)
        cancel_button.pack(pady=5)

    def on_edit(self, category_id):
        if self.edit_callback:
            for cat in self.categories:
                if cat[0] == category_id:
                    self.show_add_dialog(self.edit_callback, cat[1], category_id)
                    break

    def on_delete(self, category_id):
        if self.delete_callback:
            self.delete_callback(category_id)

    def set_edit_callback(self, callback):
        self.edit_callback = callback

    def set_delete_callback(self, callback):
        self.delete_callback = callback

    def get_frame(self):
        return self.frame
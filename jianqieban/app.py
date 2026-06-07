import customtkinter as ctk
from customtkinter import CTkFont
import tkinter as tk
from tkinter import messagebox
from database import get_all_records, delete_record, delete_all_records, toggle_favorite, get_record_count
from utils import set_clipboard_content, truncate_content
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FONT_FAMILY

class ClipboardHistoryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("剪贴板历史管理器")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(True, True)
        
        self.search_query = tk.StringVar()
        self.search_query.trace('w', self.on_search_change)
        
        self.selected_items = []
        self.setup_ui()
        self.update_history()
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_ui(self):
        default_font = CTkFont(family=FONT_FAMILY, size=12)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        top_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(top_frame, textvariable=self.search_query, font=default_font, placeholder_text="搜索历史记录...")
        self.search_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.clear_button = ctk.CTkButton(top_frame, text="清空历史", command=self.confirm_clear_all, font=default_font)
        self.clear_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.history_frame = ctk.CTkFrame(self)
        self.history_frame.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        self.history_frame.grid_columnconfigure(0, weight=1)
        self.history_frame.grid_rowconfigure(0, weight=1)
        
        self.history_canvas = ctk.CTkCanvas(self.history_frame, bg="#2a2a2a")
        self.scrollbar = ctk.CTkScrollbar(self.history_frame, command=self.history_canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.history_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.history_canvas.configure(
                scrollregion=self.history_canvas.bbox("all")
            )
        )
        
        self.history_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.history_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.history_canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.history_canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
        
        status_frame = ctk.CTkFrame(self)
        status_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        self.status_label = ctk.CTkLabel(status_frame, text="总记录数: 0 | 选中: 0", font=default_font)
        self.status_label.grid(row=0, column=0, padx=5, pady=5)
    
    def on_mouse_wheel(self, event):
        self.history_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def on_search_change(self, *args):
        self.update_history()
    
    def update_history(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        records = get_all_records(self.search_query.get())
        self.selected_items = []
        
        for record in records:
            self.create_history_item(record)
        
        self.update_status()
    
    def create_history_item(self, record):
        record_id, content, copy_time, is_favorite = record
        
        item_frame = ctk.CTkFrame(self.scrollable_frame)
        item_frame.grid(sticky="ew", padx=5, pady=2)
        item_frame.grid_columnconfigure(1, weight=1)
        item_frame.bind("<Button-1>", lambda e, rid=record_id: self.on_item_click(e, rid))
        item_frame.bind("<Double-1>", lambda e, rid=record_id, cnt=content: self.on_item_double_click(rid, cnt))
        
        favorite_label = ctk.CTkLabel(item_frame, text="★" if is_favorite else "☆", width=25, font=CTkFont(family=FONT_FAMILY, size=14))
        favorite_label.grid(row=0, column=0, padx=5, pady=3, sticky="w")
        
        content_label = ctk.CTkLabel(item_frame, text=truncate_content(content), anchor="w", font=CTkFont(family=FONT_FAMILY, size=12), wraplength=450)
        content_label.grid(row=0, column=1, padx=5, pady=3, sticky="w")
        
        time_label = ctk.CTkLabel(item_frame, text=copy_time, font=CTkFont(family=FONT_FAMILY, size=11, slant="italic"), text_color="gray")
        time_label.grid(row=0, column=2, padx=5, pady=3)
        
        item_frame.context_menu = self.create_context_menu(record_id, content)
        item_frame.bind("<Button-3>", lambda e, menu=item_frame.context_menu: self.show_context_menu(e, menu))
    
    def create_context_menu(self, record_id, content):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="复制这条", command=lambda: self.copy_to_clipboard(content))
        menu.add_command(label="删除这条", command=lambda: self.delete_single_record(record_id))
        menu.add_command(label="收藏/取消收藏", command=lambda: self.toggle_record_favorite(record_id))
        menu.add_separator()
        menu.add_command(label="清空所有", command=self.confirm_clear_all)
        return menu
    
    def show_context_menu(self, event, menu):
        menu.post(event.x_root, event.y_root)
    
    def on_item_click(self, event, record_id):
        pass
    
    def on_item_double_click(self, record_id, content):
        self.copy_to_clipboard(content)
    
    def copy_to_clipboard(self, content):
        if set_clipboard_content(content):
            self.show_notification("已复制")
    
    def show_notification(self, message):
        notification = ctk.CTkToplevel(self)
        notification.overrideredirect(True)
        notification.geometry("+{}+{}".format(
            self.winfo_screenwidth() - 150,
            self.winfo_screenheight() - 100
        ))
        label = ctk.CTkLabel(notification, text=message, font=CTkFont(family=FONT_FAMILY, size=12), bg_color="#2a2a2a", fg_color="#2a2a2a")
        label.pack(padx=15, pady=10)
        notification.after(2000, notification.destroy)
    
    def delete_single_record(self, record_id):
        delete_record(record_id)
        self.update_history()
    
    def confirm_clear_all(self):
        if messagebox.askyesno("确认清空", "确定要清空所有历史记录吗？"):
            delete_all_records()
            self.update_history()
    
    def toggle_record_favorite(self, record_id):
        toggle_favorite(record_id)
        self.update_history()
    
    def update_status(self):
        total = get_record_count()
        selected = len(self.selected_items)
        self.status_label.configure(text=f"总记录数: {total} | 选中: {selected}")
    
    def on_close(self):
        self.withdraw()
    
    def show(self):
        self.deiconify()
        self.lift()
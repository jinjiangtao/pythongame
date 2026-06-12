import customtkinter as ctk
from typing import List, Dict, Any
from config_manager import ConfigManager


def get_display_name(item: Dict[str, Any]) -> str:
    headers = item.get("headers", {})
    for key, value in headers.items():
        if key.lower() == 'x-name':
            return value
    
    method = item.get("method", "GET")
    url = item.get("url", "")
    display_url = url[:30] + "..." if len(url) > 30 else url
    return f"{method} {display_url}"


class HistoryPanel(ctk.CTkFrame):
    def __init__(self, parent, on_select_callback):
        super().__init__(parent)
        
        self.on_select_callback = on_select_callback
        self.config_manager = ConfigManager()
        self.history = self.config_manager.load_history()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.tree = ctk.CTkScrollableFrame(self)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.history_label = ctk.CTkLabel(self.tree, text="History", font=("Arial", 12, "bold"))
        self.history_label.grid(row=0, column=0, sticky="w", pady=5)
        
        self.history_items = []
        self.load_history_items()
        
        self.clear_button = ctk.CTkButton(self, text="Clear History", command=self.clear_history)
        self.clear_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    def load_history_items(self):
        for widget in self.tree.winfo_children():
            if widget != self.history_label:
                widget.destroy()
        
        self.history_items.clear()
        
        for i, item in enumerate(self.history):
            frame = ctk.CTkFrame(self.tree)
            frame.grid(row=i + 1, column=0, sticky="ew", pady=2)
            frame.grid_columnconfigure(1, weight=1)
            
            display_name = get_display_name(item)
            
            name_label = ctk.CTkLabel(frame, text=display_name, anchor="w")
            name_label.grid(row=0, column=0, padx=5, sticky="ew", columnspan=2)
            
            frame.bind("<Button-1>", lambda e, item=item: self.on_select(item))
            name_label.bind("<Button-1>", lambda e, item=item: self.on_select(item))
            
            self.history_items.append(frame)

    def on_select(self, item):
        if self.on_select_callback:
            self.on_select_callback(item)

    def add_history(self, request_data: Dict[str, Any]):
        import time
        item = {
            "id": int(time.time()),
            "method": request_data["method"],
            "url": request_data["url"],
            "headers": request_data["headers"],
            "body_type": request_data["body_type"],
            "body": request_data["body"],
            "timeout": request_data["timeout"],
            "timestamp": time.time()
        }
        
        self.history.insert(0, item)
        if len(self.history) > 50:
            self.history = self.history[:50]
        
        self.config_manager.save_history(self.history)
        self.load_history_items()

    def clear_history(self):
        self.history = []
        self.config_manager.save_history(self.history)
        self.load_history_items()

    def get_history(self) -> List[Dict[str, Any]]:
        return self.history

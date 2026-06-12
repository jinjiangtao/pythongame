import customtkinter as ctk
from typing import Dict


class HeadersEditor(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.headers: Dict[str, str] = {}
        self.header_rows = []
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        
        self.add_button = ctk.CTkButton(self, text="+", width=30, 
                                        command=self.add_header_row)
        self.add_button.grid(row=0, column=0, columnspan=3, pady=5, sticky="w")
        
        self.add_header_row()

    def add_header_row(self, key: str = "", value: str = ""):
        row_index = len(self.header_rows)
        
        key_entry = ctk.CTkEntry(self, placeholder_text="Key")
        key_entry.insert(0, key)
        key_entry.grid(row=row_index + 1, column=0, padx=5, pady=2, sticky="ew")
        
        value_entry = ctk.CTkEntry(self, placeholder_text="Value")
        value_entry.insert(0, value)
        value_entry.grid(row=row_index + 1, column=1, padx=5, pady=2, sticky="ew")
        
        remove_button = ctk.CTkButton(self, text="-", width=30,
                                      command=lambda: self.remove_header_row(row_index))
        remove_button.grid(row=row_index + 1, column=2, padx=5, pady=2)
        
        self.header_rows.append((key_entry, value_entry, remove_button))

    def remove_header_row(self, index: int):
        if len(self.header_rows) > 1:
            key_entry, value_entry, remove_button = self.header_rows.pop(index)
            key_entry.destroy()
            value_entry.destroy()
            remove_button.destroy()
            self._refresh_rows()

    def _refresh_rows(self):
        for i, (key_entry, value_entry, remove_button) in enumerate(self.header_rows):
            key_entry.grid(row=i + 1, column=0)
            value_entry.grid(row=i + 1, column=1)
            remove_button.grid(row=i + 1, column=2)

    def get_headers(self) -> Dict[str, str]:
        headers = {}
        for key_entry, value_entry, _ in self.header_rows:
            key = key_entry.get().strip()
            value = value_entry.get().strip()
            if key:
                headers[key] = value
        return headers

    def set_headers(self, headers: Dict[str, str]):
        for key_entry, value_entry, remove_button in self.header_rows:
            key_entry.destroy()
            value_entry.destroy()
            remove_button.destroy()
        
        self.header_rows.clear()
        
        if not headers:
            self.add_header_row()
        else:
            for key, value in headers.items():
                self.add_header_row(key, value)

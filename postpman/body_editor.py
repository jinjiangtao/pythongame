import customtkinter as ctk
from typing import Dict, Any


class BodyEditor(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.body_type = ctk.StringVar(value="none")
        self.body_items = []
        
        self.type_frame = ctk.CTkFrame(self)
        self.type_frame.grid(row=0, column=0, sticky="ew", pady=5)
        self.type_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        types = ["None", "form-data", "x-www-form-urlencoded", "raw"]
        for i, t in enumerate(types):
            radio = ctk.CTkRadioButton(self.type_frame, text=t, 
                                       variable=self.body_type, value=t.lower(),
                                       command=self.on_type_change)
            radio.grid(row=0, column=i, padx=5)
        
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        self.raw_textbox = ctk.CTkTextbox(self.content_frame, wrap="word")
        self.raw_textbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.raw_textbox.insert("0.0", '{\n  "key": "value"\n}')
        self.raw_textbox.pack_forget()
        
        self.form_frame = ctk.CTkFrame(self.content_frame)
        self.form_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.form_frame.grid_columnconfigure(0, weight=1)
        self.form_frame.grid_columnconfigure(1, weight=1)
        self.form_frame.grid_columnconfigure(2, weight=0)
        
        self.add_form_button = ctk.CTkButton(self.form_frame, text="+", width=30,
                                             command=self.add_form_row)
        self.add_form_button.grid(row=0, column=0, columnspan=3, pady=5, sticky="w")
        
        self.add_form_row()
        
        self.on_type_change()

    def on_type_change(self):
        t = self.body_type.get()
        
        if t == "none":
            self.form_frame.pack_forget()
            self.raw_textbox.pack_forget()
        elif t == "form-data" or t == "x-www-form-urlencoded":
            self.raw_textbox.pack_forget()
            self.form_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        elif t == "raw":
            self.form_frame.grid_forget()
            self.raw_textbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def add_form_row(self, key: str = "", value: str = ""):
        row_index = len(self.body_items)
        
        key_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Key")
        key_entry.insert(0, key)
        key_entry.grid(row=row_index + 1, column=0, padx=5, pady=2, sticky="ew")
        
        value_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Value")
        value_entry.insert(0, value)
        value_entry.grid(row=row_index + 1, column=1, padx=5, pady=2, sticky="ew")
        
        remove_button = ctk.CTkButton(self.form_frame, text="-", width=30,
                                      command=lambda: self.remove_form_row(row_index))
        remove_button.grid(row=row_index + 1, column=2, padx=5, pady=2)
        
        self.body_items.append((key_entry, value_entry, remove_button))

    def remove_form_row(self, index: int):
        if len(self.body_items) > 1:
            key_entry, value_entry, remove_button = self.body_items.pop(index)
            key_entry.destroy()
            value_entry.destroy()
            remove_button.destroy()
            self._refresh_rows()

    def _refresh_rows(self):
        for i, (key_entry, value_entry, remove_button) in enumerate(self.body_items):
            key_entry.grid(row=i + 1, column=0)
            value_entry.grid(row=i + 1, column=1)
            remove_button.grid(row=i + 1, column=2)

    def get_body(self) -> Any:
        t = self.body_type.get()
        
        if t == "none":
            return {}
        elif t == "form-data" or t == "x-www-form-urlencoded":
            body = {}
            for key_entry, value_entry, _ in self.body_items:
                key = key_entry.get().strip()
                value = value_entry.get().strip()
                if key:
                    body[key] = value
            return body
        elif t == "raw":
            return self.raw_textbox.get("0.0", "end-1c")
        return {}

    def get_body_type(self) -> str:
        return self.body_type.get()

    def set_body(self, body: Any, body_type: str = "none"):
        self.body_type.set(body_type)
        
        if body_type == "none":
            return
        elif body_type == "form-data" or body_type == "x-www-form-urlencoded":
            for key_entry, value_entry, remove_button in self.body_items:
                key_entry.destroy()
                value_entry.destroy()
                remove_button.destroy()
            self.body_items.clear()
            
            if isinstance(body, dict):
                for key, value in body.items():
                    self.add_form_row(key, value)
            else:
                self.add_form_row()
        elif body_type == "raw":
            self.raw_textbox.delete("0.0", "end")
            if isinstance(body, dict):
                import json
                self.raw_textbox.insert("0.0", json.dumps(body, indent=2))
            else:
                self.raw_textbox.insert("0.0", str(body))
        
        self.on_type_change()

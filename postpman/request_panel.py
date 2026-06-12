import customtkinter as ctk
from headers_editor import HeadersEditor
from body_editor import BodyEditor


class RequestPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.method_var = ctk.StringVar(value="GET")
        self.methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        
        self.grid_columnconfigure(0, weight=1)
        
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(2, weight=0)
        self.top_frame.grid_columnconfigure(3, weight=0)
        
        self.method_menu = ctk.CTkOptionMenu(self.top_frame, values=self.methods, 
                                             variable=self.method_var)
        self.method_menu.grid(row=0, column=0, padx=5)
        
        self.url_entry = ctk.CTkEntry(self.top_frame, placeholder_text="Enter URL")
        self.url_entry.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.timeout_label = ctk.CTkLabel(self.top_frame, text="Timeout:")
        self.timeout_label.grid(row=0, column=2, padx=5)
        
        self.timeout_entry = ctk.CTkEntry(self.top_frame, width=60, placeholder_text="30")
        self.timeout_entry.insert(0, "30")
        self.timeout_entry.grid(row=0, column=3, padx=5)
        
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.headers_tab = self.tabview.add("Headers")
        self.body_tab = self.tabview.add("Body")
        
        self.headers_tab.grid_rowconfigure(0, weight=1)
        self.headers_tab.grid_columnconfigure(0, weight=1)
        
        self.body_tab.grid_rowconfigure(0, weight=1)
        self.body_tab.grid_columnconfigure(0, weight=1)
        
        self.headers_editor = HeadersEditor(self.headers_tab)
        self.headers_editor.grid(row=0, column=0, sticky="nsew")
        
        self.body_editor = BodyEditor(self.body_tab)
        self.body_editor.grid(row=0, column=0, sticky="nsew")
        
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.send_button = ctk.CTkButton(self.button_frame, text="Send", command=self.on_send)
        self.send_button.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", 
                                           command=self.on_cancel, state="disabled")
        self.cancel_button.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.import_curl_button = ctk.CTkButton(self.button_frame, text="Import cURL", 
                                                 command=self.on_import_curl)
        self.import_curl_button.grid(row=0, column=2, padx=5, sticky="ew")
        
        self.clear_button = ctk.CTkButton(self.button_frame, text="Clear", command=self.on_clear)
        self.clear_button.grid(row=0, column=3, padx=5, sticky="ew")
        
        self.grid_rowconfigure(1, weight=1)
        
        self.send_callback = None
        self.cancel_callback = None
        self.import_curl_callback = None

    def set_send_callback(self, callback):
        self.send_callback = callback

    def set_cancel_callback(self, callback):
        self.cancel_callback = callback

    def set_import_curl_callback(self, callback):
        self.import_curl_callback = callback

    def on_send(self):
        if self.send_callback:
            self.send_button.configure(state="disabled")
            self.cancel_button.configure(state="normal")
            self.send_callback(self.get_request_data())

    def on_cancel(self):
        if self.cancel_callback:
            self.cancel_callback()
            self.send_button.configure(state="normal")
            self.cancel_button.configure(state="disabled")

    def on_import_curl(self):
        if self.import_curl_callback:
            self.import_curl_callback()

    def on_clear(self):
        self.method_var.set("GET")
        self.url_entry.delete(0, "end")
        self.timeout_entry.delete(0, "end")
        self.timeout_entry.insert(0, "30")
        self.headers_editor.set_headers({})
        self.body_editor.set_body({}, "none")

    def get_request_data(self):
        return {
            "method": self.method_var.get(),
            "url": self.url_entry.get(),
            "headers": self.headers_editor.get_headers(),
            "body": self.body_editor.get_body(),
            "body_type": self.body_editor.get_body_type(),
            "timeout": int(self.timeout_entry.get() or 30)
        }

    def set_request_data(self, data):
        self.method_var.set(data.get("method", "GET"))
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, data.get("url", ""))
        self.timeout_entry.delete(0, "end")
        self.timeout_entry.insert(0, str(data.get("timeout", 30)))
        self.headers_editor.set_headers(data.get("headers", {}))
        self.body_editor.set_body(data.get("body", {}), data.get("body_type", "none"))

    def set_sending_state(self, sending: bool):
        if sending:
            self.send_button.configure(state="disabled")
            self.cancel_button.configure(state="normal")
        else:
            self.send_button.configure(state="normal")
            self.cancel_button.configure(state="disabled")

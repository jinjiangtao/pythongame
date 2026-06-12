import customtkinter as ctk
import json
from http_client import ResponseData


class ResponsePanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.body_tab = self.tabview.add("Body")
        self.headers_tab = self.tabview.add("Headers")
        
        self.body_tab.grid_rowconfigure(0, weight=1)
        self.body_tab.grid_columnconfigure(0, weight=1)
        
        self.headers_tab.grid_rowconfigure(0, weight=1)
        self.headers_tab.grid_columnconfigure(0, weight=1)
        
        self.body_textbox = ctk.CTkTextbox(self.body_tab, wrap="word", state="disabled")
        self.body_textbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.headers_textbox = ctk.CTkTextbox(self.headers_tab, wrap="word", state="disabled")
        self.headers_textbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.info_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.status_label = ctk.CTkLabel(self.info_frame, text="Status: -")
        self.status_label.grid(row=0, column=0, padx=5)
        
        self.time_label = ctk.CTkLabel(self.info_frame, text="Time: -")
        self.time_label.grid(row=0, column=1, padx=5)
        
        self.size_label = ctk.CTkLabel(self.info_frame, text="Size: -")
        self.size_label.grid(row=0, column=2, padx=5)
        
        self.error_label = ctk.CTkLabel(self.info_frame, text="", text_color="red")
        self.error_label.grid(row=0, column=3, padx=5)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def display_response(self, response_data: ResponseData):
        self.body_textbox.configure(state="normal")
        self.headers_textbox.configure(state="normal")
        
        if response_data.error:
            self.status_label.configure(text=f"Status: Error")
            self.error_label.configure(text=response_data.error)
            self.body_textbox.delete("0.0", "end")
            self.body_textbox.insert("0.0", response_data.error)
        else:
            self.status_label.configure(text=f"Status: {response_data.status_code}")
            self.error_label.configure(text="")
            
            status_color = "green" if 200 <= response_data.status_code < 300 else "orange" if 300 <= response_data.status_code < 400 else "red"
            self.status_label.configure(text_color=status_color)
            
            self.time_label.configure(text=f"Time: {response_data.response_time:.2f}s")
            
            body_size = len(str(response_data.body))
            if body_size < 1024:
                size_str = f"{body_size} B"
            elif body_size < 1024 * 1024:
                size_str = f"{body_size / 1024:.2f} KB"
            else:
                size_str = f"{body_size / (1024 * 1024):.2f} MB"
            self.size_label.configure(text=f"Size: {size_str}")
            
            headers_text = "\n".join(f"{k}: {v}" for k, v in response_data.headers.items())
            self.headers_textbox.delete("0.0", "end")
            self.headers_textbox.insert("0.0", headers_text)
            
            body_text = str(response_data.body)
            try:
                parsed = json.loads(body_text)
                body_text = json.dumps(parsed, indent=2, ensure_ascii=False)
            except:
                pass
            
            self.body_textbox.delete("0.0", "end")
            self.body_textbox.insert("0.0", body_text)
        
        self.body_textbox.configure(state="disabled")
        self.headers_textbox.configure(state="disabled")

    def clear(self):
        self.body_textbox.configure(state="normal")
        self.headers_textbox.configure(state="normal")
        
        self.body_textbox.delete("0.0", "end")
        self.headers_textbox.delete("0.0", "end")
        
        self.status_label.configure(text="Status: -", text_color="white")
        self.time_label.configure(text="Time: -")
        self.size_label.configure(text="Size: -")
        self.error_label.configure(text="")
        
        self.body_textbox.configure(state="disabled")
        self.headers_textbox.configure(state="disabled")

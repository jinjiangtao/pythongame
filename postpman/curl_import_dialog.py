import customtkinter as ctk
from typing import Optional, Dict, Any
from curl_parser import parse_curl, CurlParser


class CurlImportDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_success_callback):
        super().__init__(parent)
        
        self.on_success_callback = on_success_callback
        self.result: Optional[Dict[str, Any]] = None
        
        self.title("Import cURL Command")
        self.geometry("600x400")
        self.resizable(True, True)
        
        self.transient(parent)
        self.grab_set()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.label = ctk.CTkLabel(self, text="Paste your cURL command below:", 
                                   font=("Arial", 12))
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.textbox = ctk.CTkTextbox(self, wrap="word", font=("Consolas", 11))
        self.textbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 10))
        self.error_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.import_button = ctk.CTkButton(self.button_frame, text="Import", 
                                           command=self.on_import)
        self.import_button.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.cancel_button = ctk.CTkButton(self.button_frame, text="Cancel", 
                                          command=self.on_cancel)
        self.cancel_button.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.focus_set()
        self.textbox.focus_set()
        
        self.bind("<Return>", lambda e: self.on_import())
        self.bind("<Escape>", lambda e: self.on_cancel())
    
    def on_import(self):
        curl_command = self.textbox.get("0.0", "end-1c").strip()
        
        if not curl_command:
            self.error_label.configure(text="Please enter a cURL command")
            return
        
        try:
            result = parse_curl(curl_command)
            self.result = result
            self.error_label.configure(text="")
            
            if self.on_success_callback:
                self.on_success_callback(result)
            
            self.destroy()
            
        except ValueError as e:
            self.error_label.configure(text=str(e))
        except Exception as e:
            self.error_label.configure(text=f"Invalid cURL command format: {str(e)}")
    
    def on_cancel(self):
        self.result = None
        self.destroy()
    
    def get_result(self) -> Optional[Dict[str, Any]]:
        return self.result
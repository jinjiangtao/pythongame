import customtkinter as ctk
from request_panel import RequestPanel
from response_panel import ResponsePanel
from history_panel import HistoryPanel
from http_client import HttpClient
from config_manager import ConfigManager, RequestConfig
from curl_import_dialog import CurlImportDialog
from curl_parser import get_display_name
import os


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("PyPostman - API Testing Tool")
        self.geometry("1200x800")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.http_client = HttpClient(self)
        self.config_manager = ConfigManager()
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.history_panel = HistoryPanel(self, self.on_history_select)
        self.history_panel.grid(row=0, column=0, sticky="nsew")
        self.history_panel.configure(width=250)
        
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        self.request_panel = RequestPanel(self.main_frame)
        self.request_panel.grid(row=0, column=0, sticky="nsew")
        self.request_panel.set_send_callback(self.send_request)
        self.request_panel.set_cancel_callback(self.cancel_request)
        self.request_panel.set_import_curl_callback(self.import_curl)
        
        self.response_panel = ResponsePanel(self.main_frame)
        self.response_panel.grid(row=1, column=0, sticky="nsew")
        
        self.menu_bar = self.create_menu_bar()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_menu_bar(self):
        menubar = ctk.CTkOptionMenu(self, values=["File", "Help"])
        menubar.grid(row=0, column=0, sticky="nw")
        
        file_menu = ctk.CTkFrame(self)
        save_btn = ctk.CTkButton(file_menu, text="Save Request", command=self.save_request)
        save_btn.pack(padx=5, pady=2)
        import_btn = ctk.CTkButton(file_menu, text="Import Request", command=self.import_request)
        import_btn.pack(padx=5, pady=2)
        export_btn = ctk.CTkButton(file_menu, text="Export Request", command=self.export_request)
        export_btn.pack(padx=5, pady=2)
        
        return menubar

    def send_request(self, request_data):
        self.response_panel.clear()
        
        def callback(response_data):
            self.response_panel.display_response(response_data)
            self.request_panel.set_sending_state(False)
            
            if response_data.success:
                self.history_panel.add_history(request_data)
        
        self.http_client.send_request(
            method=request_data["method"],
            url=request_data["url"],
            headers=request_data["headers"],
            body=request_data["body"],
            body_type=request_data["body_type"],
            timeout=request_data["timeout"],
            callback=callback
        )
        
        self.request_panel.set_sending_state(True)

    def cancel_request(self):
        self.http_client.cancel_request()

    def on_history_select(self, item):
        self.request_panel.set_request_data(item)

    def import_curl(self):
        def on_curl_imported(result):
            if result:
                request_data = {
                    "method": result["method"],
                    "url": result["url"],
                    "headers": result["headers"],
                    "body": result["body"],
                    "body_type": result["body_type"],
                    "timeout": 30
                }
                
                self.request_panel.set_request_data(request_data)
                
                self.history_panel.add_history(request_data)
                
                self.show_message("Success", "cURL command imported successfully!")
        
        dialog = CurlImportDialog(self, on_curl_imported)
        self.wait_window(dialog)

    def save_request(self):
        data = self.request_panel.get_request_data()
        if not data["url"]:
            self.show_message("Error", "Please enter a URL first")
            return
        
        import time
        filename = f"request_{int(time.time())}"
        success = self.config_manager.save_request(RequestConfig.from_dict(data), filename)
        
        if success:
            self.show_message("Success", f"Request saved as {filename}.json")
        else:
            self.show_message("Error", "Failed to save request")

    def import_request(self):
        filepath = ctk.filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if filepath:
            config = self.config_manager.import_request(filepath)
            self.request_panel.set_request_data(config.to_dict())
            self.show_message("Success", "Request imported successfully")

    def export_request(self):
        data = self.request_panel.get_request_data()
        if not data["url"]:
            self.show_message("Error", "Please enter a URL first")
            return
        
        filepath = ctk.filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if filepath:
            success = self.config_manager.export_request(RequestConfig.from_dict(data), filepath)
            if success:
                self.show_message("Success", "Request exported successfully")
            else:
                self.show_message("Error", "Failed to export request")

    def show_message(self, title, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("300x150")
        
        label = ctk.CTkLabel(dialog, text=message)
        label.pack(pady=20)
        
        ok_btn = ctk.CTkButton(dialog, text="OK", command=dialog.destroy)
        ok_btn.pack(pady=10)
        
        dialog.transient(self)
        dialog.grab_set()
        self.wait_window(dialog)

    def on_closing(self):
        self.destroy()


if __name__ == "__main__":
    os.makedirs("config", exist_ok=True)
    app = App()
    app.mainloop()

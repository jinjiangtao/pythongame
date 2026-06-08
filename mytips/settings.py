import customtkinter as ctk
from utils import set_startup


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.title("设置")
        self.geometry("400x250")
        self.resizable(False, False)
        
        self._create_widgets()
        self._load_settings()
        
    def _create_widgets(self):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text="开机自动启动", font=("Microsoft YaHei", 14)).grid(row=0, column=0, pady=15, sticky="w")
        
        self.startup_var = ctk.BooleanVar()
        self.startup_switch = ctk.CTkSwitch(frame, variable=self.startup_var, text="")
        self.startup_switch.grid(row=0, column=1, pady=15, padx=10)
        
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(button_frame, text="保存", command=self._save_settings).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="取消", command=self.destroy).pack(side="right", padx=5)
        
    def _load_settings(self):
        startup = self.db.get_setting('startup', 'false')
        self.startup_var.set(startup == 'true')
        
    def _save_settings(self):
        self.db.set_setting('startup', 'true' if self.startup_var.get() else 'false')
        set_startup(self.startup_var.get())
        self.destroy()

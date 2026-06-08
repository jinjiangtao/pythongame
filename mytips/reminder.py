import customtkinter as ctk
from datetime import datetime
from utils import play_reminder_sound


class ReminderWindow(ctk.CTkToplevel):
    def __init__(self, parent, note_id, db, on_save=None):
        super().__init__(parent)
        self.note_id = note_id
        self.db = db
        self.on_save = on_save
        self.title("设置提醒")
        self.geometry("350x300")
        self.resizable(False, False)
        
        self._create_widgets()
        
    def _create_widgets(self):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text="日期", font=("Microsoft YaHei", 12)).grid(row=0, column=0, pady=10, sticky="w")
        self.date_var = ctk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.date_entry = ctk.CTkEntry(frame, textvariable=self.date_var)
        self.date_entry.grid(row=0, column=1, pady=10, padx=10, sticky="ew")
        
        ctk.CTkLabel(frame, text="时间", font=("Microsoft YaHei", 12)).grid(row=1, column=0, pady=10, sticky="w")
        time_frame = ctk.CTkFrame(frame)
        time_frame.grid(row=1, column=1, pady=10, padx=10, sticky="ew")
        
        self.hour_var = ctk.StringVar(value=f"{datetime.now().hour:02d}")
        self.hour_spin = ctk.CTkEntry(time_frame, textvariable=self.hour_var, width=60)
        self.hour_spin.pack(side="left", padx=2)
        
        ctk.CTkLabel(time_frame, text=":", font=("Microsoft YaHei", 14)).pack(side="left")
        
        self.minute_var = ctk.StringVar(value=f"{datetime.now().minute:02d}")
        self.minute_spin = ctk.CTkEntry(time_frame, textvariable=self.minute_var, width=60)
        self.minute_spin.pack(side="left", padx=2)
        
        ctk.CTkButton(frame, text="清除提醒", command=self._clear_reminder).grid(row=2, column=0, columnspan=2, pady=10)
        
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(button_frame, text="保存", command=self._save).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="取消", command=self.destroy).pack(side="right", padx=5)
        
    def _save(self):
        try:
            date_str = self.date_var.get()
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            reminder_str = f"{date_str} {hour:02d}:{minute:02d}:00"
            self.db.update_note(self.note_id, reminder_time=reminder_str)
            if self.on_save:
                self.on_save(reminder_str)
            self.destroy()
        except ValueError:
            pass
        
    def _clear_reminder(self):
        self.db.update_note(self.note_id, reminder_time=None)
        if self.on_save:
            self.on_save(None)
        self.destroy()


class ReminderAlert(ctk.CTkToplevel):
    def __init__(self, parent, note_content, note_window=None):
        super().__init__(parent)
        self.title("提醒")
        self.geometry("400x250")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        
        # 如果有便签窗口，定位在便签附近
        if note_window:
            note_x = note_window.winfo_x()
            note_y = note_window.winfo_y()
            note_width = note_window.winfo_width()
            # 把弹窗显示在便签右边稍微偏移的位置
            self.geometry(f"+{note_x + note_width + 20}+{note_y}")
        
        play_reminder_sound()
        
        self._create_widgets(note_content)
        
    def _create_widgets(self, content):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text="📅 提醒时间到了！", font=("Microsoft YaHei", 18)).pack(pady=10)
        
        text_box = ctk.CTkTextbox(frame, height=100)
        text_box.pack(fill="both", expand=True, pady=10)
        text_box.insert("0.0", content)
        text_box.configure(state="disabled")
        
        ctk.CTkButton(frame, text="知道了", command=self.destroy, width=100).pack(pady=10)

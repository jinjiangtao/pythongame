import customtkinter as ctk
import time

class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("医院门诊挂号系统")
        self.geometry("900x600")
        self.resizable(False, False)
        self.center_window()
        self.create_widgets()
        self.update_status_bar()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 600) // 2
        self.geometry(f"900x600+{x}+{y}")

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_frame = ctk.CTkFrame(self, height=60, corner_radius=10)
        self.top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.top_frame.grid_columnconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(self.top_frame, text="🏥 医院门诊挂号系统", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=15)

        self.theme_switch = ctk.CTkSwitch(self.top_frame, text="深色模式", command=self.toggle_theme)
        self.theme_switch.grid(row=0, column=1, padx=20, pady=15, sticky="e")

        self.main_content = ctk.CTkFrame(self, corner_radius=10)
        self.main_content.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(1, weight=1)
        self.main_content.grid_rowconfigure(0, weight=1)

        self.status_bar = ctk.CTkFrame(self, height=35, corner_radius=10)
        self.status_bar.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.status_bar.grid_columnconfigure(1, weight=1)

        self.status_time = ctk.CTkLabel(self.status_bar, text="", font=ctk.CTkFont(size=12))
        self.status_time.grid(row=0, column=0, padx=20, pady=8)

        self.status_message = ctk.CTkLabel(self.status_bar, text="欢迎使用医院门诊挂号系统", font=ctk.CTkFont(size=12))
        self.status_message.grid(row=0, column=1, padx=20, pady=8, sticky="w")

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def update_status_bar(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.status_time.configure(text=current_time)
        self.after(1000, self.update_status_bar)

    def set_status_message(self, message):
        self.status_message.configure(text=message)

    def set_form_panel(self, form_panel):
        form_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def set_list_panel(self, list_panel):
        list_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

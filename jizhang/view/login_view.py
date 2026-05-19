import customtkinter as ctk
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, ACCENT_COLOR


class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        self.login_frame = ctk.CTkFrame(root, width=400, height=400, corner_radius=15)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.title_label = ctk.CTkLabel(self.login_frame, text="个人记账管理系统", 
                                        font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=30)

        self.username_label = ctk.CTkLabel(self.login_frame, text="用户名")
        self.username_label.pack(pady=(10, 5), anchor=ctk.W, padx=40)
        self.username_entry = ctk.CTkEntry(self.login_frame, width=320, height=40)
        self.username_entry.pack(pady=5)

        self.password_label = ctk.CTkLabel(self.login_frame, text="密码")
        self.password_label.pack(pady=(10, 5), anchor=ctk.W, padx=40)
        self.password_entry = ctk.CTkEntry(self.login_frame, width=320, height=40, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ctk.CTkButton(self.login_frame, text="登录", width=320, height=40,
                                          fg_color=ACCENT_COLOR, hover_color="#2980b9")
        self.login_button.pack(pady=20)

        self.register_button = ctk.CTkButton(self.login_frame, text="注册", width=320, height=40,
                                             fg_color="transparent", border_color=ACCENT_COLOR, 
                                             border_width=2, text_color=ACCENT_COLOR)
        self.register_button.pack(pady=5)

        self.error_label = ctk.CTkLabel(self.login_frame, text="", text_color="#e74c3c", font=ctk.CTkFont(size=12))
        self.error_label.pack(pady=10)

    def get_username(self):
        return self.username_entry.get().strip()

    def get_password(self):
        return self.password_entry.get().strip()

    def show_error(self, message):
        self.error_label.configure(text=message)

    def clear_fields(self):
        self.username_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)
        self.error_label.configure(text="")

    def set_login_command(self, command):
        self.login_button.configure(command=command)

    def set_register_command(self, command):
        self.register_button.configure(command=command)
import customtkinter as ctk
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, ACCENT_COLOR


class MainView:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

        self.main_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.main_frame.pack(fill=ctk.BOTH, expand=True)

        self.sidebar = ctk.CTkFrame(self.main_frame, width=180, corner_radius=0)
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)

        self.user_label = ctk.CTkLabel(self.sidebar, text=f"欢迎, {user['username']}", 
                                       font=ctk.CTkFont(size=14, weight="bold"))
        self.user_label.pack(pady=20)

        self.bill_button = ctk.CTkButton(self.sidebar, text="账单管理", width=140, height=40,
                                         fg_color=ACCENT_COLOR, hover_color="#2980b9")
        self.bill_button.pack(pady=10)

        self.category_button = ctk.CTkButton(self.sidebar, text="分类管理", width=140, height=40,
                                             fg_color="transparent", border_color=ACCENT_COLOR,
                                             border_width=2, text_color=ACCENT_COLOR)
        self.category_button.pack(pady=5)

        self.logout_button = ctk.CTkButton(self.sidebar, text="退出登录", width=140, height=40,
                                           fg_color="#e74c3c", hover_color="#c0392b")
        self.logout_button.pack(pady=(10, 20), side=ctk.BOTTOM)

        self.content_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        self.content_frame.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=True)

    def set_bill_command(self, command):
        self.bill_button.configure(command=command)

    def set_category_command(self, command):
        self.category_button.configure(command=command)

    def set_logout_command(self, command):
        self.logout_button.configure(command=command)

    def get_content_frame(self):
        return self.content_frame

    def highlight_bill_button(self):
        self.bill_button.configure(fg_color=ACCENT_COLOR, hover_color="#2980b9", 
                                   border_color="transparent", border_width=0,
                                   text_color="white")
        self.category_button.configure(fg_color="transparent", hover_color="gray", 
                                       border_color=ACCENT_COLOR, border_width=2,
                                       text_color=ACCENT_COLOR)

    def highlight_category_button(self):
        self.category_button.configure(fg_color=ACCENT_COLOR, hover_color="#2980b9", 
                                       border_color="transparent", border_width=0,
                                       text_color="white")
        self.bill_button.configure(fg_color="transparent", hover_color="gray", 
                                   border_color=ACCENT_COLOR, border_width=2,
                                   text_color=ACCENT_COLOR)
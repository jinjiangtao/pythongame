import customtkinter as ctk
from view.login_view import LoginView
from view.main_view import MainView
from view.category_view import CategoryView
from view.bill_view import BillView
from view.log_view import LogView
from controller.user_controller import UserController
from controller.category_controller import CategoryController
from controller.bill_controller import BillController
from controller.log_controller import LogController
from model.db import Database


class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.current_user = None
        self.login_view = None
        self.main_view = None
        self.category_view = None
        self.bill_view = None
        self.log_view = None
        self.category_controller = None
        self.bill_controller = None
        self.log_controller = None
        self.current_theme = "light"

        ctk.set_appearance_mode(self.current_theme)
        ctk.set_default_color_theme("blue")

        self.show_login()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def show_login(self):
        self.clear_frame()
        self.login_view = LoginView(self.root)
        self.user_controller = UserController(self.login_view)
        self.user_controller.set_login_success_callback(self.on_login_success)

    def on_login_success(self, user):
        self.current_user = user
        self.show_main()

    def show_main(self):
        self.clear_frame()
        self.main_view = MainView(self.root, self.current_user)
        self.main_view.set_bill_command(self.show_bill_view)
        self.main_view.set_category_command(self.show_category_view)
        self.main_view.set_log_command(self.show_log_view)
        self.main_view.set_theme_command(self.toggle_theme)
        self.main_view.set_logout_command(self.on_logout)
        self.show_bill_view()

    def show_bill_view(self):
        self.clear_content()
        self.main_view.highlight_bill_button()
        self.bill_view = BillView(self.main_view.get_content_frame())
        self.bill_controller = BillController(self.bill_view, self.current_user)

    def show_category_view(self):
        self.clear_content()
        self.main_view.highlight_category_button()
        self.category_view = CategoryView(self.main_view.get_content_frame())
        self.category_controller = CategoryController(self.category_view, self.current_user)

    def show_log_view(self):
        self.clear_content()
        self.main_view.highlight_log_button()
        self.log_view = LogView(self.main_view.get_content_frame())
        self.log_controller = LogController(self.log_view, self.current_user)

    def toggle_theme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
        ctk.set_appearance_mode(self.current_theme)

    def on_logout(self):
        self.current_user = None
        self.show_login()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def clear_content(self):
        for widget in self.main_view.get_content_frame().winfo_children():
            widget.destroy()

    def on_close(self):
        db = Database()
        db.close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
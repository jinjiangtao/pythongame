from model.user_model import UserModel
from model.operation_log_model import OperationLogModel


class UserController:
    def __init__(self, view):
        self.view = view
        self.user_model = UserModel()
        self.log_model = OperationLogModel()
        self.view.set_login_command(self.handle_login)
        self.view.set_register_command(self.handle_register)

    def handle_login(self):
        username = self.view.get_username()
        password = self.view.get_password()

        user, message = self.user_model.login(username, password)
        
        if user:
            self.log_model.add_log(user["id"], "LOGIN", description=f"用户 {username} 登录成功")
            self.view.show_error("")
            if self.on_login_success:
                self.on_login_success(user)
        else:
            self.view.show_error(message)

    def handle_register(self):
        username = self.view.get_username()
        password = self.view.get_password()

        success, message = self.user_model.register(username, password)
        
        if success:
            self.view.show_error("")
            self.view.clear_fields()
            self.view.show_error(message)
        else:
            self.view.show_error(message)

    def set_login_success_callback(self, callback):
        self.on_login_success = callback
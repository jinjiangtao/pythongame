from model.operation_log_model import OperationLogModel


class OperationLogController:
    def __init__(self, view, user):
        self.view = view
        self.user = user
        self.log_model = OperationLogModel()
        self.view.set_search_command(self.handle_search)
        self.view.set_refresh_command(self.handle_refresh)
        self.view.set_prev_page_command(self.handle_prev_page)
        self.view.set_next_page_command(self.handle_next_page)
        self.load_logs()

    def load_logs(self):
        params = self.view.get_filter_params()
        current_page = self.view.get_current_page()
        page_size = self.view.get_page_size()

        logs = self.log_model.get_logs(
            self.user["id"],
            operation_type=params["operation_type"],
            start_date=params["start_date"],
            end_date=params["end_date"],
            page=current_page,
            page_size=page_size
        )

        total_count = self.log_model.get_logs_count(
            self.user["id"],
            operation_type=params["operation_type"],
            start_date=params["start_date"],
            end_date=params["end_date"]
        )

        total_pages = (total_count + page_size - 1) // page_size
        if total_pages == 0:
            total_pages = 1

        self.view.update_pagination(current_page, total_pages, total_count)
        self.view.display_logs(logs)

    def handle_search(self):
        self.view.reset_page()
        self.load_logs()

    def handle_refresh(self):
        self.view.reset_page()
        self.view.start_date_entry.delete(0, 'end')
        self.view.end_date_entry.delete(0, 'end')
        self.view.type_var.set("全部")
        self.load_logs()

    def handle_prev_page(self):
        current_page = self.view.get_current_page()
        if current_page > 1:
            self.view.update_pagination(current_page - 1, self.view.total_pages, self.view.total_count)
            self.load_logs()

    def handle_next_page(self):
        current_page = self.view.get_current_page()
        if current_page < self.view.total_pages:
            self.view.update_pagination(current_page + 1, self.view.total_pages, self.view.total_count)
            self.load_logs()

    def add_log(self, operation_type, description=None, details=None):
        self.log_model.add_log(self.user["id"], operation_type, description, details)

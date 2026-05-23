from model.log_model import LogModel


class LogController:
    def __init__(self, view, user):
        self.view = view
        self.user = user
        self.log_model = LogModel()
        self.view.set_search_command(self.handle_search)
        self.view.set_prev_page_command(self.handle_prev_page)
        self.view.set_next_page_command(self.handle_next_page)
        self.load_logs()

    def load_logs(self):
        params = self.view.get_filter_params()
        current_page = self.view.get_current_page()
        page_size = self.view.get_page_size()

        logs = self.log_model.get_logs(
            operation_type=params["operation_type"],
            start_date=params["start_date"],
            end_date=params["end_date"],
            page=current_page,
            page_size=page_size
        )

        total_count = self.log_model.get_logs_count(
            operation_type=params["operation_type"],
            start_date=params["start_date"],
            end_date=params["end_date"]
        )

        total_pages = (total_count + page_size - 1) // page_size
        self.view.update_pagination(current_page, max(total_pages, 1), total_count)
        self.view.display_logs(logs)

    def handle_search(self):
        self.view.reset_page()
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
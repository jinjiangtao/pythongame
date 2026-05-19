from model.category_model import CategoryModel


class CategoryController:
    def __init__(self, view, user):
        self.view = view
        self.user = user
        self.category_model = CategoryModel()
        self.view.set_add_command(self.handle_add)
        self.view.set_type_change_command(self.load_categories)
        self.view.set_search_command(self.load_categories)
        self.view.set_edit_callback(self.handle_edit)
        self.view.set_delete_callback(self.handle_delete)
        self.load_categories()

    def load_categories(self):
        type_ = self.view.get_selected_type()
        keyword = self.view.get_search_keyword()
        categories = self.category_model.get_categories(self.user["id"], type_, keyword)
        self.view.display_categories(categories)

    def handle_add(self):
        self.view.show_add_dialog(self.save_category)

    def save_category(self, name, category_id=None):
        if category_id:
            success, message = self.category_model.update_category(category_id, self.user["id"], name)
        else:
            type_ = self.view.get_selected_type()
            success, message = self.category_model.add_category(self.user["id"], name, type_)
        
        if success:
            self.view.show_message(message)
            self.load_categories()
        else:
            self.view.show_message(message, is_error=True)

    def handle_edit(self, category_id):
        self.view.show_add_dialog(self.save_category, "", category_id)

    def handle_delete(self, category_id):
        success, message = self.category_model.delete_category(category_id, self.user["id"])
        
        if success:
            self.view.show_message(message)
            self.load_categories()
        else:
            self.view.show_message(message, is_error=True)
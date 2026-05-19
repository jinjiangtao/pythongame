from model.bill_model import BillModel
from model.category_model import CategoryModel


class BillController:
    def __init__(self, view, user):
        self.view = view
        self.user = user
        self.bill_model = BillModel()
        self.category_model = CategoryModel()
        self.view.set_add_command(self.handle_add)
        self.view.set_search_command(self.load_bills)
        self.view.set_edit_callback(self.handle_edit)
        self.view.set_delete_callback(self.handle_delete)
        self.load_bills()

    def load_bills(self):
        params = self.view.get_filter_params()
        bills = self.bill_model.get_bills(
            self.user["id"],
            type_=params["type"],
            start_date=params["start_date"],
            end_date=params["end_date"]
        )
        self.view.display_bills(bills)
        self.update_summary()

    def update_summary(self):
        params = self.view.get_filter_params()
        summary = self.bill_model.get_summary(
            self.user["id"],
            start_date=params["start_date"],
            end_date=params["end_date"]
        )
        self.view.update_summary(summary)

    def handle_add(self):
        categories = self.category_model.get_categories(self.user["id"])
        self.view.show_add_dialog(categories, self.save_bill)

    def save_bill(self, type_, category_id, amount_val, remark, payment_method, date, bill_id=None):
        try:
            amount = float(amount_val)
        except ValueError:
            self.view.show_message("金额必须是数字", is_error=True)
            return

        if bill_id:
            success, message = self.bill_model.update_bill(
                bill_id, self.user["id"], type_, category_id, amount, remark, payment_method, date
            )
        else:
            success, message = self.bill_model.add_bill(
                self.user["id"], type_, category_id, amount, remark, payment_method, date
            )
        
        if success:
            self.view.show_message(message)
            self.load_bills()
        else:
            self.view.show_message(message, is_error=True)

    def handle_edit(self, bill_id):
        bill = self.bill_model.get_bill_by_id(bill_id, self.user["id"])
        if bill:
            categories = self.category_model.get_categories(self.user["id"], bill[1])
            self.view.show_add_dialog(categories, self.save_bill, bill)

    def handle_delete(self, bill_id):
        success, message = self.bill_model.delete_bill(bill_id, self.user["id"])
        
        if success:
            self.view.show_message(message)
            self.load_bills()
        else:
            self.view.show_message(message, is_error=True)
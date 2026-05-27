import customtkinter as ctk
from views.main_window import MainWindow
from views.form_panel import FormPanel
from views.list_panel import ListPanel
from controllers.registration_controller import RegistrationController

def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    controller = RegistrationController()
    app = MainWindow(controller)

    form_panel = FormPanel(app.main_content, controller)
    list_panel = ListPanel(app.main_content, controller)

    controller.set_view(app)
    controller.set_form_panel(form_panel)
    controller.set_list_panel(list_panel)

    app.set_form_panel(form_panel)
    app.set_list_panel(list_panel)

    controller.load_registrations()

    app.mainloop()

if __name__ == "__main__":
    main()

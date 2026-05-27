import tkinter as tk
from database.db_init import init_database
from view.main_view import MainView
from controller.main_controller import MainController

def main():
    init_database()
    
    root = tk.Tk()
    view = MainView(root)
    controller = MainController(view)
    
    view.show_employee_panel()
    
    root.mainloop()

if __name__ == '__main__':
    main()
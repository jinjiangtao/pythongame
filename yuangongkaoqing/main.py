import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from database.db_init import init_database
from view.main_view import MainView
from controller.main_controller import MainController
import tkinter as tk

def main():
    init_database()
    
    root = tk.Tk()
    view = MainView(root)
    controller = MainController(view)
    
    root.mainloop()

if __name__ == '__main__':
    main()
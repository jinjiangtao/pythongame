# -*- coding: utf-8 -*-
import tkinter as tk
from controller.MainController import MainController

def main():
    root = tk.Tk()
    root.title("学生信息管理系统")
    controller = MainController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
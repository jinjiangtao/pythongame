# -*- coding: utf-8 -*-
"""
主程序入口
"""
import tkinter as tk
from controller import Controller


def main():
    root = tk.Tk()
    root.title("学生信息管理系统")
    controller = Controller(root)
    root.mainloop()


if __name__ == "__main__":
    main()

import customtkinter as ctk
from model import CalculatorModel
from view import CalculatorView
from controller import CalculatorController


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    model = CalculatorModel()
    view = CalculatorView()
    controller = CalculatorController(model, view)

    view.set_controller(controller)

    view.mainloop()


if __name__ == "__main__":
    main()
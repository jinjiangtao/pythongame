import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model.game_model import GameModel
from view.game_view import GameView
from controller.game_controller import GameController

def main():
    root = tk.Tk()
    root.resizable(False, False)
    
    model = GameModel()
    controller = GameController(model, None)
    view = GameView(root, controller)
    controller.view = view
    
    view.center_window()
    view.update_board(model.get_board())
    
    root.mainloop()

if __name__ == "__main__":
    main()
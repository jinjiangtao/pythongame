import customtkinter as ctk
from controllers.game_controller import GameController

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    app = ctk.CTk()
    app.title("儿童数字数数游戏")
    app.resizable(False, False)
    
    controller = GameController(app)
    
    app.mainloop()
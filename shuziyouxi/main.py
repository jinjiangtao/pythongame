import customtkinter as ctk
from controllers.game_controller import GameController
from config import Config, setup_customtkinter

if __name__ == "__main__":
    setup_customtkinter()
    
    app = ctk.CTk()
    app.title(Config.WINDOW_TITLE)
    app.resizable(False, False)
    
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    window_width = 800
    window_height = 650
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    app.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    controller = GameController(app)
    
    app.mainloop()
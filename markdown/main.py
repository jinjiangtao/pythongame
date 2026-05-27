import customtkinter as ctk
from app import MarkdownEditor

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    app = MarkdownEditor()
    app.mainloop()
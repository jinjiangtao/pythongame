import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Canvas Test")
app.geometry("800x600")

canvas = tk.Canvas(app, width=800, height=500, bg="white")
canvas.pack(pady=20)

canvas.create_rectangle(0, 400, 800, 500, fill="green", outline="")
canvas.create_text(400, 450, text="Ground", fill="black", font=("Arial", 12))

canvas.create_oval(375, 50, 425, 100, fill="red", outline="darkred", width=3)
canvas.create_text(400, 75, text="Ball", fill="white", font=("Arial", 10))

canvas.create_text(100, 50, text="Canvas Test - Working!", fill="blue", font=("Arial", 14))

print("Canvas test started successfully")
app.mainloop()
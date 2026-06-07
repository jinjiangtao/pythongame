import threading
import customtkinter as ctk
from app import ClipboardHistoryApp
from monitor import ClipboardMonitor
from tray import create_tray_icon
from database import init_database

def main():
    init_database()
    
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = ClipboardHistoryApp()
    monitor = ClipboardMonitor()
    monitor.start()
    
    def show_window():
        app.show()
    
    def exit_app():
        monitor.stop()
        icon.stop()
        app.destroy()
    
    icon = create_tray_icon(show_window, exit_app)
    
    def run_tray():
        icon.run()
    
    tray_thread = threading.Thread(target=run_tray, daemon=True)
    tray_thread.start()
    
    app.mainloop()

if __name__ == "__main__":
    main()
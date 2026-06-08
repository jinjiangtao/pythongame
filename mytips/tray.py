import pystray
from PIL import Image
from utils import create_icon
import threading


class SystemTray:
    def __init__(self, app):
        self.app = app
        self.icon = None
        self.thread = None
        
    def run(self):
        image = create_icon()
        menu = pystray.Menu(
            pystray.MenuItem("新建便签", self._create_note),
            pystray.MenuItem("显示全部", self._show_all),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("设置", self._show_settings),
            pystray.MenuItem("退出", self._quit)
        )
        self.icon = pystray.Icon("MyStickyNotes", image, "便签", menu)
        self.icon.run()
        
    def start(self):
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        
    def stop(self):
        if self.icon:
            self.icon.stop()
            
    def _create_note(self, icon, item):
        self.app.create_note()
        
    def _show_all(self, icon, item):
        self.app.show_all_notes()
        
    def _show_settings(self, icon, item):
        self.app.show_settings()
        
    def _quit(self, icon, item):
        self.app.quit_app()

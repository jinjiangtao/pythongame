import pystray
from PIL import Image, ImageDraw
import threading


class TrayIcon:
    def __init__(self, on_click=None, on_show_main=None, on_stop=None, on_pause=None, on_resume=None):
        self.icon = None
        self.thread = None
        
        self.on_click = on_click
        self.on_show_main = on_show_main
        self.on_stop = on_stop
        self.on_pause = on_pause
        self.on_resume = on_resume
        
        self.is_recording = False
        self.is_paused = False
    
    def create_icon(self, recording=False, paused=False):
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color=(30, 30, 30))
        draw = ImageDraw.Draw(image)
        
        center_x = width // 2
        center_y = height // 2
        
        if recording and not paused:
            draw.ellipse([center_x - 15, center_y - 15, center_x + 15, center_y + 15],
                        fill='red', outline='white', width=2)
        elif recording and paused:
            bar_width = 6
            gap = 4
            left_bar = center_x - bar_width - gap // 2
            right_bar = center_x + gap // 2
            draw.rectangle([left_bar, center_y - 10, left_bar + bar_width, center_y + 10],
                         fill='yellow', outline='white')
            draw.rectangle([right_bar, center_y - 10, right_bar + bar_width, center_y + 10],
                         fill='yellow', outline='white')
        else:
            draw.polygon([(center_x, center_y - 15),
                         (center_x + 12, center_y + 10),
                         (center_x - 12, center_y + 10)],
                        fill='green', outline='white')
        
        return image
    
    def update_icon(self):
        if self.icon:
            self.icon.icon = self.create_icon(self.is_recording, self.is_paused)
    
    def on_activate(self, icon, item):
        if self.on_click:
            self.on_click()
    
    def on_menu_show(self, icon, item):
        if self.on_show_main:
            self.on_show_main()
    
    def on_menu_stop(self, icon, item):
        if self.on_stop:
            self.on_stop()
    
    def on_menu_pause(self, icon, item):
        if self.on_pause:
            self.on_pause()
    
    def on_menu_resume(self, icon, item):
        if self.on_resume:
            self.on_resume()
    
    def run(self):
        menu = pystray.Menu(
            pystray.MenuItem('显示主界面', self.on_menu_show),
            pystray.MenuItem('暂停录制', self.on_menu_pause, enabled=lambda item: self.is_recording and not self.is_paused),
            pystray.MenuItem('继续录制', self.on_menu_resume, enabled=lambda item: self.is_recording and self.is_paused),
            pystray.MenuItem('停止录制', self.on_menu_stop, enabled=lambda item: self.is_recording),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('退出', self.stop)
        )
        
        self.icon = pystray.Icon(
            'Screen Recorder',
            self.create_icon(),
            '屏幕录制工具',
            menu
        )
        
        self.icon.run()
    
    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        if self.icon:
            self.icon.stop()
    
    def show(self):
        if self.icon:
            self.icon.visible = True
    
    def hide(self):
        if self.icon:
            self.icon.visible = False
    
    def notify(self, message):
        if self.icon:
            self.icon.notify(message)
    
    def set_recording(self, recording):
        self.is_recording = recording
        self.update_icon()
    
    def set_paused(self, paused):
        self.is_paused = paused
        self.update_icon()
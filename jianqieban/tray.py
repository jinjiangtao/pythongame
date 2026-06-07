import pystray
from PIL import Image, ImageDraw

def create_tray_icon(show_window_callback, exit_callback):
    def create_image():
        image = Image.new('RGB', (64, 64), color=(255, 255, 255))
        dc = ImageDraw.Draw(image)
        dc.rectangle([(16, 16), (48, 48)], fill=(66, 153, 225))
        dc.text((20, 20), 'CLIP', fill='white', font_size=12)
        return image
    
    menu = pystray.Menu(
        pystray.MenuItem('显示主窗口', show_window_callback),
        pystray.MenuItem('退出程序', exit_callback)
    )
    
    icon = pystray.Icon('clipboard', create_image(), '剪贴板历史管理器', menu)
    return icon
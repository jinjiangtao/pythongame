import platform
import os
import sys
import ctypes
from PIL import Image, ImageDraw, ImageFont


def create_icon():
    img = Image.new('RGBA', (64, 64), (255, 255, 0, 255))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([4, 4, 60, 60], radius=8, fill=(255, 255, 150, 255), outline=(200, 200, 0, 255), width=3)
    draw.line([(8, 20), (56, 20)], fill=(100, 100, 100, 255), width=2)
    draw.line([(8, 30), (50, 30)], fill=(100, 100, 100, 255), width=2)
    draw.line([(8, 40), (45, 40)], fill=(100, 100, 100, 255), width=2)
    return img


NOTE_COLORS = {
    'yellow': ('#FFFF88', '#FFFFAA', '#888800'),
    'blue': ('#88CCFF', '#AAEEFF', '#0066AA'),
    'green': ('#88FF88', '#AAFFAA', '#00AA00'),
    'pink': ('#FF88CC', '#FFAAEE', '#AA0066'),
    'purple': ('#CC88FF', '#EEAAFF', '#6600AA')
}


def set_startup(enable: bool):
    if platform.system() == 'Windows':
        import winreg
        key_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
        app_name = 'MyStickyNotes'
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            if enable:
                exe_path = os.path.abspath(sys.argv[0])
                if exe_path.endswith('.py'):
                    exe_path = f'"{sys.executable}" "{exe_path}"'
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
            else:
                try:
                    winreg.DeleteValue(key, app_name)
                except WindowsError:
                    pass
            winreg.CloseKey(key)
        except Exception as e:
            print(f"设置开机启动失败: {e}")


def play_reminder_sound():
    if platform.system() == 'Windows':
        ctypes.windll.user32.MessageBeep(0xFFFFFFFF)
    else:
        print('\a')


def parse_checkbox_content(content: str):
    lines = content.split('\n')
    result = []
    for line in lines:
        if line.startswith('□ '):
            result.append(('checkbox', False, line[2:]))
        elif line.startswith('☑ '):
            result.append(('checkbox', True, line[2:]))
        else:
            result.append(('text', line))
    return result

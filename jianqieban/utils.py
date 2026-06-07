import pyperclip
from datetime import datetime

def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_clipboard_content():
    try:
        return pyperclip.paste()
    except Exception:
        return ""

def set_clipboard_content(content):
    try:
        pyperclip.copy(content)
        return True
    except Exception:
        return False

def truncate_content(content, max_length=30):
    if len(content) > max_length:
        return content[:max_length] + "..."
    return content
import os
import time
from PIL import ImageTk, Image
import tkinter as tk
from settings import SUPPORTED_IMAGE_FORMATS


def get_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def is_image_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    return ext in SUPPORTED_IMAGE_FORMATS


def resize_image(image, max_size):
    img_width, img_height = image.size
    max_width, max_height = max_size
    
    ratio = min(max_width / img_width, max_height / img_height)
    new_size = (int(img_width * ratio), int(img_height * ratio))
    
    return image.resize(new_size, Image.Resampling.LANCZOS)


def image_to_tkinter(image):
    return ImageTk.PhotoImage(image)


def copy_to_clipboard(text):
    try:
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        root.destroy()
        return True
    except Exception as e:
        print(f"复制到剪贴板失败: {e}")
        return False


def export_to_txt(text, filepath):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"导出 TXT 失败: {e}")
        return False


def export_to_docx(text, filepath):
    try:
        from docx import Document
        doc = Document()
        doc.add_paragraph(text)
        doc.save(filepath)
        return True
    except Exception as e:
        print(f"导出 DOCX 失败: {e}")
        return False

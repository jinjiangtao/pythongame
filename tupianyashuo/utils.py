# ========== utils.py ==========
"""
辅助函数模块：提供格式化文件大小、弹窗提示等通用功能
"""
import os
from tkinter import messagebox


def format_file_size(size_bytes: int) -> str:
    """
    将字节数格式化为人类可读的文件大小

    Args:
        size_bytes: 文件大小（字节）

    Returns:
        格式化后的文件大小字符串，如 "1.2 MB"
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def show_info(title: str, message: str) -> None:
    """显示信息弹窗"""
    messagebox.showinfo(title, message)


def show_warning(title: str, message: str) -> None:
    """显示警告弹窗"""
    messagebox.showwarning(title, message)


def show_error(title: str, message: str) -> None:
    """显示错误弹窗"""
    messagebox.showerror(title, message)


def get_file_extension(file_path: str) -> str:
    """
    获取文件扩展名（小写）

    Args:
        file_path: 文件路径

    Returns:
        文件扩展名，如 ".jpg"
    """
    return os.path.splitext(file_path)[1].lower()


def is_supported_image(file_path: str) -> bool:
    """
    判断是否为支持的图片格式

    Args:
        file_path: 文件路径

    Returns:
        是否支持
    """
    supported_extensions = {'.jpg', '.jpeg', '.png'}
    return get_file_extension(file_path) in supported_extensions


def get_file_size(file_path: str) -> int:
    """
    获取文件大小（字节）

    Args:
        file_path: 文件路径

    Returns:
        文件大小（字节）
    """
    try:
        return os.path.getsize(file_path)
    except (OSError, FileNotFoundError):
        return 0

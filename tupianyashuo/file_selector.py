# ========== file_selector.py ==========
"""
文件选择模块：负责图片多选和输出文件夹选择功能
"""
import os
from typing import List, Tuple
from tkinter import filedialog
from utils import is_supported_image, get_file_size


class FileSelector:
    """文件选择器类"""

    def __init__(self):
        self.selected_files: List[Tuple[str, int]] = []  # (文件路径, 原始大小)
        self.output_dir: str = ""

    def select_images(self) -> List[Tuple[str, int]]:
        """
        打开文件选择对话框，选择多张图片

        Returns:
            选中的图片列表，每个元素为(文件路径, 原始大小)
        """
        file_paths = filedialog.askopenfilenames(
            title="选择图片文件",
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png"),
                ("JPG 文件", "*.jpg *.jpeg"),
                ("PNG 文件", "*.png"),
                ("所有文件", "*.*")
            ]
        )

        # 过滤支持的图片格式，并获取文件大小
        valid_files = []
        for path in file_paths:
            if is_supported_image(path):
                size = get_file_size(path)
                valid_files.append((path, size))

        self.selected_files.extend(valid_files)
        return valid_files

    def select_output_dir(self) -> str:
        """
        选择输出文件夹

        Returns:
            选中的文件夹路径
        """
        dir_path = filedialog.askdirectory(title="选择输出文件夹")
        if dir_path:
            self.output_dir = dir_path
        return self.output_dir

    def clear_files(self) -> None:
        """清空已选择的文件列表"""
        self.selected_files = []

    def remove_file(self, index: int) -> None:
        """
        移除指定索引的文件

        Args:
            index: 文件索引
        """
        if 0 <= index < len(self.selected_files):
            self.selected_files.pop(index)

    def get_file_count(self) -> int:
        """获取已选择文件的数量"""
        return len(self.selected_files)

    def get_total_size(self) -> int:
        """获取所有已选择文件的总大小"""
        return sum(size for _, size in self.selected_files)

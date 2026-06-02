# ========== file_selector.py ==========
"""
文件选择模块：负责图片多选和输出文件夹选择功能
V1.1 新增：批量移除、文件夹扫描、拖拽支持、路径去重
"""
import os
from typing import List, Tuple, Set
from tkinter import filedialog
from utils import is_supported_image, get_file_size


class FileSelector:
    """文件选择器类"""

    def __init__(self):
        self.selected_files: List[Tuple[str, int]] = []  # (文件路径, 原始大小)
        self._file_paths: Set[str] = set()  # 用于去重的路径集合
        self.output_dir: str = ""

    def select_images(self) -> List[Tuple[str, int]]:
        """
        打开文件选择对话框，选择多张图片

        Returns:
            新选择的图片列表 [(文件路径, 原始大小), ...]
        """
        file_paths = filedialog.askopenfilenames(
            title="选择图片",
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png"),
                ("JPEG 图片", "*.jpg *.jpeg"),
                ("PNG 图片", "*.png"),
                ("所有文件", "*.*")
            ]
        )

        if file_paths:
            return self.add_files(list(file_paths))
        return []

    def add_files(self, file_paths: List[str]) -> List[Tuple[str, int]]:
        """
        批量添加文件到选择列表（自动去重）

        Args:
            file_paths: 文件路径列表

        Returns:
            实际添加的图片列表 [(文件路径, 原始大小), ...]
        """
        added_files = []
        for path in file_paths:
            # 跳过已存在的文件
            if path in self._file_paths:
                continue
            # 检查是否为支持的图片格式
            if is_supported_image(path):
                size = get_file_size(path)
                self.selected_files.append((path, size))
                self._file_paths.add(path)
                added_files.append((path, size))
        return added_files

    def add_folder(self, folder_path: str) -> List[Tuple[str, int]]:
        """
        扫描文件夹并添加所有支持的图片

        Args:
            folder_path: 文件夹路径

        Returns:
            实际添加的图片列表 [(文件路径, 原始大小), ...]
        """
        added_files = []
        try:
            for root, _, files in os.walk(folder_path):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    # 跳过已存在的文件
                    if file_path in self._file_paths:
                        continue
                    # 检查是否为支持的图片格式
                    if is_supported_image(file_path):
                        size = get_file_size(file_path)
                        self.selected_files.append((file_path, size))
                        self._file_paths.add(file_path)
                        added_files.append((file_path, size))
        except Exception as e:
            print(f"扫描文件夹失败: {e}")
        return added_files

    def process_dropped_paths(self, paths: List[str]) -> List[Tuple[str, int]]:
        """
        处理拖拽进来的路径（可以是文件或文件夹）

        Args:
            paths: 拖拽进来的路径列表

        Returns:
            实际添加的图片列表 [(文件路径, 原始大小), ...]
        """
        added_files = []
        for path in paths:
            if os.path.isfile(path):
                # 是文件，直接尝试添加
                result = self.add_files([path])
                added_files.extend(result)
            elif os.path.isdir(path):
                # 是文件夹，扫描并添加
                result = self.add_folder(path)
                added_files.extend(result)
        return added_files

    def remove_selected(self, indices: List[int]) -> int:
        """
        移除指定索引的文件

        Args:
            indices: 要移除的文件索引列表

        Returns:
            实际移除的文件数量
        """
        if not indices:
            return 0

        # 按索引降序排序，从后往前删除避免索引错乱
        sorted_indices = sorted(indices, reverse=True)
        removed_count = 0

        for idx in sorted_indices:
            if 0 <= idx < len(self.selected_files):
                file_path, _ = self.selected_files.pop(idx)
                self._file_paths.discard(file_path)
                removed_count += 1

        return removed_count

    def clear_all(self) -> int:
        """
        清空所有已选文件

        Returns:
            清空的文件数量
        """
        count = len(self.selected_files)
        self.selected_files.clear()
        self._file_paths.clear()
        return count

    def get_file_count(self) -> int:
        """获取已选文件数量"""
        return len(self.selected_files)

    def get_total_size(self) -> int:
        """获取已选文件总大小（字节）"""
        return sum(size for _, size in self.selected_files)
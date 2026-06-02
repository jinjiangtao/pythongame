# ========== app.py ==========
"""
主窗口模块：负责界面布局和事件绑定
V1.1 新增功能：
- 清除列表按钮
- 移除选中功能（带复选框的列表）
- 拖拽添加支持（文件和文件夹）
- 拖拽视觉反馈
- 窗口可缩放和组件自适应
"""
import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from task_manager import TaskManager
from utils import format_file_size, show_info, show_warning, show_error

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    HAS_DND = True
except ImportError:
    HAS_DND = False

from typing import List, Tuple


class ImageCompressorApp(ctk.CTk):
    """图片批量压缩工具主窗口 - V1.1 版本"""

    def __init__(self):
        if HAS_DND:
            # 使用 TkinterDnD 支持拖拽
            super().__init__()
        else:
            super().__init__()

        # 初始化任务管理器
        self.task_manager = TaskManager()

        # 复选框状态字典 {索引: BooleanVar}
        self.checkbox_vars: dict = {}

        # 拖拽状态标志
        self._drag_over = False

        # 配置窗口
        self.title("图片批量压缩工具 V1.1")
        self.geometry("700x600")
        self.minsize(600, 500)

        # 设置深色主题
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # 创建界面
        self._create_widgets()

        # 设置拖拽支持
        if HAS_DND:
            self._setup_drag_drop()

        # 绑定窗口关闭事件
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_widgets(self):
        """创建界面组件"""
        # 配置网格权重，使窗口可缩放
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ========== 顶部区域：选择图片按钮和操作按钮 ==========
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, pady=10, padx=20, sticky="ew")
        top_frame.grid_columnconfigure(1, weight=1)

        # 左侧按钮组
        btn_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        btn_frame.grid(row=0, column=0, padx=5, sticky="w")

        self.select_btn = ctk.CTkButton(
            btn_frame,
            text="选择图片",
            command=self._on_select_images,
            width=100
        )
        self.select_btn.pack(side="left", padx=3)

        # V1.1 新增：清除列表按钮
        self.clear_btn = ctk.CTkButton(
            btn_frame,
            text="清除列表",
            command=self._on_clear_list,
            width=100,
            fg_color="#c0392b",
            hover_color="#962d22"
        )
        self.clear_btn.pack(side="left", padx=3)

        # V1.1 新增：移除选中按钮
        self.remove_btn = ctk.CTkButton(
            btn_frame,
            text="移除选中",
            command=self._on_remove_selected,
            width=100,
            fg_color="#e67e22",
            hover_color="#d35400"
        )
        self.remove_btn.pack(side="left", padx=3)

        # 文件数量标签
        self.file_count_label = ctk.CTkLabel(
            top_frame,
            text="已选 0 张图片 (共 0 B)"
        )
        self.file_count_label.grid(row=0, column=1, padx=20, sticky="e")

        # ========== 中间区域：文件列表（支持滚动和缩放） ==========
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=1, column=0, pady=5, padx=20, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

        # V1.1 新增：使用带复选框的可滚动列表
        # 创建 Canvas 和滚动条实现可滚动的复选框列表
        self.list_canvas = ctk.CTkCanvas(
            list_frame,
            bg="#1a1a2e",
            highlightthickness=2,
            highlightbackground="#2d2d44"
        )
        self.list_canvas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # 滚动条
        self.list_scrollbar = ctk.CTkScrollbar(
            list_frame,
            command=self.list_canvas.yview,
            orientation="vertical"
        )
        self.list_scrollbar.grid(row=0, column=1, sticky="ns", pady=5)

        self.list_canvas.configure(yscrollcommand=self.list_scrollbar.set)

        # 内部框架用于放置复选框
        self.list_inner_frame = ctk.CTkFrame(self.list_canvas, fg_color="transparent")
        self.list_canvas_window = self.list_canvas.create_window(
            (0, 0),
            window=self.list_inner_frame,
            anchor="nw"
        )

        # 绑定 Canvas 大小变化事件
        self.list_canvas.bind("<Configure>", self._on_canvas_configure)
        self.list_inner_frame.bind("<Configure>", self._on_frame_configure)

        # 绑定鼠标滚轮事件
        self.list_canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.list_inner_frame.bind("<MouseWheel>", self._on_mousewheel)

        # V1.1 新增：拖拽提示标签（初始隐藏）
        self.drag_hint_label = ctk.CTkLabel(
            list_frame,
            text="拖拽图片或文件夹到此处添加",
            font=("", 14),
            text_color="gray"
        )

        # ========== 压缩质量区域 ==========
        quality_frame = ctk.CTkFrame(self)
        quality_frame.grid(row=2, column=0, pady=10, padx=20, sticky="ew")
        quality_frame.grid_columnconfigure(1, weight=1)

        quality_label = ctk.CTkLabel(quality_frame, text="压缩质量:")
        quality_label.grid(row=0, column=0, padx=5, sticky="w")

        self.quality_var = ctk.IntVar(value=80)
        self.quality_slider = ctk.CTkSlider(
            quality_frame,
            from_=50,
            to=100,
            variable=self.quality_var,
            command=self._on_quality_change
        )
        self.quality_slider.grid(row=0, column=1, padx=10, sticky="ew")

        self.quality_value_label = ctk.CTkLabel(quality_frame, text="80", width=40)
        self.quality_value_label.grid(row=0, column=2, padx=5, sticky="e")

        # ========== 输出文件夹区域 ==========
        output_frame = ctk.CTkFrame(self)
        output_frame.grid(row=3, column=0, pady=5, padx=20, sticky="ew")
        output_frame.grid_columnconfigure(1, weight=1)

        self.output_btn = ctk.CTkButton(
            output_frame,
            text="选择输出文件夹",
            command=self._on_select_output,
            width=130
        )
        self.output_btn.grid(row=0, column=0, padx=5, sticky="w")

        self.output_dir_label = ctk.CTkLabel(
            output_frame,
            text="未选择输出文件夹",
            anchor="w"
        )
        self.output_dir_label.grid(row=0, column=1, padx=10, sticky="ew")

        # ========== 底部区域：压缩按钮和进度条 ==========
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.grid(row=4, column=0, pady=15, padx=20, sticky="ew")
        bottom_frame.grid_columnconfigure(1, weight=1)

        self.compress_btn = ctk.CTkButton(
            bottom_frame,
            text="开始压缩",
            command=self._on_start_compression,
            width=120
        )
        self.compress_btn.grid(row=0, column=0, padx=5, sticky="w")

        self.progress_bar = ctk.CTkProgressBar(bottom_frame)
        self.progress_bar.grid(row=0, column=1, padx=10, sticky="ew")
        self.progress_bar.set(0)

        # 显示拖拽提示（如果没有文件）
        self._update_drag_hint()

    def _on_canvas_configure(self, event):
        """Canvas 大小变化时调整内部框架宽度"""
        self.list_canvas.itemconfig(self.list_canvas_window, width=event.width)

    def _on_frame_configure(self, event):
        """内部框架大小变化时更新滚动区域"""
        self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))

    def _on_mousewheel(self, event):
        """鼠标滚轮滚动事件"""
        self.list_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _update_drag_hint(self):
        """更新拖拽提示显示状态"""
        if not self.task_manager.file_selector.selected_files:
            self.drag_hint_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.drag_hint_label.place_forget()

    def _setup_drag_drop(self):
        """V1.1 新增：设置拖拽支持"""
        if not HAS_DND:
            return

        # 注册拖拽目标
        self.list_canvas.drop_target_register(DND_FILES)
        self.list_canvas.dnd_bind('<<Drop>>', self._on_drop)
        self.list_canvas.dnd_bind('<<DragEnter>>', self._on_drag_enter)
        self.list_canvas.dnd_bind('<<DragLeave>>', self._on_drag_leave)
        self.list_canvas.dnd_bind('<<DragOver>>', self._on_drag_over)

    def _on_drag_enter(self, event):
        """V1.1 新增：拖拽进入事件 - 视觉反馈"""
        self._drag_over = True
        self.list_canvas.configure(highlightbackground="#3498db", highlightthickness=3)
        self.list_canvas.configure(bg="#1a2a3e")

    def _on_drag_leave(self, event):
        """V1.1 新增：拖拽离开事件 - 恢复样式"""
        self._drag_over = False
        self.list_canvas.configure(highlightbackground="#2d2d44", highlightthickness=2)
        self.list_canvas.configure(bg="#1a1a2e")

    def _on_drag_over(self, event):
        """V1.1 新增：拖拽悬停事件"""
        pass

    def _on_drop(self, event):
        """V1.1 新增：拖拽放下事件 - 处理拖拽的文件"""
        self._drag_over = False
        self.list_canvas.configure(highlightbackground="#2d2d44", highlightthickness=2)
        self.list_canvas.configure(bg="#1a1a2e")

        # 解析拖拽的路径
        dropped_data = event.data
        paths = self._parse_dropped_files(dropped_data)

        if paths:
            added = self.task_manager.file_selector.process_dropped_paths(paths)
            if added:
                self._update_file_list()
                self._update_file_count()
                show_info("添加成功", f"成功添加 {len(added)} 张图片")

    def _parse_dropped_files(self, dropped_data: str) -> List[str]:
        """
        V1.1 新增：解析拖拽的文件数据

        Args:
            dropped_data: 拖拽事件的数据字符串

        Returns:
            文件路径列表
        """
        paths = []
        # Windows 下拖拽数据格式可能是 {path1} {path2} 或 path1 path2
        # 处理带花括号的路径（包含空格的路径）
        i = 0
        data = dropped_data
        while i < len(data):
            if data[i] == '{':
                # 找到匹配的右花括号
                end = data.find('}', i)
                if end != -1:
                    path = data[i+1:end]
                    paths.append(path)
                    i = end + 1
                else:
                    break
            elif data[i] == ' ':
                i += 1
            else:
                # 找到下一个空格或结尾
                end = data.find(' ', i)
                if end == -1:
                    end = len(data)
                path = data[i:end]
                if path:
                    paths.append(path)
                i = end + 1

        return paths

    def _on_select_images(self):
        """选择图片按钮点击事件"""
        files = self.task_manager.file_selector.select_images()
        if files:
            self._update_file_list()
            self._update_file_count()

    def _on_clear_list(self):
        """V1.1 新增：清除列表按钮点击事件"""
        if not self.task_manager.file_selector.selected_files:
            show_warning("提示", "列表已经是空的！")
            return

        count = self.task_manager.file_selector.clear_all()
        self._update_file_list()
        self._update_file_count()
        show_info("清除完成", f"已清除 {count} 张图片")

    def _on_remove_selected(self):
        """V1.1 新增：移除选中按钮点击事件"""
        # 获取所有选中的索引
        selected_indices = []
        for idx, var in self.checkbox_vars.items():
            if var.get():
                selected_indices.append(idx)

        if not selected_indices:
            show_warning("提示", "请先勾选要移除的图片！")
            return

        # 移除选中的文件
        removed_count = self.task_manager.file_selector.remove_selected(selected_indices)
        self._update_file_list()
        self._update_file_count()
        show_info("移除完成", f"已移除 {removed_count} 张图片")

    def _on_select_output(self):
        """选择输出文件夹按钮点击事件"""
        output_dir = self.task_manager.file_selector.select_output_dir()
        if output_dir:
            self.output_dir_label.configure(text=output_dir)

    def _on_quality_change(self, value):
        """压缩质量滑动条变化事件"""
        self.quality_value_label.configure(text=str(int(value)))

    def _on_start_compression(self):
        """开始压缩按钮点击事件"""
        if not self.task_manager.file_selector.selected_files:
            show_warning("提示", "请先选择要压缩的图片！")
            return

        if not self.task_manager.file_selector.output_dir:
            show_warning("提示", "请先选择输出文件夹！")
            return

        self.compress_btn.configure(state="disabled")
        self.select_btn.configure(state="disabled")
        self.output_btn.configure(state="disabled")
        self.clear_btn.configure(state="disabled")
        self.remove_btn.configure(state="disabled")

        self.progress_bar.set(0)
        quality = self.quality_var.get()

        self.task_manager.start_compression(
            quality=quality,
            progress_callback=self._on_progress_update,
            complete_callback=self._on_compression_complete
        )

    def _on_progress_update(self, current, total):
        """进度更新回调"""
        progress = current / total
        self.progress_bar.after(0, self._update_progress, progress)

    def _update_progress(self, progress):
        """在主线程中更新进度条"""
        self.progress_bar.set(progress)

    def _on_compression_complete(self, success_count, fail_count, errors):
        """压缩完成回调"""
        self.after(0, self._handle_completion, success_count, fail_count, errors)

    def _handle_completion(self, success_count, fail_count, errors):
        """在主线程中处理压缩完成"""
        self.compress_btn.configure(state="normal")
        self.select_btn.configure(state="normal")
        self.output_btn.configure(state="normal")
        self.clear_btn.configure(state="normal")
        self.remove_btn.configure(state="normal")

        result_msg = f"完成 {success_count} 张，失败 {fail_count} 张"
        show_info("压缩完成", result_msg)
        self.progress_bar.set(0)

    def _update_file_list(self):
        """V1.1 修改：更新文件列表显示（带复选框）"""
        # 清除旧的复选框
        for widget in self.list_inner_frame.winfo_children():
            widget.destroy()

        self.checkbox_vars.clear()

        # 创建新的复选框列表
        files = self.task_manager.file_selector.selected_files
        for idx, (file_path, size) in enumerate(files):
            size_str = format_file_size(size)
            display_text = f"{file_path}  ({size_str})"

            var = tk.BooleanVar(value=False)
            self.checkbox_vars[idx] = var

            cb = ctk.CTkCheckBox(
                self.list_inner_frame,
                text=display_text,
                variable=var,
                command=self._on_checkbox_change,
                font=("", 11),
                anchor="w"
            )
            cb.pack(fill="x", padx=5, pady=2)

        # 更新滚动区域
        self.list_inner_frame.update_idletasks()
        self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))

        # 更新拖拽提示
        self._update_drag_hint()

    def _on_checkbox_change(self):
        """V1.1 新增：复选框状态变化事件"""
        pass

    def _update_file_count(self):
        """更新文件数量显示"""
        count = self.task_manager.file_selector.get_file_count()
        total_size = self.task_manager.file_selector.get_total_size()
        size_str = format_file_size(total_size)
        self.file_count_label.configure(text=f"已选 {count} 张图片 (共 {size_str})")

    def _on_closing(self):
        """窗口关闭事件"""
        self.destroy()


def create_app():
    """创建应用实例"""
    return ImageCompressorApp()
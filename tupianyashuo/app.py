# ========== app.py ==========
"""
主窗口模块：负责界面布局和事件绑定
"""
import customtkinter as ctk
from tkinter.scrolledtext import ScrolledText
from task_manager import TaskManager
from utils import format_file_size, show_info, show_warning, show_error


class ImageCompressorApp(ctk.CTk):
    """图片批量压缩工具主窗口"""

    def __init__(self):
        super().__init__()

        # 初始化任务管理器
        self.task_manager = TaskManager()

        # 配置窗口
        self.title("图片批量压缩工具")
        self.geometry("600x500")
        self.minsize(600, 500)

        # 设置深色主题
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # 创建界面
        self._create_widgets()

    def _create_widgets(self):
        """创建界面组件"""
        # 顶部区域：选择图片按钮
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(pady=10, padx=20, fill="x")

        self.select_btn = ctk.CTkButton(
            top_frame,
            text="选择图片",
            command=self._on_select_images
        )
        self.select_btn.pack(side="left", padx=5)

        self.file_count_label = ctk.CTkLabel(
            top_frame,
            text="已选 0 张图片"
        )
        self.file_count_label.pack(side="left", padx=20)

        # 中间区域：文件列表
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(pady=5, padx=20, fill="both", expand=True)

        # 使用 ScrolledText 显示文件列表
        self.file_list_text = ScrolledText(
            list_frame,
            wrap="none",
            bg="#1a1a1a",
            fg="white",
            insertbackground="white"
        )
        self.file_list_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.file_list_text.config(state="disabled")  # 只读

        # 压缩质量区域
        quality_frame = ctk.CTkFrame(self)
        quality_frame.pack(pady=10, padx=20, fill="x")

        quality_label = ctk.CTkLabel(quality_frame, text="压缩质量:")
        quality_label.pack(side="left", padx=5)

        self.quality_var = ctk.IntVar(value=80)
        self.quality_slider = ctk.CTkSlider(
            quality_frame,
            from_=50,
            to=100,
            variable=self.quality_var,
            command=self._on_quality_change
        )
        self.quality_slider.pack(side="left", padx=10, fill="x", expand=True)

        self.quality_value_label = ctk.CTkLabel(quality_frame, text="80")
        self.quality_value_label.pack(side="left", padx=5)

        # 输出文件夹区域
        output_frame = ctk.CTkFrame(self)
        output_frame.pack(pady=5, padx=20, fill="x")

        self.output_btn = ctk.CTkButton(
            output_frame,
            text="选择输出文件夹",
            command=self._on_select_output
        )
        self.output_btn.pack(side="left", padx=5)

        self.output_dir_label = ctk.CTkLabel(
            output_frame,
            text="未选择输出文件夹",
            anchor="w"
        )
        self.output_dir_label.pack(side="left", padx=10, fill="x", expand=True)

        # 底部区域：压缩按钮和进度条
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(pady=15, padx=20, fill="x")

        self.compress_btn = ctk.CTkButton(
            bottom_frame,
            text="开始压缩",
            command=self._on_start_compression
        )
        self.compress_btn.pack(side="left", padx=5)

        self.progress_bar = ctk.CTkProgressBar(bottom_frame)
        self.progress_bar.pack(side="left", padx=10, fill="x", expand=True)
        self.progress_bar.set(0)

    def _on_select_images(self):
        """选择图片按钮点击事件"""
        files = self.task_manager.file_selector.select_images()
        if files:
            self._update_file_list()
            self._update_file_count()

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
        # 检查是否选择了图片
        if not self.task_manager.file_selector.selected_files:
            show_warning("提示", "请先选择要压缩的图片！")
            return

        # 检查是否选择了输出文件夹
        if not self.task_manager.file_selector.output_dir:
            show_warning("提示", "请先选择输出文件夹！")
            return

        # 禁用按钮
        self.compress_btn.configure(state="disabled")
        self.select_btn.configure(state="disabled")
        self.output_btn.configure(state="disabled")

        # 获取压缩质量
        quality = self.quality_var.get()

        # 开始压缩
        self.task_manager.start_compression(
            quality=quality,
            progress_callback=self._on_progress_update,
            complete_callback=self._on_compression_complete
        )

    def _on_progress_update(self, current, total):
        """进度更新回调"""
        progress = current / total
        self.progress_bar.set(progress)
        self.update_idletasks()

    def _on_compression_complete(self, success_count, fail_count, errors):
        """压缩完成回调"""
        # 恢复按钮状态
        self.compress_btn.configure(state="normal")
        self.select_btn.configure(state="normal")
        self.output_btn.configure(state="normal")

        # 显示结果
        result_msg = f"完成 {success_count} 张，失败 {fail_count} 张"
        show_info("压缩完成", result_msg)

        # 重置进度条
        self.progress_bar.set(0)

    def _update_file_list(self):
        """更新文件列表显示"""
        self.file_list_text.config(state="normal")
        self.file_list_text.delete("1.0", "end")

        for file_path, size in self.task_manager.file_selector.selected_files:
            size_str = format_file_size(size)
            self.file_list_text.insert("end", f"{file_path} ({size_str})\n")

        self.file_list_text.config(state="disabled")

    def _update_file_count(self):
        """更新文件数量显示"""
        count = self.task_manager.file_selector.get_file_count()
        total_size = self.task_manager.file_selector.get_total_size()
        size_str = format_file_size(total_size)
        self.file_count_label.configure(text=f"已选 {count} 张图片 (共 {size_str})")

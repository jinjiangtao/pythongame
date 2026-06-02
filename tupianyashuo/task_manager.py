# ========== task_manager.py ==========
"""
任务管理模块：负责压缩任务列表维护、进度更新和异常处理
"""
import threading
from typing import List, Tuple, Callable, Optional
from file_selector import FileSelector
from compressor import Compressor
from utils import format_file_size


class TaskManager:
    """任务管理器类"""

    def __init__(self):
        self.file_selector = FileSelector()
        self.compressor = Compressor()
        self.is_running = False
        self.success_count = 0
        self.fail_count = 0
        self.errors: List[Tuple[str, str]] = []  # (文件路径, 错误信息)

    def start_compression(
        self,
        quality: int,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        complete_callback: Optional[Callable[[int, int, List[Tuple[str, str]]], None]] = None
    ) -> None:
        """
        开始压缩任务（在新线程中运行）

        Args:
            quality: 压缩质量
            progress_callback: 进度回调函数 (当前, 总数)
            complete_callback: 完成回调函数 (成功数, 失败数, 错误列表)
        """
        if self.is_running:
            return

        if not self.file_selector.selected_files:
            return

        if not self.file_selector.output_dir:
            return

        self.is_running = True
        self.success_count = 0
        self.fail_count = 0
        self.errors = []

        # 在新线程中执行压缩任务
        thread = threading.Thread(
            target=self._compress_task,
            args=(quality, progress_callback, complete_callback)
        )
        thread.daemon = True
        thread.start()

    def _compress_task(
        self,
        quality: int,
        progress_callback: Optional[Callable[[int, int], None]],
        complete_callback: Optional[Callable[[int, int, List[Tuple[str, str]]], None]]
    ) -> None:
        """
        压缩任务执行函数

        Args:
            quality: 压缩质量
            progress_callback: 进度回调
            complete_callback: 完成回调
        """
        try:
            total_files = len(self.file_selector.selected_files)

            for index, (file_path, _) in enumerate(self.file_selector.selected_files):
                # 压缩图片
                success, error_msg, _ = self.compressor.compress_image(
                    file_path,
                    self.file_selector.output_dir,
                    quality
                )

                if success:
                    self.success_count += 1
                else:
                    self.fail_count += 1
                    if error_msg:
                        self.errors.append((file_path, error_msg))

                # 更新进度
                if progress_callback:
                    progress_callback(index + 1, total_files)

        finally:
            self.is_running = False

            # 调用完成回调
            if complete_callback:
                complete_callback(self.success_count, self.fail_count, self.errors)

    def stop_compression(self) -> None:
        """停止压缩任务（目前只设置标志位，下次循环会停止）"""
        self.is_running = False

    def get_result_summary(self) -> str:
        """获取压缩结果摘要"""
        return f"完成 {self.success_count} 张，失败 {self.fail_count} 张"

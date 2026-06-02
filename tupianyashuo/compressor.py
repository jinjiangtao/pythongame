# ========== compressor.py ==========
"""
压缩逻辑模块：处理图片压缩算法，支持 JPG 和 PNG 格式
"""
import os
from typing import Optional, Tuple
from PIL import Image
from utils import get_file_extension


class Compressor:
    """图片压缩器类"""

    def __init__(self):
        pass

    def compress_image(
        self,
        input_path: str,
        output_dir: str,
        quality: int = 80
    ) -> Tuple[bool, Optional[str], Optional[int]]:
        """
        压缩单张图片

        Args:
            input_path: 输入图片路径
            output_dir: 输出文件夹路径
            quality: 压缩质量 (50-100)

        Returns:
            (是否成功, 错误信息, 压缩后文件大小)
        """
        try:
            # 检查输入文件是否存在
            if not os.path.exists(input_path):
                return False, f"文件不存在: {input_path}", None

            # 打开图片
            with Image.open(input_path) as img:
                # 获取文件扩展名
                ext = get_file_extension(input_path)

                # 构建输出路径
                filename = os.path.basename(input_path)
                output_path = os.path.join(output_dir, filename)

                # 根据格式选择压缩方式
                if ext in ['.jpg', '.jpeg']:
                    self._compress_jpg(img, output_path, quality)
                elif ext == '.png':
                    self._compress_png(img, output_path, quality)
                else:
                    return False, f"不支持的格式: {ext}", None

                # 获取压缩后文件大小
                compressed_size = os.path.getsize(output_path)
                return True, None, compressed_size

        except Exception as e:
            return False, f"压缩失败: {str(e)}", None

    def _compress_jpg(self, img: Image.Image, output_path: str, quality: int) -> None:
        """
        压缩 JPG 格式图片

        Args:
            img: PIL 图片对象
            output_path: 输出路径
            quality: 压缩质量
        """
        # 如果是 RGBA 模式，转换为 RGB
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        img.save(
            output_path,
            'JPEG',
            quality=quality,
            optimize=True
        )

    def _compress_png(self, img: Image.Image, output_path: str, quality: int) -> None:
        """
        压缩 PNG 格式图片

        Args:
            img: PIL 图片对象
            output_path: 输出路径
            quality: 压缩质量 (50-100，转换为 compress_level 1-9)
        """
        # 将 quality (50-100) 映射到 compress_level (1-9)
        # quality 50 -> compress_level 9 (最大压缩)
        # quality 100 -> compress_level 1 (最小压缩)
        compress_level = max(1, min(9, int((100 - quality) / 50 * 8) + 1))
        
        img.save(
            output_path,
            'PNG',
            optimize=True,
            compress_level=compress_level
        )

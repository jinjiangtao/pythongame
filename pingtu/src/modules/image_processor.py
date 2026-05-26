import pygame
import os
from config import DEFAULT_IMAGE_PATH

class ImageProcessor:
    def __init__(self):
        self.default_image = None
        self._create_default_image()

    def _create_default_image(self):
        width, height = 400, 400
        surface = pygame.Surface((width, height))
        surface.fill((135, 206, 235))
        
        for i in range(3):
            for j in range(3):
                color = ((i * 50 + 50) % 255, (j * 50 + 100) % 255, 150)
                rect = pygame.Rect(j * (width // 3), i * (height // 3), 
                                  width // 3, height // 3)
                pygame.draw.rect(surface, color, rect)
        
        pygame.draw.circle(surface, (255, 255, 255), (width // 2, height // 2), 60)
        pygame.draw.circle(surface, (255, 165, 0), (width // 2, height // 2), 40)
        
        self.default_image = surface

    def load_image(self, file_path=None):
        """
        加载图片文件，如果路径为空则使用默认图片
        :param file_path: 图片文件路径
        :return: pygame.Surface对象，加载成功返回图片，失败返回默认图片
        """
        if file_path is None or not os.path.exists(file_path):
            return self.default_image.copy()
        
        try:
            image = pygame.image.load(file_path)
            return image.convert()
        except pygame.error:
            return self.default_image.copy()

    def resize_image(self, image, target_width, target_height):
        """
        缩放图片以适配目标尺寸，保持宽高比
        :param image: 原始图片
        :param target_width: 目标宽度
        :param target_height: 目标高度
        :return: 缩放后的图片
        """
        original_width, original_height = image.get_size()
        
        width_ratio = target_width / original_width
        height_ratio = target_height / original_height
        scale_ratio = min(width_ratio, height_ratio)
        
        new_width = int(original_width * scale_ratio)
        new_height = int(original_height * scale_ratio)
        
        return pygame.transform.smoothscale(image, (new_width, new_height))

    def crop_image(self, image, x, y, width, height):
        """
        裁剪图片的指定区域
        :param image: 原始图片
        :param x: 起始x坐标
        :param y: 起始y坐标
        :param width: 裁剪宽度
        :param height: 裁剪高度
        :return: 裁剪后的图片
        """
        rect = pygame.Rect(x, y, width, height)
        return image.subsurface(rect).copy()

    def split_image(self, image, grid_size):
        """
        将图片分割为指定数量的碎片
        :param image: 原始图片
        :param grid_size: 网格大小（如3表示3x3）
        :return: 碎片列表，按行优先顺序排列
        """
        pieces = []
        width, height = image.get_size()
        
        piece_width = width // grid_size
        piece_height = height // grid_size
        
        for row in range(grid_size):
            for col in range(grid_size):
                x = col * piece_width
                y = row * piece_height
                piece = self.crop_image(image, x, y, piece_width, piece_height)
                pieces.append(piece)
        
        return pieces
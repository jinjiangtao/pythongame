import pygame
from config import BORDER_COLOR, PIECE_BORDER_WIDTH

class PuzzlePiece:
    def __init__(self, image, correct_index, current_index):
        """
        拼图碎片类
        :param image: 碎片的图片内容
        :param correct_index: 正确的位置索引
        :param current_index: 当前位置索引
        """
        self.image = image
        self.correct_index = correct_index
        self.current_index = current_index
        self.rect = None
        self.is_highlighted = False
        self.is_selected = False

    def set_position(self, x, y):
        """
        设置碎片的显示位置
        :param x: x坐标
        :param y: y坐标
        """
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    def draw(self, screen):
        """
        绘制碎片到屏幕
        :param screen: pygame屏幕对象
        """
        if self.image:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        
        if self.is_highlighted:
            pygame.draw.rect(screen, (46, 204, 113), self.rect, 3)
        elif self.is_selected:
            pygame.draw.rect(screen, (230, 126, 34), self.rect, 3)
        else:
            pygame.draw.rect(screen, BORDER_COLOR, self.rect, PIECE_BORDER_WIDTH)

    def is_clicked(self, mouse_pos):
        """
        判断鼠标是否点击了该碎片
        :param mouse_pos: 鼠标位置
        :return: True表示点击了该碎片
        """
        if self.rect:
            return self.rect.collidepoint(mouse_pos)
        return False

    def is_in_correct_position(self):
        """
        判断碎片是否在正确的位置
        :return: True表示在正确位置
        """
        return self.current_index == self.correct_index

    def update_position(self, new_index):
        """
        更新碎片的当前位置索引
        :param new_index: 新的位置索引
        """
        self.current_index = new_index
import random
import time
from .puzzle_piece import PuzzlePiece
from .image_processor import ImageProcessor

class GameLogic:
    def __init__(self, grid_size=3):
        """
        游戏逻辑类
        :param grid_size: 网格大小（默认3x3）
        """
        self.grid_size = grid_size
        self.total_pieces = grid_size * grid_size
        self.pieces = []
        self.empty_index = 0
        self.steps = 0
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False
        self.image_processor = ImageProcessor()
        self.original_image = None
        self.hint_piece = None

    def load_image_and_split(self, image_path=None):
        """
        加载图片并分割为碎片
        :param image_path: 图片路径
        """
        self.original_image = self.image_processor.load_image(image_path)
        
        target_size = min(500, self.original_image.get_width(), self.original_image.get_height())
        self.original_image = self.image_processor.resize_image(
            self.original_image, target_size, target_size
        )
        
        piece_images = self.image_processor.split_image(self.original_image, self.grid_size)
        
        self.pieces = []
        for i in range(self.total_pieces - 1):
            piece = PuzzlePiece(piece_images[i], i, i)
            self.pieces.append(piece)
        
        self.empty_index = self.total_pieces - 1

    def shuffle_pieces(self):
        """
        随机打乱碎片位置，确保拼图可解
        """
        positions = list(range(self.total_pieces - 1))
        empty_row = self.empty_index // self.grid_size
        
        while True:
            random.shuffle(positions)
            
            inversions = self._count_inversions(positions)
            row_from_bottom = self.grid_size - empty_row
            
            if (self.grid_size % 2 == 1 and inversions % 2 == 0) or \
               (self.grid_size % 2 == 0 and (inversions + row_from_bottom) % 2 == 1):
                break
        
        for i, piece in enumerate(self.pieces):
            piece.current_index = positions[i]
        
        self._update_piece_order()

    def _count_inversions(self, arr):
        """
        计算逆序对数量
        :param arr: 数组
        :return: 逆序对数量
        """
        count = 0
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] > arr[j]:
                    count += 1
        return count

    def _update_piece_order(self):
        """
        根据current_index重新排序碎片列表
        """
        self.pieces.sort(key=lambda p: p.current_index)

    def get_adjacent_indices(self, index):
        """
        获取与指定位置相邻的位置列表
        :param index: 当前位置索引
        :return: 相邻位置索引列表
        """
        adjacent = []
        row = index // self.grid_size
        col = index % self.grid_size
        
        if row > 0:
            adjacent.append(index - self.grid_size)
        if row < self.grid_size - 1:
            adjacent.append(index + self.grid_size)
        if col > 0:
            adjacent.append(index - 1)
        if col < self.grid_size - 1:
            adjacent.append(index + 1)
        
        return adjacent

    def is_valid_move(self, piece_index):
        """
        判断碎片是否可以移动（与空白格相邻）
        :param piece_index: 碎片索引
        :return: True表示可以移动
        """
        adjacent_indices = self.get_adjacent_indices(self.empty_index)
        return piece_index in adjacent_indices

    def move_piece(self, piece_index):
        """
        移动碎片到空白格位置
        :param piece_index: 要移动的碎片索引
        :return: True表示移动成功
        """
        if not self.is_valid_move(piece_index):
            return False
        
        piece = self.pieces[piece_index]
        old_index = piece.current_index
        piece.update_position(self.empty_index)
        self.empty_index = old_index
        
        self._update_piece_order()
        self.steps += 1
        
        return True

    def check_win(self):
        """
        检查是否所有碎片都在正确位置
        :return: True表示拼图完成
        """
        for piece in self.pieces:
            if not piece.is_in_correct_position():
                return False
        return True

    def start_game(self):
        """
        开始游戏，初始化计时和步数
        """
        self.steps = 0
        self.start_time = time.time()
        self.elapsed_time = 0
        self.is_running = True
        self.hint_piece = None

    def update_timer(self):
        """
        更新游戏计时
        """
        if self.is_running and self.start_time is not None:
            self.elapsed_time = int(time.time() - self.start_time)

    def get_hint(self):
        """
        获取一个提示（找到一个不在正确位置的碎片）
        :return: 提示的碎片索引，如果所有碎片都正确返回None
        """
        misplaced = [i for i, piece in enumerate(self.pieces) 
                     if not piece.is_in_correct_position()]
        
        if misplaced:
            self.hint_piece = random.choice(misplaced)
            return self.hint_piece
        return None

    def reset_hint(self):
        """
        重置提示状态
        """
        self.hint_piece = None

    def reset_game(self):
        """
        重置游戏，重新打乱碎片
        """
        self.shuffle_pieces()
        self.steps = 0
        self.start_time = time.time()
        self.elapsed_time = 0
        self.hint_piece = None

    def get_piece_at_position(self, row, col):
        """
        获取指定行列位置的碎片
        :param row: 行号
        :param col: 列号
        :return: 碎片对象，如果是空白格返回None
        """
        index = row * self.grid_size + col
        if index == self.empty_index:
            return None
        
        for piece in self.pieces:
            if piece.current_index == index:
                return piece
        return None
import json
import os
from modules.light_cell import LightCell

LEVELS = [
    {"size": 3, "name": "入门", "grid": [
        [False, True, False],
        [True, False, True],
        [False, True, False]
    ]},
    {"size": 3, "name": "初级", "grid": [
        [True, True, False],
        [False, True, False],
        [True, False, True]
    ]},
    {"size": 4, "name": "普通", "grid": [
        [False, False, True, False],
        [True, False, False, True],
        [False, True, False, False],
        [False, False, True, False]
    ]},
    {"size": 4, "name": "进阶", "grid": [
        [True, False, True, False],
        [False, True, False, True],
        [True, False, True, False],
        [False, True, False, True]
    ]},
    {"size": 5, "name": "困难", "grid": [
        [False, True, False, True, False],
        [True, False, True, False, True],
        [False, True, False, True, False],
        [True, False, True, False, True],
        [False, True, False, True, False]
    ]},
    {"size": 5, "name": "专家", "grid": [
        [True, True, False, False, True],
        [False, True, True, True, False],
        [True, False, True, False, True],
        [False, True, True, True, False],
        [True, False, False, True, True]
    ]},
    {"size": 6, "name": "大师", "grid": [
        [False, False, True, True, False, False],
        [False, True, False, False, True, False],
        [True, False, False, False, False, True],
        [True, False, False, False, False, True],
        [False, True, False, False, True, False],
        [False, False, True, True, False, False]
    ]},
    {"size": 6, "name": "传说", "grid": [
        [True, False, False, False, False, True],
        [False, True, False, False, True, False],
        [False, False, True, True, False, False],
        [False, False, True, True, False, False],
        [False, True, False, False, True, False],
        [True, False, False, False, False, True]
    ]}
]

class GameLogic:
    def __init__(self):
        self.cells = []
        self.current_level = 0
        self.unlocked_levels = 1
        self.load_progress()
    
    def load_progress(self):
        try:
            if os.path.exists("progress.json"):
                with open("progress.json", "r") as f:
                    data = json.load(f)
                    self.unlocked_levels = data.get("unlocked_levels", 1)
        except:
            self.unlocked_levels = 1
    
    def save_progress(self):
        try:
            with open("progress.json", "w") as f:
                json.dump({"unlocked_levels": self.unlocked_levels}, f)
        except:
            pass
    
    def init_board(self, screen_width, screen_height, level_index=0):
        self.current_level = level_index
        level = LEVELS[level_index]
        size = level["size"]
        grid = level["grid"]
        
        cell_size = min(60, (min(screen_width, screen_height) - 100) // size)
        total_width = cell_size * size
        total_height = cell_size * size
        
        start_x = (screen_width - total_width) // 2
        start_y = (screen_height - total_height) // 2
        
        self.cells = []
        for row in range(size):
            row_cells = []
            for col in range(size):
                x = start_x + col * cell_size
                y = start_y + row * cell_size
                cell = LightCell(x, y, cell_size, row, col)
                cell.set_state(grid[row][col])
                row_cells.append(cell)
            self.cells.append(row_cells)
    
    def get_cell_size(self):
        if self.cells:
            return self.cells[0][0].size
        return 60
    
    def get_grid_size(self):
        if self.cells:
            return len(self.cells)
        return 3
    
    def handle_click(self, mouse_pos):
        for row in self.cells:
            for cell in row:
                if cell.is_clicked(mouse_pos):
                    self.toggle_cell(cell.row, cell.col)
                    return True
        return False
    
    def toggle_cell(self, row, col):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
        
        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc
            
            if 0 <= new_row < len(self.cells) and 0 <= new_col < len(self.cells[0]):
                self.cells[new_row][new_col].toggle()
    
    def check_win(self):
        for row in self.cells:
            for cell in row:
                if not cell.is_on:
                    return False
        return True
    
    def unlock_next_level(self):
        if self.current_level + 1 < len(LEVELS) and self.current_level + 2 > self.unlocked_levels:
            self.unlocked_levels = self.current_level + 2
            self.save_progress()
    
    def reset_level(self):
        self.init_board(800, 600, self.current_level)
    
    def draw(self, screen):
        for row in self.cells:
            for cell in row:
                cell.draw(screen)
    
    def update_hover(self, mouse_pos):
        for row in self.cells:
            for cell in row:
                cell.check_hover(mouse_pos)
    
    def get_hint(self):
        for row in self.cells:
            for cell in row:
                if not cell.is_on:
                    return (cell.row, cell.col)
        return None
    
    def get_level_info(self, level_index):
        if 0 <= level_index < len(LEVELS):
            return LEVELS[level_index]
        return None
    
    def get_total_levels(self):
        return len(LEVELS)
    
    def is_level_unlocked(self, level_index):
        return level_index < self.unlocked_levels
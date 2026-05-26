import json
import os
import random
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
    ], "obstacles": [(1, 1), (2, 2)]},
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
    ], "frozen": [(2, 2)]},
    {"size": 6, "name": "大师", "grid": [
        [False, False, True, True, False, False],
        [False, True, False, False, True, False],
        [True, False, False, False, False, True],
        [True, False, False, False, False, True],
        [False, True, False, False, True, False],
        [False, False, True, True, False, False]
    ], "obstacles": [(2, 3), (3, 2)]},
    {"size": 6, "name": "传说", "grid": [
        [True, False, False, False, False, True],
        [False, True, False, False, True, False],
        [False, False, True, True, False, False],
        [False, False, True, True, False, False],
        [False, True, False, False, True, False],
        [True, False, False, False, False, True]
    ], "obstacles": [(1, 4), (4, 1)], "frozen": [(2, 2), (3, 3)]}
]

class GameLogic:
    def __init__(self):
        self.cells = []
        self.current_level = 0
        self.unlocked_levels = 1
        self.save_manager = None
        self.settings = None
        self.theme = None
        
        self.load_progress()
    
    def set_save_manager(self, save_manager):
        self.save_manager = save_manager
    
    def set_settings(self, settings):
        self.settings = settings
        self.theme = settings.get_theme()
    
    def set_theme(self, theme):
        self.theme = theme
    
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
        
        cell_size = min(60, (min(screen_width, screen_height) - 120) // size)
        total_width = cell_size * size
        total_height = cell_size * size
        
        start_x = (screen_width - total_width) // 2
        start_y = (screen_height - total_height) // 2 + 50
        
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
        
        obstacles = level.get("obstacles", [])
        for row, col in obstacles:
            if 0 <= row < size and 0 <= col < size:
                self.cells[row][col].set_obstacle(True)
        
        frozen = level.get("frozen", [])
        for row, col in frozen:
            if 0 <= row < size and 0 <= col < size:
                self.cells[row][col].set_frozen(True)
    
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
                if not cell.is_obstacle and not cell.is_frozen and not cell.is_on:
                    return False
        return True
    
    def check_failure(self, steps, time):
        if self.settings:
            mode = self.settings.get_mode()
            difficulty = self.settings.get_difficulty()
            
            if mode == "timed" and difficulty["time_limit"] > 0:
                if time >= difficulty["time_limit"]:
                    return True, "时间耗尽"
            
            if mode == "limited_steps" and difficulty["step_limit"] > 0:
                if steps >= difficulty["step_limit"]:
                    return True, "步数耗尽"
            
            if mode == "classic":
                if difficulty["time_limit"] > 0 and time >= difficulty["time_limit"]:
                    return True, "时间耗尽"
                if difficulty["step_limit"] > 0 and steps >= difficulty["step_limit"]:
                    return True, "步数耗尽"
        
        return False, ""
    
    def calculate_stars(self, steps, time):
        stars = 0
        
        if self.settings:
            difficulty = self.settings.get_difficulty()
            
            time_limit = difficulty["time_limit"] if difficulty["time_limit"] > 0 else 120
            step_limit = difficulty["step_limit"] if difficulty["step_limit"] > 0 else 30
            
            if time <= time_limit / 3:
                stars += 1
            elif time <= time_limit / 2:
                stars += 1
            elif time <= time_limit:
                stars += 1
            
            if steps <= step_limit / 3:
                stars += 1
            elif steps <= step_limit / 2:
                stars += 1
            elif steps <= step_limit:
                stars += 1
            
            stars = min(3, max(1, stars // 2))
        else:
            if steps <= 10:
                stars = 3
            elif steps <= 20:
                stars = 2
            else:
                stars = 1
        
        return stars
    
    def unlock_next_level(self):
        if self.save_manager:
            self.save_manager.unlock_level(self.current_level + 1)
            self.save_manager.complete_level(self.current_level)
        else:
            if self.current_level + 1 < len(LEVELS) and self.current_level + 2 > self.unlocked_levels:
                self.unlocked_levels = self.current_level + 2
                self.save_progress()
    
    def reset_level(self):
        self.init_board(800, 600, self.current_level)
    
    def draw(self, screen):
        theme = self.theme if self.theme else {
            "cell_on": (255, 255, 0),
            "cell_off": (128, 128, 128),
            "cell_hover": (255, 165, 0),
            "cell_border": (0, 0, 0),
            "glow_color": (255, 255, 100)
        }
        
        for row in self.cells:
            for cell in row:
                cell.draw(screen, theme)
    
    def update_hover(self, mouse_pos):
        for row in self.cells:
            for cell in row:
                cell.check_hover(mouse_pos)
    
    def get_hint(self):
        for row in self.cells:
            for cell in row:
                if not cell.is_on and not cell.is_obstacle and not cell.is_frozen:
                    return (cell.row, cell.col)
        return None
    
    def get_hint_cell(self, row, col):
        if 0 <= row < len(self.cells) and 0 <= col < len(self.cells[0]):
            return self.cells[row][col]
        return None
    
    def get_level_info(self, level_index):
        if 0 <= level_index < len(LEVELS):
            return LEVELS[level_index]
        return None
    
    def get_total_levels(self):
        return len(LEVELS)
    
    def is_level_unlocked(self, level_index):
        if self.save_manager:
            return self.save_manager.is_level_unlocked(level_index)
        return level_index < self.unlocked_levels
    
    def get_unlocked_levels(self):
        if self.save_manager:
            return self.save_manager.get_unlocked_levels()
        return self.unlocked_levels
    
    def get_completed_levels(self):
        if self.save_manager:
            return self.save_manager.get_total_completed()
        return 0
    
    def get_level_stars(self, level_index):
        if self.save_manager:
            return self.save_manager.get_stars(level_index)
        return 0
    
    def set_level_stars(self, level_index, stars):
        if self.save_manager:
            self.save_manager.set_stars(level_index, stars)
    
    def get_best_time(self, level_index):
        if self.save_manager:
            return self.save_manager.get_best_time(level_index)
        return 0
    
    def set_best_time(self, level_index, time):
        if self.save_manager:
            self.save_manager.set_best_time(level_index, time)
    
    def get_best_steps(self, level_index):
        if self.save_manager:
            return self.save_manager.get_best_steps(level_index)
        return 0
    
    def set_best_steps(self, level_index, steps):
        if self.save_manager:
            self.save_manager.set_best_steps(level_index, steps)
    
    def get_board_center(self):
        if self.cells:
            size = len(self.cells)
            cell_size = self.cells[0][0].size
            start_x = self.cells[0][0].x
            start_y = self.cells[0][0].y
            
            center_x = start_x + (size * cell_size) // 2
            center_y = start_y + (size * cell_size) // 2
            return (center_x, center_y)
        return (400, 300)
    
    def get_all_non_obstacle_cells(self):
        cells = []
        for row in self.cells:
            for cell in row:
                if not cell.is_obstacle:
                    cells.append(cell)
        return cells
import pygame
from config import (
    GRID_ROWS, GRID_COLS, CELL_SIZE, CELL_PADDING,
    TOP_BAR_HEIGHT, SIDE_PANEL_WIDTH, GAME_TIME_INTERVAL, CROPS
)
from model.farm_model import CropState


class FarmController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True
        self.message = ""
        self.last_time_update = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def handle_click(self, pos):
        x, y = pos
        
        if x < SIDE_PANEL_WIDTH and y > TOP_BAR_HEIGHT + 40:
            self.handle_side_panel_click(y)
            return
        
        grid_x = SIDE_PANEL_WIDTH + 20
        grid_y = TOP_BAR_HEIGHT + 20
        
        if x < grid_x or y < grid_y:
            return
        
        col = (x - grid_x) // (CELL_SIZE + CELL_PADDING)
        row = (y - grid_y) // (CELL_SIZE + CELL_PADDING)
        
        if row >= GRID_ROWS or col >= GRID_COLS:
            return
        
        cell = self.model.get_cell(row, col)
        
        if cell.state == CropState.EMPTY:
            self.model.plant_crop(row, col)
            self.message = f"已播种 {CROPS[self.model.selected_crop]['name']}"
        elif cell.state == CropState.MATURE:
            value = self.model.harvest_crop(row, col)
            self.message = f"收获成功！获得 {value} 金币"
        elif cell.state in (CropState.PLANTED, CropState.GROWING):
            self.message = "作物生长中..."

    def handle_side_panel_click(self, y):
        crop_y_start = TOP_BAR_HEIGHT + 135
        crop_y_interval = 22
        
        for i, crop_id in enumerate(CROPS.keys()):
            crop_y = crop_y_start + i * crop_y_interval
            if crop_y <= y <= crop_y + 20:
                self.model.set_selected_crop(crop_id)
                self.message = f"已选择 {CROPS[crop_id]['name']}"
                break

    def update_time(self):
        current_ticks = pygame.time.get_ticks()
        if current_ticks - self.last_time_update >= GAME_TIME_INTERVAL:
            self.model.update_day()
            self.last_time_update = current_ticks
            self.message = f"第 {self.model.current_day} 天开始"

    def reset_game(self):
        self.model.__init__(GRID_ROWS, GRID_COLS)
        self.message = "游戏已重置"

    def run(self):
        while self.running:
            self.handle_events()
            self.update_time()
            self.view.draw(self.model, self.message)
            pygame.time.delay(50)

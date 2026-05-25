import pygame
from config import (
    GRID_ROWS, GRID_COLS, CELL_SIZE, CELL_PADDING,
    TOP_BAR_HEIGHT, SIDE_PANEL_WIDTH, BOTTOM_BAR_HEIGHT,
    GAME_TIME_INTERVAL, STAMINA_RECOVER_INTERVAL, CROPS
)
from model.farm_model import CropState


class FarmController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True
        self.message = ""
        self.message_timer = 0
        self.last_time_update = pygame.time.get_ticks()
        self.last_stamina_recover = pygame.time.get_ticks()
        self.show_backpack = False
        self.show_shop = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)
            
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event.pos)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    self.close_popups()

    def handle_click(self, pos):
        if self.show_backpack:
            if self.view.get_popup_close_button(pos, "backpack"):
                self.show_backpack = False
                return
            
            crop_name = self.view.get_backpack_sell_button(pos, self.model)
            if crop_name:
                success, msg = self.model.sell_crop(crop_name, 1)
                self.message = msg
                self.message_timer = pygame.time.get_ticks()
                return
        
        if self.show_shop:
            if self.view.get_popup_close_button(pos, "shop"):
                self.show_shop = False
                return
            
            crop_id = self.view.get_shop_buy_button(pos)
            if crop_id:
                success, msg = self.model.buy_seed(crop_id)
                self.message = msg
                self.message_timer = pygame.time.get_ticks()
                return
        
        side_button = self.view.get_side_button_click(pos)
        if side_button:
            self.handle_side_button(side_button)
            return
        
        bottom_button = self.view.get_bottom_button_click(pos)
        if bottom_button:
            self.handle_bottom_button(bottom_button)
            return
        
        grid_cell = self.view.get_grid_cell(pos)
        if grid_cell:
            row, col = grid_cell
            self.handle_grid_click(row, col)

    def handle_side_button(self, button):
        if button == "backpack":
            self.show_backpack = not self.show_backpack
            self.show_shop = False
        elif button == "shop":
            self.show_shop = not self.show_shop
            self.show_backpack = False
        elif button == "refresh":
            self.reset_game()

    def handle_bottom_button(self, crop_id):
        success, msg = self.model.set_selected_crop(crop_id)
        self.message = msg
        self.message_timer = pygame.time.get_ticks()

    def handle_grid_click(self, row, col):
        cell = self.model.get_cell(row, col)
        
        if cell.state == CropState.EMPTY:
            success, msg = self.model.plant_crop(row, col)
            self.message = msg
            self.message_timer = pygame.time.get_ticks()
        elif cell.state == CropState.MATURE:
            value, msg = self.model.harvest_crop(row, col)
            self.message = msg
            self.message_timer = pygame.time.get_ticks()
        elif cell.state in (CropState.PLANTED, CropState.GROWING):
            self.message = "作物生长中..."
            self.message_timer = pygame.time.get_ticks()

    def handle_mouse_motion(self, pos):
        if not self.show_backpack and not self.show_shop:
            self.view.hover_cell = self.view.get_grid_cell(pos)
        else:
            self.view.hover_cell = None

    def close_popups(self):
        self.show_backpack = False
        self.show_shop = False

    def update_time(self):
        current_ticks = pygame.time.get_ticks()
        
        if current_ticks - self.last_time_update >= GAME_TIME_INTERVAL:
            self.model.update_day()
            self.last_time_update = current_ticks
            self.message = f"第 {self.model.current_day} 天开始"
            self.message_timer = current_ticks
        
        if current_ticks - self.last_stamina_recover >= STAMINA_RECOVER_INTERVAL:
            self.model.recover_stamina(10)
            self.last_stamina_recover = current_ticks
        
        if current_ticks - self.message_timer > 2000:
            self.message = ""

    def reset_game(self):
        self.model.__init__(GRID_ROWS, GRID_COLS)
        self.message = "游戏已重置"
        self.message_timer = pygame.time.get_ticks()
        self.show_backpack = False
        self.show_shop = False

    def run(self):
        while self.running:
            self.handle_events()
            self.update_time()
            self.view.draw(self.model, self.message, self.show_backpack, self.show_shop)
            pygame.time.delay(50)

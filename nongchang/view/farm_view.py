import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRID_ROWS, GRID_COLS,
    CELL_SIZE, CELL_PADDING, TOP_BAR_HEIGHT, SIDE_PANEL_WIDTH,
    CROPS, COLORS
)
from model.farm_model import CropState


class FarmView:
    def __init__(self, screen):
        self.screen = screen
        self.font = self.get_font(24)
        self.small_font = self.get_font(18)
        self.grid_x = SIDE_PANEL_WIDTH + 20
        self.grid_y = TOP_BAR_HEIGHT + 20

    def get_font(self, size):
        import os
        font_paths = [
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simsun.ttc",
            "C:/Windows/Fonts/msyhbd.ttc",
            "C:/Windows/Fonts/msyhl.ttc",
            "C:/Windows/Fonts/kaiu.ttf",
            "C:/Windows/Fonts/fangsong.ttf",
            "C:/Windows/Fonts/STSong.ttf",
            "C:/Windows/Fonts/STHeiti.ttf",
            "C:\\Windows\\Fonts\\simhei.ttf",
            "C:\\Windows\\Fonts\\msyh.ttc",
            "C:\\Windows\\Fonts\\simsun.ttc",
            "/Library/Fonts/Songti.ttc",
            "/Library/Fonts/Hiragino Sans GB W3.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "simhei.ttf",
            "msyh.ttc",
            "simsun.ttc",
        ]
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font = pygame.font.Font(font_path, size)
                    test_surface = font.render("测试", True, (0, 0, 0))
                    if test_surface:
                        return font
                except:
                    continue
        try:
            font = pygame.font.Font(pygame.font.match_font('arial'), size)
            if font:
                return font
        except:
            pass
        return pygame.font.Font(None, size)

    def draw_top_bar(self, gold, day):
        pygame.draw.rect(self.screen, (60, 60, 60), (0, 0, SCREEN_WIDTH, TOP_BAR_HEIGHT))
        gold_text = self.font.render(f"金币: {gold}", True, COLORS["text"])
        day_text = self.font.render(f"第 {day} 天", True, COLORS["text"])
        self.screen.blit(gold_text, (20, 15))
        self.screen.blit(day_text, (SCREEN_WIDTH - 120, 15))

    def draw_background(self):
        self.screen.fill(COLORS["background"])
        pygame.draw.rect(
            self.screen, COLORS["water"],
            (0, TOP_BAR_HEIGHT, SCREEN_WIDTH, 40)
        )

    def draw_grid(self, model):
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                cell_x = self.grid_x + col * (CELL_SIZE + CELL_PADDING)
                cell_y = self.grid_y + row * (CELL_SIZE + CELL_PADDING)
                cell = model.get_cell(row, col)
                self.draw_cell(cell, cell_x, cell_y)

    def draw_cell(self, cell, x, y):
        pygame.draw.rect(self.screen, COLORS["soil"], (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, COLORS["soil_dark"], (x, y, CELL_SIZE, CELL_SIZE), 2)
        
        if cell.state == CropState.EMPTY:
            self.draw_empty_cell(x, y)
        elif cell.state == CropState.PLANTED:
            self.draw_planted_cell(x, y, cell)
        elif cell.state == CropState.GROWING:
            self.draw_growing_cell(x, y, cell)
        elif cell.state == CropState.MATURE:
            self.draw_mature_cell(x, y, cell)

    def draw_empty_cell(self, x, y):
        pygame.draw.line(self.screen, COLORS["soil_dark"], (x + 5, y + 5), (x + CELL_SIZE - 5, y + CELL_SIZE - 5), 2)
        pygame.draw.line(self.screen, COLORS["soil_dark"], (x + CELL_SIZE - 5, y + 5), (x + 5, y + CELL_SIZE - 5), 2)

    def draw_planted_cell(self, x, y, cell):
        crop_color = CROPS[cell.crop_type]["color"]
        seed_size = 8
        pygame.draw.circle(self.screen, crop_color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), seed_size)

    def draw_growing_cell(self, x, y, cell):
        crop_color = CROPS[cell.crop_type]["color"]
        stem_height = 30
        stem_width = 4
        center_x = x + CELL_SIZE // 2
        stem_y = y + CELL_SIZE // 2
        
        pygame.draw.rect(self.screen, (34, 139, 34), (center_x - stem_width // 2, y + CELL_SIZE - stem_height, stem_width, stem_height))
        
        leaf_size = 10
        pygame.draw.polygon(self.screen, (34, 139, 34), [
            (center_x, y + CELL_SIZE - stem_height),
            (center_x + leaf_size, y + CELL_SIZE - stem_height + leaf_size),
            (center_x - leaf_size, y + CELL_SIZE - stem_height + leaf_size)
        ])

    def draw_mature_cell(self, x, y, cell):
        crop_color = CROPS[cell.crop_type]["color"]
        center_x = x + CELL_SIZE // 2
        center_y = y + CELL_SIZE // 2
        
        pygame.draw.rect(self.screen, (34, 139, 34), (center_x - 3, y + 20, 6, CELL_SIZE - 30))
        
        for i in range(3):
            offset = (i - 1) * 15
            pygame.draw.circle(self.screen, crop_color, (center_x + offset, y + 25), 12)

    def draw_side_panel(self, model, message):
        pygame.draw.rect(self.screen, COLORS["panel"], (0, TOP_BAR_HEIGHT + 40, SIDE_PANEL_WIDTH, SCREEN_HEIGHT - TOP_BAR_HEIGHT - 40))
        
        title = self.font.render("农场指南", True, COLORS["text_dark"])
        self.screen.blit(title, (20, TOP_BAR_HEIGHT + 55))
        
        instructions = [
            "1. 点击空地播种",
            "2. 等待作物生长",
            "3. 成熟后收获",
            "4. 获得金币奖励",
            "",
            "时间每10秒更新",
            "作物会自动生长",
        ]
        
        y = TOP_BAR_HEIGHT + 90
        for line in instructions:
            text = self.small_font.render(line, True, COLORS["text_dark"])
            self.screen.blit(text, (20, y))
            y += 25
        
        pygame.draw.rect(self.screen, (200, 200, 200), (20, y + 10, SIDE_PANEL_WIDTH - 40, 60))
        crop_title = self.small_font.render("选择作物:", True, COLORS["text_dark"])
        self.screen.blit(crop_title, (30, y + 15))
        
        y += 35
        for crop_id, crop_data in CROPS.items():
            color = crop_data["color"]
            text = crop_data["name"] + f" ({crop_data['value']}金币)"
            is_selected = model.selected_crop == crop_id
            
            if is_selected:
                pygame.draw.rect(self.screen, (150, 150, 150), (25, y - 5, SIDE_PANEL_WIDTH - 50, 20))
            
            pygame.draw.circle(self.screen, color, (35, y + 5), 8)
            crop_text = self.small_font.render(text, True, COLORS["text_dark"])
            self.screen.blit(crop_text, (55, y))
            y += 22

        if message:
            pygame.draw.rect(self.screen, (255, 255, 200), (20, SCREEN_HEIGHT - 60, SIDE_PANEL_WIDTH - 40, 30))
            message_text = self.small_font.render(message, True, COLORS["text_dark"])
            self.screen.blit(message_text, (25, SCREEN_HEIGHT - 48))

    def draw(self, model, message):
        self.draw_background()
        self.draw_top_bar(model.gold, model.current_day)
        self.draw_grid(model)
        self.draw_side_panel(model, message)
        pygame.display.flip()

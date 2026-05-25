import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRID_ROWS, GRID_COLS,
    CELL_SIZE, CELL_PADDING, TOP_BAR_HEIGHT, SIDE_PANEL_WIDTH, BOTTOM_BAR_HEIGHT,
    CROPS, COLORS, MAX_STAMINA
)
from model.farm_model import CropState


class FarmView:
    def __init__(self, screen):
        self.screen = screen
        self.font = self.get_font(24)
        self.small_font = self.get_font(18)
        self.tiny_font = self.get_font(14)
        self.grid_x = SIDE_PANEL_WIDTH + 20
        self.grid_y = TOP_BAR_HEIGHT + 60
        self.water_height = 40
        self.hover_cell = None

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

    def draw_top_bar(self, gold, day, stamina, total_crops):
        pygame.draw.rect(self.screen, (60, 60, 60), (0, 0, SCREEN_WIDTH, TOP_BAR_HEIGHT))
        
        gold_text = self.font.render(f"💰 金币: {gold}", True, COLORS["gold"])
        day_text = self.font.render(f"📅 第 {day} 天", True, COLORS["text"])
        stamina_text = self.font.render(f"❤️ 体力: {stamina}/{MAX_STAMINA}", True, COLORS["stamina"])
        crops_text = self.font.render(f"🌱 作物: {total_crops}", True, (100, 200, 100))
        
        gold_x = 20
        stamina_x = gold_x + self.font.size(f"💰 金币: {gold}")[0] + 30
        crops_x = stamina_x + self.font.size(f"❤️ 体力: {stamina}/{MAX_STAMINA}")[0] + 140
        day_x = SCREEN_WIDTH - self.font.size(f"📅 第 {day} 天")[0] - 20
        
        self.screen.blit(gold_text, (gold_x, 15))
        self.screen.blit(stamina_text, (stamina_x, 15))
        self.screen.blit(crops_text, (crops_x, 15))
        self.screen.blit(day_text, (day_x, 15))
        
        stamina_bar_width = 120
        stamina_bar_height = 12
        stamina_bar_x = stamina_x + self.font.size(f"❤️ 体力: {stamina}/{MAX_STAMINA}")[0] + 10
        stamina_bar_y = TOP_BAR_HEIGHT // 2 - stamina_bar_height // 2
        
        pygame.draw.rect(self.screen, (100, 100, 100), (stamina_bar_x, stamina_bar_y, stamina_bar_width, stamina_bar_height))
        stamina_fill_width = int(stamina_bar_width * (stamina / MAX_STAMINA))
        pygame.draw.rect(self.screen, COLORS["stamina"], (stamina_bar_x, stamina_bar_y, stamina_fill_width, stamina_bar_height))

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

    def draw_side_panel(self):
        panel_top = TOP_BAR_HEIGHT + self.water_height
        panel_height = SCREEN_HEIGHT - panel_top - BOTTOM_BAR_HEIGHT
        pygame.draw.rect(self.screen, COLORS["panel"], (0, panel_top, SIDE_PANEL_WIDTH, panel_height))
        
        button_width = SIDE_PANEL_WIDTH - 20
        button_height = 45
        button_y = TOP_BAR_HEIGHT + self.water_height + 15
        
        buttons = [
            ("🎒 背包", (255, 192, 203)),
            ("🏪 商店", (135, 206, 235)),
            ("🔄 刷新", (144, 238, 144)),
        ]
        
        for i, (text, color) in enumerate(buttons):
            button_x = 10
            current_y = button_y + i * (button_height + 10)
            
            pygame.draw.rect(self.screen, color, (button_x, current_y, button_width, button_height))
            pygame.draw.rect(self.screen, (100, 100, 100), (button_x, current_y, button_width, button_height), 2)
            
            text_surface = self.font.render(text, True, COLORS["text_dark"])
            text_rect = text_surface.get_rect(center=(button_x + button_width // 2, current_y + button_height // 2))
            self.screen.blit(text_surface, text_rect)

    def draw_bottom_bar(self, model):
        pygame.draw.rect(self.screen, COLORS["panel"], (0, SCREEN_HEIGHT - BOTTOM_BAR_HEIGHT, SCREEN_WIDTH, BOTTOM_BAR_HEIGHT))
        
        title_text = self.font.render("🌱 选择种子:", True, COLORS["text_dark"])
        self.screen.blit(title_text, (20, SCREEN_HEIGHT - BOTTOM_BAR_HEIGHT + 15))
        
        button_width = 80
        button_height = 50
        start_x = 150
        
        for i, (crop_id, crop_data) in enumerate(CROPS.items()):
            button_x = start_x + i * (button_width + 15)
            button_y = SCREEN_HEIGHT - BOTTOM_BAR_HEIGHT + 10
            
            is_selected = model.selected_crop == crop_id
            color = COLORS["button_hover"] if is_selected else COLORS["button"]
            
            pygame.draw.rect(self.screen, color, (button_x, button_y, button_width, button_height))
            pygame.draw.rect(self.screen, COLORS["text_dark"], (button_x, button_y, button_width, button_height), 2)
            
            crop_color = crop_data["color"]
            pygame.draw.circle(self.screen, crop_color, (button_x + 20, button_y + button_height // 2), 12)
            
            name_text = self.small_font.render(crop_data["name"], True, COLORS["text_dark"])
            price_text = self.tiny_font.render(f"💰{crop_data['buy_price']}", True, COLORS["text_dark"])
            
            self.screen.blit(name_text, (button_x + 38, button_y + 10))
            self.screen.blit(price_text, (button_x + 38, button_y + 30))

    def draw_hover_tip(self, model, mouse_pos):
        if self.hover_cell is None:
            return
        
        row, col = self.hover_cell
        cell = model.get_cell(row, col)
        
        if cell.state in (CropState.PLANTED, CropState.GROWING):
            difficulty_multiplier = 1.0 + (model.current_day - 1) * 0.05
            progress = cell.get_growth_progress(model.current_day, difficulty_multiplier)
            crop_name = CROPS[cell.crop_type]["name"]
            
            tip_text = f"{crop_name} - 生长进度: {int(progress)}%"
            tip_surface = self.small_font.render(tip_text, True, COLORS["text_dark"])
            
            tip_x = mouse_pos[0] + 10
            tip_y = mouse_pos[1] + 10
            
            if tip_x + tip_surface.get_width() > SCREEN_WIDTH:
                tip_x = mouse_pos[0] - tip_surface.get_width() - 10
            if tip_y + tip_surface.get_height() > SCREEN_HEIGHT:
                tip_y = mouse_pos[1] - tip_surface.get_height() - 10
            
            pygame.draw.rect(self.screen, COLORS["popup_bg"], 
                           (tip_x - 5, tip_y - 5, tip_surface.get_width() + 10, tip_surface.get_height() + 10))
            pygame.draw.rect(self.screen, COLORS["popup_border"], 
                           (tip_x - 5, tip_y - 5, tip_surface.get_width() + 10, tip_surface.get_height() + 10), 1)
            self.screen.blit(tip_surface, (tip_x, tip_y))

    def draw_backpack_popup(self, model):
        popup_width = 400
        popup_height = 450
        popup_x = (SCREEN_WIDTH - popup_width) // 2
        popup_y = (SCREEN_HEIGHT - popup_height) // 2
        
        pygame.draw.rect(self.screen, COLORS["popup_bg"], (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.screen, COLORS["popup_border"], (popup_x, popup_y, popup_width, popup_height), 3)
        
        title_text = self.font.render("🎒 背包", True, COLORS["text_dark"])
        self.screen.blit(title_text, (popup_x + 20, popup_y + 15))
        
        close_button = pygame.draw.rect(self.screen, (255, 100, 100), (popup_x + popup_width - 50, popup_y + 10, 40, 30))
        close_text = self.font.render("✕", True, COLORS["text"])
        self.screen.blit(close_text, (popup_x + popup_width - 35, popup_y + 12))
        
        item_y = popup_y + 60
        for crop_id, count in model.backpack.items():
            if count > 0:
                crop_info = CROPS[crop_id]
                pygame.draw.circle(self.screen, crop_info["color"], (popup_x + 30, item_y + 15), 15)
                name_text = self.font.render(crop_info["name"], True, COLORS["text_dark"])
                count_text = self.font.render(f"x{count}", True, COLORS["text_dark"])
                price_text = self.small_font.render(f"💰{crop_info['sell_price']}", True, COLORS["gold"])
                
                self.screen.blit(name_text, (popup_x + 60, item_y))
                self.screen.blit(count_text, (popup_x + 150, item_y))
                self.screen.blit(price_text, (popup_x + 220, item_y))
                
                sell_button = pygame.draw.rect(self.screen, (100, 200, 100), (popup_x + 300, item_y, 80, 30))
                sell_text = self.small_font.render("出售", True, COLORS["text"])
                self.screen.blit(sell_text, (popup_x + 325, item_y + 5))
                
                item_y += 45
        
        if item_y == popup_y + 60:
            empty_text = self.font.render("背包是空的", True, COLORS["text_dark"])
            self.screen.blit(empty_text, (popup_x + popup_width // 2 - 60, popup_y + popup_height // 2))

    def draw_shop_popup(self, model):
        popup_width = 500
        popup_height = 400
        popup_x = (SCREEN_WIDTH - popup_width) // 2
        popup_y = (SCREEN_HEIGHT - popup_height) // 2
        
        pygame.draw.rect(self.screen, COLORS["popup_bg"], (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.screen, COLORS["popup_border"], (popup_x, popup_y, popup_width, popup_height), 3)
        
        title_text = self.font.render("🏪 商店", True, COLORS["text_dark"])
        self.screen.blit(title_text, (popup_x + 20, popup_y + 15))
        
        gold_text = self.font.render(f"💰 金币: {model.gold}", True, COLORS["gold"])
        self.screen.blit(gold_text, (popup_x + popup_width - 150, popup_y + 15))
        
        close_button = pygame.draw.rect(self.screen, (255, 100, 100), (popup_x + popup_width - 50, popup_y + 10, 40, 30))
        close_text = self.font.render("✕", True, COLORS["text"])
        self.screen.blit(close_text, (popup_x + popup_width - 35, popup_y + 12))
        
        tab_y = popup_y + 55
        sell_tab = pygame.draw.rect(self.screen, COLORS["button_hover"], (popup_x + 20, tab_y, 100, 35))
        buy_tab = pygame.draw.rect(self.screen, COLORS["button"], (popup_x + 130, tab_y, 100, 35))
        
        sell_text = self.small_font.render("出售", True, COLORS["text"])
        buy_text = self.small_font.render("购买", True, COLORS["text"])
        
        self.screen.blit(sell_text, (popup_x + 50, tab_y + 5))
        self.screen.blit(buy_text, (popup_x + 160, tab_y + 5))
        
        item_y = popup_y + 100
        for crop_id, crop_info in CROPS.items():
            pygame.draw.circle(self.screen, crop_info["color"], (popup_x + 40, item_y + 15), 15)
            
            name_text = self.font.render(crop_info["name"], True, COLORS["text_dark"])
            sell_price_text = self.small_font.render(f"售价: {crop_info['sell_price']}", True, (100, 200, 100))
            buy_price_text = self.small_font.render(f"进价: {crop_info['buy_price']}", True, (200, 100, 100))
            
            self.screen.blit(name_text, (popup_x + 70, item_y))
            self.screen.blit(sell_price_text, (popup_x + 200, item_y))
            self.screen.blit(buy_price_text, (popup_x + 320, item_y))
            
            buy_button = pygame.draw.rect(self.screen, (70, 130, 180), (popup_x + 420, item_y, 60, 30))
            buy_text = self.tiny_font.render("购买", True, COLORS["text"])
            self.screen.blit(buy_text, (popup_x + 435, item_y + 5))
            
            item_y += 45

    def draw(self, model, message, show_backpack, show_shop):
        self.draw_background()
        self.draw_top_bar(model.gold, model.current_day, model.stamina, model.get_total_crops())
        self.draw_grid(model)
        self.draw_side_panel()
        self.draw_bottom_bar(model)
        
        if show_backpack:
            self.draw_backpack_popup(model)
        if show_shop:
            self.draw_shop_popup(model)
        
        if message:
            pygame.draw.rect(self.screen, (255, 255, 200), (SIDE_PANEL_WIDTH + 20, SCREEN_HEIGHT - BOTTOM_BAR_HEIGHT - 40, 300, 30))
            message_text = self.small_font.render(message, True, COLORS["text_dark"])
            self.screen.blit(message_text, (SIDE_PANEL_WIDTH + 25, SCREEN_HEIGHT - BOTTOM_BAR_HEIGHT - 30))
        
        # 绘制悬停提示（在最后，确保它显示在最上层）
        mouse_pos = pygame.mouse.get_pos()
        self.draw_hover_tip(model, mouse_pos)
        
        pygame.display.flip()

    def get_side_button_click(self, pos):
        x, y = pos
        if x < SIDE_PANEL_WIDTH and y > TOP_BAR_HEIGHT + self.water_height:
            button_height = 45
            button_y_start = TOP_BAR_HEIGHT + self.water_height + 15
            
            for i in range(3):
                button_y = button_y_start + i * (button_height + 10)
                if button_y <= y <= button_y + button_height:
                    return ["backpack", "shop", "refresh"][i]
        return None

    def get_bottom_button_click(self, pos):
        x, y = pos
        if y > SCREEN_HEIGHT - BOTTOM_BAR_HEIGHT:
            button_width = 80
            button_height = 50
            start_x = 150
            button_y = SCREEN_HEIGHT - BOTTOM_BAR_HEIGHT + 10
            
            if button_y <= y <= button_y + button_height:
                for i, crop_id in enumerate(CROPS.keys()):
                    button_x = start_x + i * (button_width + 15)
                    if button_x <= x <= button_x + button_width:
                        return crop_id
        return None

    def get_grid_cell(self, pos):
        x, y = pos
        grid_x = SIDE_PANEL_WIDTH + 20
        grid_y = TOP_BAR_HEIGHT + 20
        
        if x < grid_x or y < grid_y:
            return None
        
        grid_bottom = grid_y + GRID_ROWS * (CELL_SIZE + CELL_PADDING)
        grid_right = grid_x + GRID_COLS * (CELL_SIZE + CELL_PADDING)
        
        if x > grid_right or y > grid_bottom:
            return None
        
        col = (x - grid_x) // (CELL_SIZE + CELL_PADDING)
        row = (y - grid_y) // (CELL_SIZE + CELL_PADDING)
        
        return (row, col)

    def get_popup_close_button(self, pos, popup_type):
        x, y = pos
        
        if popup_type == "backpack":
            popup_width = 400
            popup_height = 450
            popup_x = (SCREEN_WIDTH - popup_width) // 2
            popup_y = (SCREEN_HEIGHT - popup_height) // 2
            close_x, close_y = popup_x + popup_width - 50, popup_y + 10
            close_w, close_h = 40, 30
        elif popup_type == "shop":
            popup_width = 500
            popup_height = 400
            popup_x = (SCREEN_WIDTH - popup_width) // 2
            popup_y = (SCREEN_HEIGHT - popup_height) // 2
            close_x, close_y = popup_x + popup_width - 50, popup_y + 10
            close_w, close_h = 40, 30
        else:
            return False
        
        return close_x <= x <= close_x + close_w and close_y <= y <= close_y + close_h

    def get_backpack_sell_button(self, pos, model):
        popup_width = 400
        popup_height = 450
        popup_x = (SCREEN_WIDTH - popup_width) // 2
        popup_y = (SCREEN_HEIGHT - popup_height) // 2
        
        x, y = pos
        if not (popup_x <= x <= popup_x + popup_width and popup_y <= y <= popup_y + popup_height):
            return None
        
        item_y = popup_y + 60
        for crop_id, count in model.backpack.items():
            if count > 0:
                sell_x, sell_y = popup_x + 300, item_y
                sell_w, sell_h = 80, 30
                
                if sell_x <= x <= sell_x + sell_w and sell_y <= y <= sell_y + sell_h:
                    return crop_id
                
                item_y += 45
        
        return None

    def get_shop_buy_button(self, pos):
        popup_width = 500
        popup_height = 400
        popup_x = (SCREEN_WIDTH - popup_width) // 2
        popup_y = (SCREEN_HEIGHT - popup_height) // 2
        
        x, y = pos
        if not (popup_x <= x <= popup_x + popup_width and popup_y <= y <= popup_y + popup_height):
            return None
        
        item_y = popup_y + 100
        for crop_id in CROPS.keys():
            buy_x, buy_y = popup_x + 420, item_y
            buy_w, buy_h = 60, 30
            
            if buy_x <= x <= buy_x + buy_w and buy_y <= y <= buy_y + buy_h:
                return crop_id
            
            item_y += 45
        
        return None

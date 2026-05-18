from src.config import *

class GameMap:
    def __init__(self, level=1):
        self.level = level
        self.map_width = SCREEN_WIDTH // GRID_SIZE
        self.map_height = SCREEN_HEIGHT // GRID_SIZE
        self.tiles = []
        self.base_destroyed = False
        self.base_position = None
        self.generate_map()
    
    def generate_map(self):
        self.tiles = [[EMPTY for _ in range(self.map_width)] for _ in range(self.map_height)]
        
        self.place_base()
        self.place_walls()
        self.place_grass()
    
    def place_base(self):
        base_col = self.map_width // 2 - 1
        base_row = self.map_height - 1
        self.tiles[base_row][base_col] = BASE
        self.tiles[base_row][base_col + 1] = BASE
        self.base_position = (base_col * GRID_SIZE, base_row * GRID_SIZE)
    
    def place_walls(self):
        layouts = [
            [
                "          ",
                "  BB  BB  ",
                "  BB  BB  ",
                "          ",
                "  BB  BB  ",
                "  BB  BB  ",
                "    SS    ",
                "          ",
                "BB    BB  ",
                "BB    BB  ",
                "  BB  BB  ",
                "  BB  BB  ",
                "          ",
                "      BB  ",
                "      BB  "
            ],
            [
                "    BB    ",
                "    BB    ",
                "  BB  BB  ",
                "  BB  BB  ",
                "SS    SS  ",
                "          ",
                "  BB  BB  ",
                "  BB  BB  ",
                "    BB    ",
                "    BB    ",
                "BB  SS  BB",
                "          ",
                "    BB    ",
                "    BB    ",
                "  BB  BB  "
            ],
            [
                "BB    BB  ",
                "BB    BB  ",
                "  SS  SS  ",
                "          ",
                "BB  BB  BB",
                "BB  BB  BB",
                "    SS    ",
                "          ",
                "  BB  BB  ",
                "  BB  BB  ",
                "SS    SS  ",
                "          ",
                "BB    BB  ",
                "BB    BB  ",
                "  BB  BB  "
            ],
            [
                "  BB  BB  ",
                "  BB  BB  ",
                "BB    BB  ",
                "BB    BB  ",
                "  SS  SS  ",
                "          ",
                "BB  BB  BB",
                "    SS    ",
                "BB  BB  BB",
                "          ",
                "  SS  SS  ",
                "BB    BB  ",
                "BB    BB  ",
                "  BB  BB  ",
                "  BB  BB  "
            ],
            [
                "BB    BB  ",
                "BB    BB  ",
                "  BB  BB  ",
                "  BB  BB  ",
                "SS    SS  ",
                "          ",
                "  BB  BB  ",
                "  BB  BB  ",
                "    SS    ",
                "  BB  BB  ",
                "  BB  BB  ",
                "SS    SS  ",
                "  BB  BB  ",
                "  BB  BB  ",
                "BB    BB  "
            ]
        ]
        
        layout = layouts[min(self.level - 1, len(layouts) - 1)]
        
        for row, line in enumerate(layout):
            if row >= self.map_height:
                break
            for col, char in enumerate(line):
                if col >= self.map_width:
                    break
                if char == 'B':
                    self.tiles[row][col] = BRICK
                elif char == 'S':
                    self.tiles[row][col] = STEEL
    
    def place_grass(self):
        grass_positions = [
            (2, 3), (2, 4), (3, 3), (3, 4),
            (2, 9), (2, 10), (3, 9), (3, 10),
            (7, 2), (7, 3), (8, 2), (8, 3),
            (7, 16), (7, 17), (8, 16), (8, 17),
            (11, 6), (11, 7), (12, 6), (12, 7),
            (11, 12), (11, 13), (12, 12), (12, 13)
        ]
        
        for row, col in grass_positions:
            if row < self.map_height and col < self.map_width:
                self.tiles[row][col] = GRASS
    
    def check_collision(self, rect):
        left = rect.left // GRID_SIZE
        right = (rect.right - 1) // GRID_SIZE
        top = rect.top // GRID_SIZE
        bottom = (rect.bottom - 1) // GRID_SIZE
        
        for row in range(top, bottom + 1):
            for col in range(left, right + 1):
                if row >= 0 and row < self.map_height and col >= 0 and col < self.map_width:
                    tile = self.tiles[row][col]
                    if tile == BRICK or tile == STEEL or tile == BASE:
                        return True
        return False
    
    def check_bullet_collision(self, bullet):
        rect = bullet.get_rect()
        center_x = rect.centerx // GRID_SIZE
        center_y = rect.centery // GRID_SIZE
        
        if center_x < 0 or center_x >= self.map_width or center_y < 0 or center_y >= self.map_height:
            return None, None
        
        tile = self.tiles[center_y][center_x]
        
        if tile == BRICK:
            self.tiles[center_y][center_x] = EMPTY
            return "destroy", (center_x, center_y)
        elif tile == STEEL:
            return "block", None
        elif tile == BASE:
            self.base_destroyed = True
            return "base", None
        
        return None, None
    
    def is_grass(self, x, y):
        col = x // GRID_SIZE
        row = y // GRID_SIZE
        if row >= 0 and row < self.map_height and col >= 0 and col < self.map_width:
            return self.tiles[row][col] == GRASS
        return False
    
    def draw(self, screen):
        for row in range(self.map_height):
            for col in range(self.map_width):
                tile = self.tiles[row][col]
                x = col * GRID_SIZE
                y = row * GRID_SIZE
                
                if tile == BRICK:
                    pygame.draw.rect(screen, BROWN, (x, y, GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(screen, (160, 80, 20), 
                                    (x + 2, y + 2, GRID_SIZE - 4, GRID_SIZE - 4))
                    pygame.draw.line(screen, (100, 50, 10), (x, y + GRID_SIZE // 2), 
                                    (x + GRID_SIZE, y + GRID_SIZE // 2))
                    pygame.draw.line(screen, (100, 50, 10), (x + GRID_SIZE // 2, y), 
                                    (x + GRID_SIZE // 2, y + GRID_SIZE))
                elif tile == STEEL:
                    pygame.draw.rect(screen, GRAY, (x, y, GRID_SIZE, GRID_SIZE))
                    pygame.draw.rect(screen, (180, 180, 180), 
                                    (x + 3, y + 3, GRID_SIZE - 6, GRID_SIZE - 6))
                    pygame.draw.line(screen, (150, 150, 150), (x + 5, y + 5), 
                                    (x + GRID_SIZE - 5, y + GRID_SIZE - 5))
                    pygame.draw.line(screen, (150, 150, 150), (x + GRID_SIZE - 5, y + 5), 
                                    (x + 5, y + GRID_SIZE - 5))
                elif tile == BASE:
                    pygame.draw.rect(screen, YELLOW, (x, y, GRID_SIZE, GRID_SIZE))
                    pygame.draw.circle(screen, RED, 
                                        (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 
                                        GRID_SIZE // 3)
    
    def draw_grass(self, screen):
        for row in range(self.map_height):
            for col in range(self.map_width):
                if self.tiles[row][col] == GRASS:
                    x = col * GRID_SIZE
                    y = row * GRID_SIZE
                    pygame.draw.rect(screen, GREEN_GRASS, (x, y, GRID_SIZE, GRID_SIZE))
                    for i in range(5):
                        for j in range(5):
                            if (i + j) % 2 == 0:
                                pygame.draw.rect(screen, (20, 100, 20), 
                                                (x + i * 8 + 2, y + j * 8 + 2, 4, 4))
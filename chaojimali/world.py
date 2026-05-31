from game_platform import Platform
from coin import Coin
from enemy import Enemy
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT

class World:
    def __init__(self):
        self.platforms = []
        self.coins = []
        self.enemies = []
        self.world_width = 2000
        self.load_level()
    
    def load_level(self):
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        
        self.platforms.append(Platform(0, ground_y, self.world_width, GROUND_HEIGHT))
        
        # 确保所有平台尺寸都是整数，避免晃动问题
        self.platforms.append(Platform(300, 400, int(PLATFORM_WIDTH), PLATFORM_HEIGHT))
        self.platforms.append(Platform(500, 320, int(PLATFORM_WIDTH * 1.5), PLATFORM_HEIGHT))
        self.platforms.append(Platform(700, 240, int(PLATFORM_WIDTH), PLATFORM_HEIGHT))
        self.platforms.append(Platform(900, 400, int(PLATFORM_WIDTH), PLATFORM_HEIGHT))
        self.platforms.append(Platform(1100, 320, int(PLATFORM_WIDTH * 2), PLATFORM_HEIGHT))
        self.platforms.append(Platform(1400, 240, int(PLATFORM_WIDTH), PLATFORM_HEIGHT))
        self.platforms.append(Platform(1600, 400, int(PLATFORM_WIDTH * 1.5), PLATFORM_HEIGHT))
        
        self.coins.append(Coin(350, 360))
        self.coins.append(Coin(400, 360))
        self.coins.append(Coin(550, 280))
        self.coins.append(Coin(600, 280))
        self.coins.append(Coin(650, 280))
        self.coins.append(Coin(750, 200))
        self.coins.append(Coin(950, 360))
        self.coins.append(Coin(1000, 360))
        self.coins.append(Coin(1150, 280))
        self.coins.append(Coin(1200, 280))
        self.coins.append(Coin(1250, 280))
        self.coins.append(Coin(1300, 280))
        self.coins.append(Coin(1450, 200))
        self.coins.append(Coin(1650, 360))
        self.coins.append(Coin(1700, 360))
        self.coins.append(Coin(1750, 360))
        
        self.enemies.append(Enemy(450, ground_y - 40, 80))
        self.enemies.append(Enemy(750, ground_y - 40, 80))
        self.enemies.append(Enemy(1300, ground_y - 40, 100))
        self.enemies.append(Enemy(1500, 360 - 40, 120))
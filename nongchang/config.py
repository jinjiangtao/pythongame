SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

GRID_ROWS = 5
GRID_COLS = 6
CELL_SIZE = 80
CELL_PADDING = 10

TOP_BAR_HEIGHT = 60
SIDE_PANEL_WIDTH = 120
BOTTOM_BAR_HEIGHT = 80

GAME_TIME_INTERVAL = 10000
STAMINA_RECOVER_INTERVAL = 5000

CROPS = {
    "wheat": {"name": "小麦", "growth_days": 2, "sell_price": 10, "buy_price": 3, "color": (244, 214, 66)},
    "corn": {"name": "玉米", "growth_days": 3, "sell_price": 15, "buy_price": 5, "color": (255, 204, 0)},
    "carrot": {"name": "胡萝卜", "growth_days": 1, "sell_price": 8, "buy_price": 2, "color": (255, 102, 51)},
    "tomato": {"name": "番茄", "growth_days": 4, "sell_price": 20, "buy_price": 8, "color": (255, 51, 51)},
    "potato": {"name": "土豆", "growth_days": 2, "sell_price": 12, "buy_price": 4, "color": (139, 69, 19)},
    "rice": {"name": "水稻", "growth_days": 5, "sell_price": 25, "buy_price": 10, "color": (200, 200, 200)},
}

INITIAL_GOLD = 50
INITIAL_STAMINA = 100
MAX_STAMINA = 100
PLANT_COST = 10
HARVEST_COST = 5

COLORS = {
    "background": (135, 206, 235),
    "soil": (139, 69, 19),
    "soil_dark": (101, 67, 33),
    "water": (0, 102, 204),
    "text": (255, 255, 255),
    "text_dark": (0, 0, 0),
    "panel": (245, 222, 179),
    "panel_dark": (218, 193, 144),
    "mature": (34, 139, 34),
    "stamina": (255, 100, 100),
    "gold": (255, 204, 0),
    "button": (70, 130, 180),
    "button_hover": (100, 160, 210),
    "button_active": (50, 100, 150),
    "popup_bg": (255, 255, 255),
    "popup_border": (100, 100, 100),
}

ICONS = {
    "backpack": "🎒",
    "shop": "🏪",
    "refresh": "🔄",
    "seed": "🌱",
    "coin": "💰",
    "heart": "❤️",
}

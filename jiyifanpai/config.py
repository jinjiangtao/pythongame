# 游戏配置常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
GRID_COLS = 6
GRID_ROWS = 6
TOTAL_CARDS = GRID_COLS * GRID_ROWS  # 36 cards
TOTAL_PAIRS = TOTAL_CARDS // 2  # 18 pairs

# 卡片配置
CARD_WIDTH = 100
CARD_HEIGHT = 120
CARD_MARGIN = 10
CARD_PADDING = 15

# 颜色定义
BG_COLOR = (30, 30, 50)
CARD_BACK_COLOR = (100, 100, 120)
CARD_FRONT_COLOR = (255, 255, 255)
CARD_MATCHED_COLOR = (150, 150, 150)
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (100, 200, 100)
WARNING_COLOR = (255, 100, 100)

# 游戏时间
GAME_TIME = 90  # 秒
FLIP_DELAY = 600  # 毫秒
PREVIEW_TIME = 1000  # 毫秒

# UI位置
UI_TOP_MARGIN = 30
STATS_LEFT_MARGIN = 20
STATS_RIGHT_MARGIN = 20

# 形状类型
SHAPE_TYPES = ['circle', 'triangle', 'square', 'cross', 'pentagon', 'diamond']

# 形状颜色（每种形状一个颜色）
SHAPE_COLORS = {
    'circle': (255, 100, 100),      # 红色
    'triangle': (100, 255, 100),    # 绿色
    'square': (100, 100, 255),      # 蓝色
    'cross': (255, 255, 100),       # 黄色
    'pentagon': (255, 100, 255),    # 紫色
    'diamond': (100, 255, 255)      # 青色
}

def get_grid_offset():
    """计算网格在屏幕上的偏移量"""
    total_width = GRID_COLS * CARD_WIDTH + (GRID_COLS - 1) * CARD_MARGIN
    total_height = GRID_ROWS * CARD_HEIGHT + (GRID_ROWS - 1) * CARD_MARGIN
    offset_x = (SCREEN_WIDTH - total_width) // 2
    offset_y = (SCREEN_HEIGHT - total_height) // 2 + 50
    return offset_x, offset_y

def get_card_position(index):
    """根据卡片索引计算其在屏幕上的位置"""
    offset_x, offset_y = get_grid_offset()
    col = index % GRID_COLS
    row = index // GRID_COLS
    x = offset_x + col * (CARD_WIDTH + CARD_MARGIN)
    y = offset_y + row * (CARD_HEIGHT + CARD_MARGIN)
    return x, y

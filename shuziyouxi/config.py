import customtkinter as ctk

class Config:
    WINDOW_TITLE = "小学数学数字游戏"
    WINDOW_SIZE = "800x650"
    
    COLORS = {
        "primary": "#4ECDC4",
        "secondary": "#45B7D1",
        "success": "#27AE60",
        "error": "#E74C3C",
        "warning": "#F39C12",
        "bg_light": "#F8FAFC",
        "bg_dark": "#1E293B",
        "card_light": "#FFFFFF",
        "card_dark": "#334155",
    }
    
    FONTS = {
        "title": ("Microsoft YaHei", 24, "bold"),
        "subtitle": ("Microsoft YaHei", 20, "bold"),
        "button": ("Microsoft YaHei", 16, "bold"),
        "label": ("Microsoft YaHei", 14),
        "large_number": ("Microsoft YaHei", 36, "bold"),
    }
    
    GAME_CONFIG = {
        "questions_per_level": 5,
        "pass_rate": 0.8,
    }
    
    DIFFICULTY_LEVELS = {
        1: {"name": "入门级", "grade": "一年级上", "description": "数数、10以内数的认识"},
        2: {"name": "基础级", "grade": "一年级下", "description": "20以内加减法"},
        3: {"name": "进阶级", "grade": "二年级上", "description": "100以内加减法、表内乘法"},
        4: {"name": "挑战级", "grade": "二年级下-三年级", "description": "表内除法、两步运算、比大小"},
    }
    
    TIME_LIMITS = {
        1: 60,
        2: 40,
        3: 30,
        4: 25,
    }
    
    QUESTION_TYPES = {
        "counting": {"name": "数数", "icon": "🔢"},
        "addition": {"name": "加法", "icon": "➕"},
        "subtraction": {"name": "减法", "icon": "➖"},
        "multiplication": {"name": "乘法", "icon": "✖️"},
        "division": {"name": "除法", "icon": "➗"},
        "compare": {"name": "比大小", "icon": "⚖️"},
        "mixed": {"name": "混合运算", "icon": "🧮"},
    }
    
    ENCOURAGEMENTS = [
        "🎉 太棒了！你算得又快又准！",
        "👏 真聪明！答对了！",
        "🌟 完美！你真厉害！",
        "💯 正确！继续加油！",
        "🎊 答对啦！你真棒！",
        "🏆 数学小天才！",
        "✨ 太厉害了！",
        "👍 做得好！",
    ]
    
    HINTS = [
        "别灰心，再算一遍试试！",
        "先算加法再算乘法哦",
        "仔细想一想，答案就在眼前！",
        "再检查一下，你可以的！",
        "不要着急，慢慢来！",
    ]
    
    BADGES = {
        1: {"name": "数数小能手", "icon": "🌟", "description": "完成入门级挑战"},
        2: {"name": "计算小达人", "icon": "🏆", "description": "完成基础级挑战"},
        3: {"name": "乘法小专家", "icon": "💎", "description": "完成进阶级挑战"},
        4: {"name": "数学全能王", "icon": "👑", "description": "完成挑战级挑战"},
    }

def setup_customtkinter():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
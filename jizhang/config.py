import os

DATABASE_NAME = "accounting.db"
DATABASE_PATH = os.path.join(os.path.dirname(__file__), DATABASE_NAME)

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
WINDOW_TITLE = "个人记账管理系统"

THEME_COLOR = "#2c3e50"
ACCENT_COLOR = "#3498db"
SUCCESS_COLOR = "#27ae60"
ERROR_COLOR = "#e74c3c"

PAYMENT_METHODS = ["现金", "银行卡", "支付宝", "微信", "其他"]

EXPENSE_DEFAULT_CATEGORIES = ["餐饮", "交通", "购物", "娱乐", "医疗", "教育", "住房", "其他"]
INCOME_DEFAULT_CATEGORIES = ["工资", "奖金", "投资收益", "兼职", "其他"]
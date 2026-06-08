
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.webp']

POSITION_MAP = {
    '左上': (0, 0),
    '中上': (0.5, 0),
    '右上': (1, 0),
    '左中': (0, 0.5),
    '正中间': (0.5, 0.5),
    '右中': (1, 0.5),
    '左下': (0, 1),
    '中下': (0.5, 1),
    '右下': (1, 1)
}

DEFAULT_SETTINGS = {
    'text': '水印',
    'font_size': 40,
    'color': '#FFFFFF',
    'opacity': 0.5,
    'rotation': 0,
    'position': '右下',
    'margin': 20,
    'image_scale': 0.2,
    'output_format': '保持原格式',
    'jpg_quality': 90,
    'filename_rule': '原文件名_watermarked',
    'custom_prefix': 'wm_'
}

COLOR_PRESETS = [
    ('白色', '#FFFFFF'),
    ('黑色', '#000000'),
    ('红色', '#FF0000'),
    ('蓝色', '#0000FF'),
    ('绿色', '#00FF00')
]

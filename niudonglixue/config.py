import customtkinter as ctk

APP_TITLE = "牛顿力学科普小游戏"
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700

LIGHT_THEME = "light"
DARK_THEME = "dark"

GRAVITY = 9.8
TIME_STEP = 0.016

LEVELS = [
    {"id": 1, "name": "重力实验", "knowledge": "重力", "description": "物体由于地球吸引而受到的力"},
    {"id": 2, "name": "摩擦力实验", "knowledge": "摩擦力", "description": "阻碍物体相对运动的力"},
    {"id": 3, "name": "斜面实验", "knowledge": "斜面原理", "description": "斜面可以省力"},
    {"id": 4, "name": "杠杆实验", "knowledge": "杠杆原理", "description": "杠杆平衡条件"},
    {"id": 5, "name": "弹力实验", "knowledge": "弹力", "description": "物体发生形变时产生的力"},
    {"id": 6, "name": "惯性实验", "knowledge": "惯性", "description": "物体保持原有运动状态的性质"}
]

COLORS = {
    "light": {
        "bg": "#f0f8ff",
        "canvas_bg": "#ffffff",
        "button": "#4a90d9",
        "button_hover": "#357abd",
        "text": "#333333",
        "accent": "#5cb85c",
        "warning": "#f0ad4e",
        "danger": "#d9534f"
    },
    "dark": {
        "bg": "#2c3e50",
        "canvas_bg": "#34495e",
        "button": "#3498db",
        "button_hover": "#2980b9",
        "text": "#ecf0f1",
        "accent": "#2ecc71",
        "warning": "#f39c12",
        "danger": "#e74c3c"
    }
}

QUESTIONS = {
    1: [
        {"question": "物体从高处下落时，速度会怎样变化？", "options": ["越来越慢", "保持不变", "越来越快"], "answer": 2, "hint": "想想苹果从树上掉下来的样子"},
        {"question": "如果没有重力，我们会怎么样？", "options": ["站得更稳", "飘在空中", "跑得更快"], "answer": 1, "hint": "就像在太空中一样"}
    ],
    2: [
        {"question": "在粗糙的地面上滑行，物体会：", "options": ["滑得更远", "很快停下", "速度不变"], "answer": 1, "hint": "摩擦力会阻碍运动"},
        {"question": "冰面很光滑，摩擦力：", "options": ["很大", "很小", "不变"], "answer": 1, "hint": "光滑的表面摩擦力小"}
    ],
    3: [
        {"question": "斜面角度越小，物体下滑：", "options": ["越快", "越慢", "不变"], "answer": 1, "hint": "角度小更平缓"},
        {"question": "斜面可以帮我们：", "options": ["省力", "省距离", "省时间"], "answer": 0, "hint": "搬东西上斜坡更轻松"}
    ],
    4: [
        {"question": "杠杆支点靠近重物时：", "options": ["更费力", "更省力", "一样"], "answer": 1, "hint": "阿基米德说过给我支点"},
        {"question": "杠杆平衡需要两边：", "options": ["重量相等", "力乘以距离相等", "距离相等"], "answer": 1, "hint": "力和距离的乘积"}
    ],
    5: [
        {"question": "弹簧被压缩后会：", "options": ["保持压缩", "弹回去", "消失"], "answer": 1, "hint": "弹力会试图恢复原状"},
        {"question": "弹簧拉得越长，弹力：", "options": ["越小", "越大", "不变"], "answer": 1, "hint": "形变越大弹力越大"}
    ],
    6: [
        {"question": "快速抽走书本，上面的鸡蛋会：", "options": ["跟着走", "原地落下", "飞走"], "answer": 1, "hint": "鸡蛋想保持原来的静止状态"},
        {"question": "汽车突然刹车，乘客会：", "options": ["向后倒", "向前倾", "不动"], "answer": 1, "hint": "身体想继续向前运动"}
    ]
}

KNOWLEDGE_EXPLANATIONS = {
    1: "重力是地球对物体的吸引力。所有物体都受到重力的作用，所以我们站在地面上不会飘起来。物体下落时，重力会让它的速度越来越快。",
    2: "摩擦力是两个物体接触时产生的阻碍力。粗糙的表面摩擦力大，光滑的表面摩擦力小。摩擦力可以帮助我们走路、刹车，但也会阻碍物体运动。",
    3: "斜面是一种简单机械。斜面越平缓（角度越小），就越省力，但需要走更长的距离。盘山公路就是利用了斜面原理。",
    4: "杠杆原理：动力×动力臂 = 阻力×阻力臂。支点靠近重物时更省力，靠近动力端时更费力。跷跷板就是一个杠杆。",
    5: "弹力是物体发生形变时产生的恢复力。弹簧被拉伸或压缩后，会产生弹力试图恢复原来的形状。弹力的大小和形变量成正比。",
    6: "惯性是物体保持原有运动状态的性质。静止的物体想保持静止，运动的物体想保持运动。乘车时刹车身体前倾就是惯性的表现。"
}
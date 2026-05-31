import pygame
import math
import config

def draw_circle(surface, color, center, size):
    """绘制圆形"""
    radius = size // 2
    pygame.draw.circle(surface, color, center, radius, 3)
    pygame.draw.circle(surface, color, center, radius // 3, 0)

def draw_triangle(surface, color, center, size):
    """绘制等边三角形"""
    points = []
    for i in range(3):
        angle = math.radians(90 + i * 120)
        x = center[0] + size // 2 * math.cos(angle)
        y = center[1] - size // 2 * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points, 3)
    inner_points = []
    for i in range(3):
        angle = math.radians(90 + i * 120)
        x = center[0] + size // 4 * math.cos(angle)
        y = center[1] - size // 4 * math.sin(angle)
        inner_points.append((x, y))
    pygame.draw.polygon(surface, color, inner_points, 0)

def draw_square(surface, color, center, size):
    """绘制正方形"""
    half_size = size // 2
    rect = pygame.Rect(center[0] - half_size, center[1] - half_size, size, size)
    pygame.draw.rect(surface, color, rect, 3)
    inner_rect = pygame.Rect(center[0] - half_size // 2, center[1] - half_size // 2, size // 2, size // 2)
    pygame.draw.rect(surface, color, inner_rect, 0)

def draw_cross(surface, color, center, size):
    """绘制十字形"""
    thickness = 3
    arm_length = size // 2
    arm_width = size // 6
    pygame.draw.line(surface, color, (center[0] - arm_length, center[1]), (center[0] + arm_length, center[1]), thickness)
    pygame.draw.line(surface, color, (center[0], center[1] - arm_length), (center[0], center[1] + arm_length), thickness)
    pygame.draw.circle(surface, color, center, arm_width // 2, 0)

def draw_pentagon(surface, color, center, size):
    """绘制五边形"""
    points = []
    for i in range(5):
        angle = math.radians(90 + i * 72)
        x = center[0] + size // 2 * math.cos(angle)
        y = center[1] - size // 2 * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points, 3)
    inner_points = []
    for i in range(5):
        angle = math.radians(90 + i * 72)
        x = center[0] + size // 4 * math.cos(angle)
        y = center[1] - size // 4 * math.sin(angle)
        inner_points.append((x, y))
    pygame.draw.polygon(surface, color, inner_points, 0)

def draw_diamond(surface, color, center, size):
    """绘制菱形"""
    points = [
        (center[0], center[1] - size // 2),
        (center[0] + size // 2, center[1]),
        (center[0], center[1] + size // 2),
        (center[0] - size // 2, center[1])
    ]
    pygame.draw.polygon(surface, color, points, 3)
    inner_size = size // 3
    inner_points = [
        (center[0], center[1] - inner_size // 2),
        (center[0] + inner_size // 2, center[1]),
        (center[0], center[1] + inner_size // 2),
        (center[0] - inner_size // 2, center[1])
    ]
    pygame.draw.polygon(surface, color, inner_points, 0)

def draw_shape(surface, shape_type, color, center, size=60):
    """根据形状类型绘制对应的图形"""
    shape_functions = {
        'circle': draw_circle,
        'triangle': draw_triangle,
        'square': draw_square,
        'cross': draw_cross,
        'pentagon': draw_pentagon,
        'diamond': draw_diamond
    }
    
    draw_func = shape_functions.get(shape_type)
    if draw_func:
        draw_func(surface, color, center, size)

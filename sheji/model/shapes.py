import pygame
import math

class Shape:
    def __init__(self, x, y, color, size):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.selected = False
        self.rotation = 0
        self.scale = 1.0
    
    def draw(self, screen):
        pass
    
    def contains(self, pos):
        pass
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def draw_selection(self, screen):
        if not self.selected:
            return
        
        bounding_box = self.get_bounding_box()
        
        # 绘制高亮边框
        pygame.draw.rect(screen, (255, 255, 0), bounding_box, 3, border_radius=3)
        
        # 绘制控制点
        control_points = self.get_control_points()
        for point in control_points:
            pygame.draw.circle(screen, (255, 255, 255), point, 6)
            pygame.draw.circle(screen, (255, 200, 0), point, 4)
            pygame.draw.circle(screen, (255, 255, 255), point, 2)
    
    def rotate_point(self, point, center, angle):
        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        dx = point[0] - center[0]
        dy = point[1] - center[1]
        new_x = center[0] + dx * cos_a - dy * sin_a
        new_y = center[1] + dx * sin_a + dy * cos_a
        return (new_x, new_y)
    
    def rotate_points(self, points, center, angle):
        return [self.rotate_point(p, center, angle) for p in points]
    
    def get_bounding_box(self):
        return (self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
    
    def get_control_points(self):
        bb = self.get_bounding_box()
        x, y, w, h = bb
        return [
            (x, y),
            (x + w//2, y),
            (x + w, y),
            (x + w, y + h//2),
            (x + w, y + h),
            (x + w//2, y + h),
            (x, y + h),
            (x, y + h//2)
        ]

class Circle(Shape):
    def __init__(self, x, y, color, size):
        super().__init__(x, y, color, size)
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), int(self.size * self.scale))
        if self.selected:
            self.draw_selection(screen)
    
    def contains(self, pos):
        distance = ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) ** 0.5
        return distance <= self.size * self.scale
    
    def get_bounding_box(self):
        scaled_size = self.size * self.scale
        return (self.x - scaled_size, self.y - scaled_size, scaled_size * 2, scaled_size * 2)
    
    def get_control_points(self):
        scaled_size = self.size * self.scale
        return [
            (self.x - scaled_size, self.y - scaled_size),
            (self.x, self.y - scaled_size),
            (self.x + scaled_size, self.y - scaled_size),
            (self.x + scaled_size, self.y),
            (self.x + scaled_size, self.y + scaled_size),
            (self.x, self.y + scaled_size),
            (self.x - scaled_size, self.y + scaled_size),
            (self.x - scaled_size, self.y)
        ]

class Rectangle(Shape):
    def __init__(self, x, y, color, size):
        super().__init__(x, y, color, size)
    
    def draw(self, screen):
        scaled_size = self.size * self.scale
        rect = pygame.Rect(self.x - scaled_size, self.y - scaled_size, scaled_size * 2, scaled_size * 2)
        pygame.draw.rect(screen, self.color, rect)
        if self.selected:
            self.draw_selection(screen)
    
    def contains(self, pos):
        scaled_size = self.size * self.scale
        return (self.x - scaled_size <= pos[0] <= self.x + scaled_size and
                self.y - scaled_size <= pos[1] <= self.y + scaled_size)
    
    def get_bounding_box(self):
        scaled_size = self.size * self.scale
        return (self.x - scaled_size, self.y - scaled_size, scaled_size * 2, scaled_size * 2)
    
    def get_control_points(self):
        scaled_size = self.size * self.scale
        return [
            (self.x - scaled_size, self.y - scaled_size),
            (self.x, self.y - scaled_size),
            (self.x + scaled_size, self.y - scaled_size),
            (self.x + scaled_size, self.y),
            (self.x + scaled_size, self.y + scaled_size),
            (self.x, self.y + scaled_size),
            (self.x - scaled_size, self.y + scaled_size),
            (self.x - scaled_size, self.y)
        ]

class Triangle(Shape):
    def __init__(self, x, y, color, size):
        super().__init__(x, y, color, size)
    
    def draw(self, screen):
        scaled_size = self.size * self.scale
        points = [
            (self.x, self.y - scaled_size),
            (self.x - scaled_size, self.y + scaled_size),
            (self.x + scaled_size, self.y + scaled_size)
        ]
        if self.rotation != 0:
            points = self.rotate_points(points, (self.x, self.y), self.rotation)
        pygame.draw.polygon(screen, self.color, points)
        if self.selected:
            self.draw_selection(screen)
    
    def contains(self, pos):
        px, py = pos
        scaled_size = self.size * self.scale
        ax, ay = self.x, self.y - scaled_size
        bx, by = self.x - scaled_size, self.y + scaled_size
        cx, cy = self.x + scaled_size, self.y + scaled_size
        
        if self.rotation != 0:
            ax, ay = self.rotate_point((ax, ay), (self.x, self.y), self.rotation)
            bx, by = self.rotate_point((bx, by), (self.x, self.y), self.rotation)
            cx, cy = self.rotate_point((cx, cy), (self.x, self.y), self.rotation)
        
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        d1 = sign((px, py), (ax, ay), (bx, by))
        d2 = sign((px, py), (bx, by), (cx, cy))
        d3 = sign((px, py), (cx, cy), (ax, ay))
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        return not (has_neg and has_pos)
    
    def get_bounding_box(self):
        scaled_size = self.size * self.scale
        return (self.x - scaled_size, self.y - scaled_size, scaled_size * 2, scaled_size * 2)
    
    def get_control_points(self):
        scaled_size = self.size * self.scale
        points = [
            (self.x - scaled_size, self.y - scaled_size),
            (self.x, self.y - scaled_size),
            (self.x + scaled_size, self.y - scaled_size),
            (self.x + scaled_size, self.y),
            (self.x + scaled_size, self.y + scaled_size),
            (self.x, self.y + scaled_size),
            (self.x - scaled_size, self.y + scaled_size),
            (self.x - scaled_size, self.y)
        ]
        if self.rotation != 0:
            points = self.rotate_points(points, (self.x, self.y), self.rotation)
        return points

class Diamond(Shape):
    def __init__(self, x, y, color, size):
        super().__init__(x, y, color, size)
    
    def draw(self, screen):
        scaled_size = self.size * self.scale
        points = [
            (self.x, self.y - scaled_size),
            (self.x + scaled_size, self.y),
            (self.x, self.y + scaled_size),
            (self.x - scaled_size, self.y)
        ]
        if self.rotation != 0:
            points = self.rotate_points(points, (self.x, self.y), self.rotation)
        pygame.draw.polygon(screen, self.color, points)
        if self.selected:
            self.draw_selection(screen)
    
    def contains(self, pos):
        px, py = pos
        scaled_size = self.size * self.scale
        return (abs(px - self.x) + abs(py - self.y)) <= scaled_size
    
    def get_bounding_box(self):
        scaled_size = self.size * self.scale
        return (self.x - scaled_size, self.y - scaled_size, scaled_size * 2, scaled_size * 2)
    
    def get_control_points(self):
        scaled_size = self.size * self.scale
        points = [
            (self.x - scaled_size, self.y - scaled_size),
            (self.x, self.y - scaled_size),
            (self.x + scaled_size, self.y - scaled_size),
            (self.x + scaled_size, self.y),
            (self.x + scaled_size, self.y + scaled_size),
            (self.x, self.y + scaled_size),
            (self.x - scaled_size, self.y + scaled_size),
            (self.x - scaled_size, self.y)
        ]
        if self.rotation != 0:
            points = self.rotate_points(points, (self.x, self.y), self.rotation)
        return points

class Star(Shape):
    def __init__(self, x, y, color, size):
        super().__init__(x, y, color, size)
    
    def draw(self, screen):
        import math
        scaled_size = self.size * self.scale
        points = []
        for i in range(5):
            angle = math.pi / 2 + (2 * math.pi * i) / 5
            outer_x = self.x + scaled_size * math.cos(angle)
            outer_y = self.y - scaled_size * math.sin(angle)
            points.append((outer_x, outer_y))
            
            inner_angle = angle + math.pi / 5
            inner_x = self.x + (scaled_size / 2) * math.cos(inner_angle)
            inner_y = self.y - (scaled_size / 2) * math.sin(inner_angle)
            points.append((inner_x, inner_y))
        
        if self.rotation != 0:
            points = self.rotate_points(points, (self.x, self.y), self.rotation)
        
        pygame.draw.polygon(screen, self.color, points)
        if self.selected:
            self.draw_selection(screen)
    
    def contains(self, pos):
        distance = ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) ** 0.5
        return distance <= self.size * self.scale
    
    def get_bounding_box(self):
        scaled_size = self.size * self.scale
        return (self.x - scaled_size, self.y - scaled_size, scaled_size * 2, scaled_size * 2)
    
    def get_control_points(self):
        scaled_size = self.size * self.scale
        points = [
            (self.x - scaled_size, self.y - scaled_size),
            (self.x, self.y - scaled_size),
            (self.x + scaled_size, self.y - scaled_size),
            (self.x + scaled_size, self.y),
            (self.x + scaled_size, self.y + scaled_size),
            (self.x, self.y + scaled_size),
            (self.x - scaled_size, self.y + scaled_size),
            (self.x - scaled_size, self.y)
        ]
        if self.rotation != 0:
            points = self.rotate_points(points, (self.x, self.y), self.rotation)
        return points
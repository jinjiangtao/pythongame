import pygame

class Shape:
    def __init__(self, x, y, color, size):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.selected = False
    
    def draw(self, screen):
        pass
    
    def contains(self, pos):
        pass
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Circle(Shape):
    def __init__(self, x, y, color, size):
        super().__init__(x, y, color, size)
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        if self.selected:
            pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.size + 3, 2)
    
    def contains(self, pos):
        distance = ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) ** 0.5
        return distance <= self.size

class Rectangle(Shape):
    def __init__(self, x, y, color, size):
        super().__init__(x, y, color, size)
    
    def draw(self, screen):
        rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
        pygame.draw.rect(screen, self.color, rect)
        if self.selected:
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
    
    def contains(self, pos):
        return (self.x - self.size <= pos[0] <= self.x + self.size and
                self.y - self.size <= pos[1] <= self.y + self.size)

class Triangle(Shape):
    def __init__(self, x, y, color, size):
        super().__init__(x, y, color, size)
    
    def draw(self, screen):
        points = [
            (self.x, self.y - self.size),
            (self.x - self.size, self.y + self.size),
            (self.x + self.size, self.y + self.size)
        ]
        pygame.draw.polygon(screen, self.color, points)
        if self.selected:
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)
    
    def contains(self, pos):
        px, py = pos
        ax, ay = self.x, self.y - self.size
        bx, by = self.x - self.size, self.y + self.size
        cx, cy = self.x + self.size, self.y + self.size
        
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        d1 = sign((px, py), (ax, ay), (bx, by))
        d2 = sign((px, py), (bx, by), (cx, cy))
        d3 = sign((px, py), (cx, cy), (ax, ay))
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        return not (has_neg and has_pos)

class Diamond(Shape):
    def __init__(self, x, y, color, size):
        super().__init__(x, y, color, size)
    
    def draw(self, screen):
        points = [
            (self.x, self.y - self.size),
            (self.x + self.size, self.y),
            (self.x, self.y + self.size),
            (self.x - self.size, self.y)
        ]
        pygame.draw.polygon(screen, self.color, points)
        if self.selected:
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)
    
    def contains(self, pos):
        px, py = pos
        return (abs(px - self.x) + abs(py - self.y)) <= self.size

class Star(Shape):
    def __init__(self, x, y, color, size):
        super().__init__(x, y, color, size)
    
    def draw(self, screen):
        import math
        points = []
        for i in range(5):
            angle = math.pi / 2 + (2 * math.pi * i) / 5
            outer_x = self.x + self.size * math.cos(angle)
            outer_y = self.y - self.size * math.sin(angle)
            points.append((outer_x, outer_y))
            
            inner_angle = angle + math.pi / 5
            inner_x = self.x + (self.size / 2) * math.cos(inner_angle)
            inner_y = self.y - (self.size / 2) * math.sin(inner_angle)
            points.append((inner_x, inner_y))
        
        pygame.draw.polygon(screen, self.color, points)
        if self.selected:
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)
    
    def contains(self, pos):
        px, py = pos
        distance = ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) ** 0.5
        return distance <= self.size
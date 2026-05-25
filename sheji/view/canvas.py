import pygame

class Canvas:
    def __init__(self, screen, toolbar_width=150):
        self.screen = screen
        self.toolbar_width = toolbar_width
        self.width = screen.get_width() - toolbar_width
        self.height = screen.get_height() - 50
        self.x = toolbar_width
        self.y = 50
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bg_color = (255, 255, 255)
        self.grid_color = (230, 230, 230)
        self.grid_size = 20
    
    def draw(self, shapes):
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        
        for x in range(self.x, self.x + self.width, self.grid_size):
            pygame.draw.line(self.screen, self.grid_color, (x, self.y), (x, self.y + self.height))
        for y in range(self.y, self.y + self.height, self.grid_size):
            pygame.draw.line(self.screen, self.grid_color, (self.x, y), (self.x + self.width, y))
        
        for shape in shapes:
            shape.draw(self.screen)
    
    def is_inside(self, pos):
        return self.rect.collidepoint(pos)
    
    def to_canvas_coords(self, pos):
        return (pos[0] - self.x, pos[1] - self.y)
    
    def get_screen_coords(self, canvas_pos):
        return (canvas_pos[0] + self.x, canvas_pos[1] + self.y)
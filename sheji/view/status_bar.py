import pygame

class StatusBar:
    def __init__(self, screen):
        self.screen = screen
        self.height = 50
        self.width = screen.get_width()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.bg_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        
        try:
            self.font = pygame.font.Font('simhei.ttf', 16)
        except:
            self.font = pygame.font.Font(None, 16)
        
        self.shape_names = {
            'circle': '圆形',
            'rectangle': '矩形',
            'triangle': '三角形',
            'diamond': '四边形',
            'star': '星形'
        }
    
    def draw(self, current_shape_type, status_message):
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        
        shape_label = self.font.render(f'当前素材: {self.shape_names.get(current_shape_type, current_shape_type)}', 
                                      True, self.text_color)
        self.screen.blit(shape_label, (160, 15))
        
        message_surface = self.font.render(status_message, True, (150, 200, 255))
        self.screen.blit(message_surface, (400, 15))
        
        pygame.draw.line(self.screen, (80, 80, 80), (0, self.height - 1), (self.width, self.height - 1))
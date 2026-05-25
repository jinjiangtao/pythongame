import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model.canvas_model import CanvasModel
from view.toolbar import Toolbar
from view.canvas import Canvas
from view.status_bar import StatusBar
from controller.event_handler import EventHandler

class App:
    def __init__(self):
        pygame.init()
        
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 700
        
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('创意设计搭建小游戏')
        
        self.center_window()
        
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        self.model = CanvasModel()
        self.toolbar = Toolbar(self.screen)
        self.canvas = Canvas(self.screen)
        self.status_bar = StatusBar(self.screen)
        self.event_handler = EventHandler(self.model, self.toolbar, self.canvas, self.status_bar)
    
    def center_window(self):
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        
        x = (screen_width - self.WINDOW_WIDTH) // 2
        y = (screen_height - self.WINDOW_HEIGHT) // 2
        
        os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if not self.event_handler.handle_event(event):
                    running = False
            
            self.screen.fill((30, 30, 30))
            
            self.status_bar.draw(self.model.current_shape_type, self.model.status_message)
            self.toolbar.draw(self.model.current_shape_type, self.model.current_color, self.model.current_size)
            self.canvas.draw(self.model.shapes)
            
            pygame.display.flip()
            self.clock.tick(self.FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    app = App()
    app.run()
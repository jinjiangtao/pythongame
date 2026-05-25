import pygame
import os

class EventHandler:
    def __init__(self, model, toolbar, canvas, status_bar):
        self.model = model
        self.toolbar = toolbar
        self.canvas = canvas
        self.status_bar = status_bar
        self.dragging = False
        self.drag_offset = (0, 0)
        self.last_mouse_pos = (0, 0)
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(event)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(event)
        
        elif event.type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(event)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                self.model.remove_selected()
            elif event.key == pygame.K_ESCAPE:
                self.model.deselect_all()
        
        return True
    
    def handle_mouse_down(self, event):
        if event.button == 1:
            pos = pygame.mouse.get_pos()
            
            toolbar_result = self.toolbar.handle_click(pos, self.model.current_shape_type)
            if toolbar_result[0] == 'shape':
                self.model.update_current_shape_type(toolbar_result[1])
            elif toolbar_result[0] == 'color':
                if self.model.selected_shape:
                    self.model.update_selected_color(toolbar_result[1])
                self.model.update_current_color(toolbar_result[1])
            elif toolbar_result[0] == 'size':
                if self.model.selected_shape:
                    self.model.update_selected_size(toolbar_result[1])
                self.model.update_current_size(toolbar_result[1])
            elif toolbar_result[0] == 'rotate':
                self.model.update_current_rotation(toolbar_result[1])
            elif toolbar_result[0] == 'scale':
                self.model.update_current_scale(toolbar_result[1])
            elif toolbar_result[0] == 'action':
                self.handle_action(toolbar_result[1])
            elif self.canvas.is_inside(pos):
                if self.model.select_shape_at(pos):
                    self.dragging = True
                    self.last_mouse_pos = pos
                else:
                    self.model.add_shape(pos[0], pos[1])
                    self.model.status_message = f'已添加图形'
    
    def handle_mouse_up(self, event):
        if event.button == 1:
            self.dragging = False
    
    def handle_mouse_motion(self, event):
        if self.dragging and self.model.selected_shape:
            current_pos = pygame.mouse.get_pos()
            dx = current_pos[0] - self.last_mouse_pos[0]
            dy = current_pos[1] - self.last_mouse_pos[1]
            self.model.move_selected(dx, dy)
            self.last_mouse_pos = current_pos
    
    def handle_action(self, action):
        if action == 'delete':
            self.model.remove_selected()
        elif action == 'clear':
            self.model.clear_all()
        elif action == 'save':
            self.save_canvas()
        elif action == 'custom_color':
            self.open_color_picker()
    
    def save_canvas(self):
        canvas_surface = pygame.Surface((self.canvas.width, self.canvas.height))
        canvas_surface.fill((255, 255, 255))
        
        grid_color = (230, 230, 230)
        grid_size = 20
        for x in range(0, self.canvas.width, grid_size):
            pygame.draw.line(canvas_surface, grid_color, (x, 0), (x, self.canvas.height))
        for y in range(0, self.canvas.height, grid_size):
            pygame.draw.line(canvas_surface, grid_color, (0, y), (self.canvas.width, y))
        
        for shape in self.model.shapes:
            shape.draw(canvas_surface)
        
        if not os.path.exists('saved'):
            os.makedirs('saved')
        
        import time
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        filename = f'saved/drawing_{timestamp}.png'
        pygame.image.save(canvas_surface, filename)
        self.model.status_message = f'作品已保存为 {filename}'
    
    def open_color_picker(self):
        try:
            import tkinter as tk
            from tkinter import colorchooser
            
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            color = colorchooser.askcolor(title="选择颜色", initialcolor=(255, 0, 0))
            
            root.destroy()
            
            if color[1]:
                rgb_color = tuple(int(color[0][i]) for i in range(3))
                if self.model.selected_shape:
                    self.model.update_selected_color(rgb_color)
                self.model.update_current_color(rgb_color)
                self.model.status_message = f'已选择自定义颜色 {rgb_color}'
        except Exception as e:
            self.model.status_message = f'颜色选择器打开失败: {str(e)}'
from .shapes import Circle, Rectangle, Triangle, Diamond, Star

class CanvasModel:
    def __init__(self):
        self.shapes = []
        self.selected_shape = None
        self.current_shape_type = 'circle'
        self.current_color = (255, 0, 0)
        self.current_size = 30
        self.current_rotation = 0
        self.current_scale = 1.0
        self.status_message = '欢迎使用创意设计工具！选择左侧素材开始创作。'
    
    def add_shape(self, x, y):
        shape_classes = {
            'circle': Circle,
            'rectangle': Rectangle,
            'triangle': Triangle,
            'diamond': Diamond,
            'star': Star
        }
        shape_class = shape_classes.get(self.current_shape_type)
        if shape_class:
            shape = shape_class(x, y, self.current_color, self.current_size)
            self.shapes.append(shape)
            self.status_message = f'已添加 {self.current_shape_type} 图形'
    
    def remove_selected(self):
        if self.selected_shape:
            self.shapes.remove(self.selected_shape)
            self.selected_shape = None
            self.status_message = '已删除选中图形'
    
    def clear_all(self):
        self.shapes.clear()
        self.selected_shape = None
        self.status_message = '画布已清空'
    
    def select_shape_at(self, pos):
        self.selected_shape = None
        for shape in reversed(self.shapes):
            if shape.contains(pos):
                shape.selected = True
                self.selected_shape = shape
                self.status_message = '已选中图形，可拖动或修改属性'
                return True
        self.status_message = '未选中任何图形'
        return False
    
    def deselect_all(self):
        if self.selected_shape:
            self.selected_shape.selected = False
            self.selected_shape = None
            self.status_message = '已取消选中'
    
    def move_selected(self, dx, dy):
        if self.selected_shape:
            self.selected_shape.move(dx, dy)
    
    def update_selected_color(self, color):
        if self.selected_shape:
            self.selected_shape.color = color
            self.status_message = '颜色已更新'
    
    def update_selected_size(self, size):
        if self.selected_shape:
            self.selected_shape.size = size
            self.status_message = '大小已更新'
    
    def update_current_shape_type(self, shape_type):
        self.current_shape_type = shape_type
        shape_names = {
            'circle': '圆形',
            'rectangle': '矩形',
            'triangle': '三角形',
            'diamond': '四边形',
            'star': '星形'
        }
        self.status_message = f'当前选中素材：{shape_names.get(shape_type, shape_type)}'
    
    def update_current_color(self, color):
        self.current_color = color
        self.status_message = '颜色已更改'
    
    def update_current_size(self, size):
        self.current_size = size
        self.status_message = f'大小设置为 {size}'
    
    def update_current_rotation(self, rotation):
        self.current_rotation = rotation
        if self.selected_shape:
            self.selected_shape.rotation = rotation
            self.status_message = f'旋转角度设置为 {rotation}°'
        else:
            self.status_message = f'旋转角度设置为 {rotation}°'
    
    def update_current_scale(self, scale):
        self.current_scale = scale
        if self.selected_shape:
            self.selected_shape.scale = scale
            self.status_message = f'缩放比例设置为 {int(scale * 100)}%'
        else:
            self.status_message = f'缩放比例设置为 {int(scale * 100)}%'
from PIL import Image

class HistoryManager:
    def __init__(self, max_history=20):
        self.max_history = max_history
        self.history = []
        self.current_index = -1
    
    def save_state(self, image):
        state = image.copy()
        
        self.history = self.history[:self.current_index + 1]
        self.history.append(state)
        
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.current_index -= 1
        
        self.current_index = len(self.history) - 1
    
    def undo(self, canvas):
        if self.current_index > 0:
            self.current_index -= 1
            self._restore_state(canvas)
            return True
        return False
    
    def redo(self, canvas):
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            self._restore_state(canvas)
            return True
        return False
    
    def _restore_state(self, canvas):
        if 0 <= self.current_index < len(self.history):
            saved_image = self.history[self.current_index]
            canvas.image = saved_image.copy()
            canvas.redraw()
    
    def clear(self):
        self.history = []
        self.current_index = -1
    
    def can_undo(self):
        return self.current_index > 0
    
    def can_redo(self):
        return self.current_index < len(self.history) - 1
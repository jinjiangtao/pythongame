import pygame
import random
from config import *
from characters import Pet

class GameArea:
    def __init__(self):
        self.cells = []
        self.pets = []
        self.last_spawn_time = 0
        self.spawn_interval = BASE_SPAWN_INTERVAL
        self.max_pets = 5
        self.init_cells()
    
    def init_cells(self):
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                cell_x = col * CELL_WIDTH + CELL_WIDTH // 2
                cell_y = row * CELL_HEIGHT + CELL_HEIGHT // 2 + TOP_BAR_HEIGHT
                self.cells.append((cell_x, cell_y))
    
    def update(self, current_time):
        self.pets = [pet for pet in self.pets if pet.update(current_time)]
        self.try_spawn_pet(current_time)
    
    def try_spawn_pet(self, current_time):
        if len(self.pets) >= self.max_pets:
            return
        
        if current_time - self.last_spawn_time >= self.spawn_interval:
            cell_x, cell_y = random.choice(self.cells)
            x = cell_x + (random.random() - 0.5) * (CELL_WIDTH - PET_SIZE * 2)
            y = cell_y + (random.random() - 0.5) * (CELL_HEIGHT - PET_SIZE * 2)
            x = max(PET_SIZE, min(GAME_AREA_WIDTH - PET_SIZE, x))
            y = max(TOP_BAR_HEIGHT + PET_SIZE, min(SCREEN_HEIGHT - PET_SIZE, y))
            
            new_pet = Pet(x, y)
            self.pets.append(new_pet)
            
            self.last_spawn_time = current_time
            self.spawn_interval = random.randint(MIN_SPAWN_INTERVAL, MAX_SPAWN_INTERVAL)
    
    def draw(self, screen):
        for pet in self.pets:
            pet.draw(screen)
    
    def handle_click(self, mouse_x, mouse_y):
        for pet in self.pets:
            if not pet.catched and pet.check_click(mouse_x, mouse_y):
                pet.catched = True
                return True, 10
        return False, 0
    
    def clear_pets(self):
        self.pets = []
        self.last_spawn_time = 0
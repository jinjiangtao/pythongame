import pygame
import random
from config import *
from characters import Pet, Prop


class GameArea:
    def __init__(self):
        self.cells = []
        self.pets = []
        self.props = []
        self.effects = []
        self.last_spawn_time = 0
        self.last_prop_time = 0
        self.spawn_interval = BASE_SPAWN_INTERVAL
        self.max_pets = MAX_PETS_BASE
        self.prop_interval = 8000
        self.current_level = 1
        self.catch_all_active = False
        self.catch_all_end_time = 0
        self.score_multiplier = 1
        self.init_cells()
    
    def init_cells(self):
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                cell_x = col * CELL_WIDTH + CELL_WIDTH // 2
                cell_y = row * CELL_HEIGHT + CELL_HEIGHT // 2 + TOP_BAR_HEIGHT
                self.cells.append((cell_x, cell_y))
    
    def set_level(self, level):
        self.current_level = level
        self.max_pets = min(MAX_PETS_BASE + (level - 1) * DIFFICULTY_MAX_PETS_INCREASE, MAX_PETS_MAX)
        self.spawn_interval = max(
            SPAWN_INTERVAL_MIN, 
            BASE_SPAWN_INTERVAL - (level - 1) * DIFFICULTY_SPAWN_DECREASE
        )
    
    def update(self, current_time):
        self.pets = [pet for pet in self.pets if pet.update(current_time)]
        self.props = [prop for prop in self.props if prop.update(current_time)]
        self.effects = [effect for effect in self.effects if effect.update()]
        
        if self.catch_all_active and current_time > self.catch_all_end_time:
            self.catch_all_active = False
        
        self.try_spawn_pet(current_time)
        self.try_spawn_prop(current_time)
    
    def try_spawn_pet(self, current_time):
        if len(self.pets) >= self.max_pets:
            return
        
        if current_time - self.last_spawn_time >= self.spawn_interval:
            cell_x, cell_y = random.choice(self.cells)
            x = cell_x + (random.random() - 0.5) * (CELL_WIDTH - PET_SIZE * 2)
            y = cell_y + (random.random() - 0.5) * (CELL_HEIGHT - PET_SIZE * 2)
            x = max(PET_SIZE, min(GAME_AREA_WIDTH - PET_SIZE, x))
            y = max(TOP_BAR_HEIGHT + PET_SIZE, min(SCREEN_HEIGHT - PET_SIZE, y))
            
            special_type = self.determine_special_type()
            
            new_pet = Pet(x, y, special_type, self.current_level)
            self.pets.append(new_pet)
            
            self.last_spawn_time = current_time
            interval_range = max(SPAWN_INTERVAL_MIN, self.spawn_interval - 200)
            self.spawn_interval = random.randint(interval_range, self.spawn_interval + 200)
    
    def determine_special_type(self):
        rand = random.random()
        if rand < SPECIAL_PET_CHANCE:
            type_rand = random.random()
            if type_rand < 0.33:
                return 'flash'
            elif type_rand < 0.66:
                return 'accel'
            else:
                return 'trick'
        return None
    
    def try_spawn_prop(self, current_time):
        if len(self.props) >= 2:
            return
        
        if current_time - self.last_prop_time >= self.prop_interval:
            if random.random() < PROP_CHANCE:
                cell_x, cell_y = random.choice(self.cells)
                x = cell_x + (random.random() - 0.5) * (CELL_WIDTH - PET_SIZE * 2)
                y = cell_y + (random.random() - 0.5) * (CELL_HEIGHT - PET_SIZE * 2)
                x = max(PET_SIZE, min(GAME_AREA_WIDTH - PET_SIZE, x))
                y = max(TOP_BAR_HEIGHT + PET_SIZE, min(SCREEN_HEIGHT - PET_SIZE, y))
                
                prop_types = ['time', 'catch_all', 'score']
                prop_type = random.choice(prop_types)
                
                new_prop = Prop(x, y, prop_type)
                self.props.append(new_prop)
                
                self.last_prop_time = current_time
                self.prop_interval = random.randint(6000, 10000)
    
    def draw(self, screen):
        for pet in self.pets:
            pet.draw(screen)
        
        for prop in self.props:
            prop.draw(screen)
        
        for effect in self.effects:
            effect.draw(screen)
    
    def handle_click(self, mouse_x, mouse_y, score_timer):
        result = {'success': False, 'points': 0, 'special_type': None, 'prop_type': None}
        
        if self.catch_all_active:
            caught_any = False
            for pet in self.pets:
                if not pet.catched and pet.check_click(mouse_x, mouse_y):
                    pet.catched = True
                    caught_any = True
            
            if caught_any:
                total_points = sum(
                    pet.points * self.score_multiplier 
                    for pet in self.pets 
                    if pet.catched and not hasattr(pet, '_counted')
                )
                for pet in self.pets:
                    if pet.catched and not hasattr(pet, '_counted'):
                        pet._counted = True
                
                self.effects.append(Effect(mouse_x, mouse_y, 'success'))
                result['success'] = True
                result['points'] = total_points
                return result
            else:
                self.effects.append(Effect(mouse_x, mouse_y, 'failure'))
                score_timer.break_combo()
                return result
        
        for prop in self.props:
            if not prop.catched and prop.check_click(mouse_x, mouse_y):
                prop.catched = True
                result['prop_type'] = prop.prop_type
                result['success'] = True
                
                if prop.prop_type == 'time':
                    result['time_bonus'] = PROP_TIME_BONUS
                elif prop.prop_type == 'catch_all':
                    self.catch_all_active = True
                    self.catch_all_end_time = pygame.time.get_ticks() + PROP_CATCH_ALL_DURATION * 1000
                elif prop.prop_type == 'score':
                    self.score_multiplier = PROP_SCORE_MULTIPLIER
                
                self.effects.append(Effect(mouse_x, mouse_y, 'success'))
                return result
        
        for pet in self.pets:
            if not pet.catched and pet.check_click(mouse_x, mouse_y):
                pet.catched = True
                points = pet.points * self.score_multiplier
                result['success'] = True
                result['points'] = points
                result['special_type'] = pet.special_type
                self.effects.append(Effect(mouse_x, mouse_y, 'success'))
                return result
        
        self.effects.append(Effect(mouse_x, mouse_y, 'failure'))
        score_timer.break_combo()
        return result
    
    def clear_pets(self):
        self.pets = []
        self.props = []
        self.effects = []
        self.last_spawn_time = 0
        self.last_prop_time = 0
        self.catch_all_active = False
        self.score_multiplier = 1

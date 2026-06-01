
from constants import *


class GameMap:
    def __init__(self):
        self.map_data = self.create_classic_map()
        self.dots_remaining = self.count_dots()

    def create_classic_map(self):
        return [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 3, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 3, 0],
            [0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0],
            [0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0],
            [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
            [0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0],
            [0, 2, 2, 2, 2, 0, 2, 2, 2, 0, 0, 2, 2, 2, 0, 2, 2, 2, 2, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0],
            [1, 1, 1, 0, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 0, 1, 1, 1],
            [0, 0, 0, 0, 2, 0, 1, 0, 0, 4, 4, 0, 0, 1, 0, 2, 0, 0, 0, 0],
            [1, 1, 1, 1, 2, 1, 1, 0, 4, 4, 4, 4, 0, 1, 1, 2, 1, 1, 1, 1],
            [0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0],
            [1, 1, 1, 0, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 0, 1, 1, 1],
            [0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
            [0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0],
            [0, 3, 2, 0, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 0, 2, 3, 0],
            [0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 0],
            [0, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def count_dots(self):
        count = 0
        for row in self.map_data:
            for cell in row:
                if cell == MAP_DOT or cell == MAP_POWER_PELLET:
                    count += 1
        return count

    def is_wall(self, x, y):
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            return True
        return self.map_data[y][x] == MAP_WALL

    def can_move_to(self, x, y):
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            return False
        return self.map_data[y][x] != MAP_WALL

    def eat_dot(self, x, y):
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
            cell = self.map_data[y][x]
            if cell == MAP_DOT:
                self.map_data[y][x] = MAP_EMPTY
                self.dots_remaining -= 1
                return MAP_DOT
            elif cell == MAP_POWER_PELLET:
                self.map_data[y][x] = MAP_EMPTY
                self.dots_remaining -= 1
                return MAP_POWER_PELLET
        return None

    def reset(self):
        self.map_data = self.create_classic_map()
        self.dots_remaining = self.count_dots()

    def draw(self, surface):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                cell = self.map_data[y][x]
                rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if cell == MAP_WALL:
                    import pygame
                    pygame.draw.rect(surface, BLUE, rect, 2)
                elif cell == MAP_DOT:
                    center_x = x * CELL_SIZE + CELL_SIZE // 2
                    center_y = y * CELL_SIZE + CELL_SIZE // 2
                    import pygame
                    pygame.draw.circle(surface, WHITE, (center_x, center_y), 4)
                elif cell == MAP_POWER_PELLET:
                    center_x = x * CELL_SIZE + CELL_SIZE // 2
                    center_y = y * CELL_SIZE + CELL_SIZE // 2
                    import pygame
                    pygame.draw.circle(surface, WHITE, (center_x, center_y), 10)

    def get_pacman_start(self):
        return (10, 14)

    def get_ghost_starts(self):
        return [(9, 8), (10, 8), (9, 9), (10, 9)]

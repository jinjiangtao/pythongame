
import pygame
import math
import random
from collections import deque
from constants import *


class Ghost:
    def __init__(self, ghost_type, start_pos):
        self.ghost_type = ghost_type
        self.start_grid_x, self.start_grid_y = start_pos
        self.reset()
        self.colors = [RED, PINK, CYAN, ORANGE]

    def reset(self):
        self.grid_x = self.start_grid_x
        self.grid_y = self.start_grid_y
        self.x = self.grid_x * CELL_SIZE + CELL_SIZE // 2
        self.y = self.grid_y * CELL_SIZE + CELL_SIZE // 2
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.vulnerable = False
        self.vulnerable_timer = 0
        self.eaten = False
        self.speed = GHOST_SPEED

    def bfs(self, game_map, start, target):
        if start == target:
            return []
        
        visited = set()
        queue = deque([(start, [])])
        visited.add(start)
        
        while queue:
            (x, y), path = queue.popleft()
            
            for dx, dy in [UP, DOWN, LEFT, RIGHT]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited and game_map.can_move_to(nx, ny):
                    if (nx, ny) == target:
                        return path + [(dx, dy)]
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(dx, dy)]))
        
        return []

    def get_target(self, pacman, pacman_direction, red_ghost_pos):
        px, py = pacman
        
        if self.ghost_type == GHOST_RED:
            return (px, py)
        elif self.ghost_type == GHOST_PINK:
            dx, dy = pacman_direction
            return (px + dx * 2, py + dy * 2)
        elif self.ghost_type == GHOST_CYAN:
            rx, ry = red_ghost_pos
            dx, dy = pacman_direction
            target_x = px + dx * 2
            target_y = py + dy * 2
            return (2 * target_x - rx, 2 * target_y - ry)
        elif self.ghost_type == GHOST_ORANGE:
            dist = math.hypot(px - self.grid_x, py - self.grid_y)
            if dist > 8:
                return (px, py)
            else:
                corners = [(1, 1), (18, 1), (1, 18), (18, 18)]
                return random.choice(corners)
        
        return (px, py)

    def can_move(self, game_map, direction):
        dx, dy = direction
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        return game_map.can_move_to(new_x, new_y)

    def update(self, game_map, pacman, pacman_direction, red_ghost_pos, level):
        if self.vulnerable:
            self.vulnerable_timer -= 1
            if self.vulnerable_timer <= 0:
                self.vulnerable = False
                self.eaten = False
                self.speed = GHOST_SPEED + (level - 1) * 0.3

        if self.eaten:
            target = (10, 10)
        elif self.vulnerable:
            px, py = pacman
            corners = [(1, 1), (18, 1), (1, 18), (18, 18)]
            target = min(corners, key=lambda c: math.hypot(c[0] - px, c[1] - py))
        else:
            target = self.get_target(pacman, pacman_direction, red_ghost_pos)

        center_x = self.grid_x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.grid_y * CELL_SIZE + CELL_SIZE // 2
        dist_to_center = math.hypot(self.x - center_x, self.y - center_y)

        if dist_to_center < self.speed:
            self.x = center_x
            self.y = center_y

            possible_dirs = []
            for direction in [UP, DOWN, LEFT, RIGHT]:
                if direction != (-self.direction[0], -self.direction[1]) and self.can_move(game_map, direction):
                    possible_dirs.append(direction)

            if possible_dirs:
                if len(possible_dirs) == 1:
                    self.direction = possible_dirs[0]
                else:
                    path = self.bfs(game_map, (self.grid_x, self.grid_y), target)
                    if path:
                        self.direction = path[0]
                    else:
                        self.direction = random.choice(possible_dirs)

            dx, dy = self.direction
            if self.can_move(game_map, self.direction):
                self.grid_x += dx
                self.grid_y += dy
        else:
            dx, dy = self.direction
            current_speed = self.speed
            if self.vulnerable and not self.eaten:
                current_speed = VULNERABLE_GHOST_SPEED
            self.x += dx * current_speed
            self.y += dy * current_speed

    def draw(self, surface):
        center_x = int(self.x)
        center_y = int(self.y)
        radius = CELL_SIZE // 2 - 4

        if self.vulnerable and not self.eaten:
            remaining = self.vulnerable_timer
            if remaining < POWER_PELLET_BLINK_START:
                if int(pygame.time.get_ticks() / 200) % 2 == 0:
                    color = WHITE
                else:
                    color = (100, 100, 255)
            else:
                color = (100, 100, 255)
        elif self.eaten:
            color = (50, 50, 100)
        else:
            color = self.colors[self.ghost_type]

        pygame.draw.circle(surface, color, (center_x, center_y - 2), radius)
        
        rect = pygame.Rect(center_x - radius, center_y - 4, radius * 2, radius)
        pygame.draw.rect(surface, color, rect)
        
        wave_width = radius * 2 // 4
        for i in range(4):
            wave_x = center_x - radius + i * wave_width + wave_width // 2
            pygame.draw.circle(surface, BLACK, (wave_x, center_y + radius - 4), wave_width // 2)

        if not self.eaten:
            eye_radius = radius // 4
            pupil_radius = eye_radius // 2
            
            left_eye_x = center_x - radius // 2
            right_eye_x = center_x + radius // 2
            eye_y = center_y - radius // 3
            
            pygame.draw.circle(surface, WHITE, (left_eye_x, eye_y), eye_radius)
            pygame.draw.circle(surface, WHITE, (right_eye_x, eye_y), eye_radius)
            
            dx, dy = self.direction
            pupil_offset_x = dx * pupil_radius
            pupil_offset_y = dy * pupil_radius
            
            pygame.draw.circle(surface, BLACK, (left_eye_x + pupil_offset_x, eye_y + pupil_offset_y), pupil_radius)
            pygame.draw.circle(surface, BLACK, (right_eye_x + pupil_offset_x, eye_y + pupil_offset_y), pupil_radius)

    def get_grid_pos(self):
        return (self.grid_x, self.grid_y)

    def get_pos(self):
        return (self.x, self.y)

    def set_vulnerable(self):
        self.vulnerable = True
        self.vulnerable_timer = POWER_PELLET_DURATION // 16
        self.speed = VULNERABLE_GHOST_SPEED
        self.eaten = False

    def set_eaten(self):
        self.eaten = True
        self.speed = GHOST_SPEED * 2

    def is_vulnerable(self):
        return self.vulnerable and not self.eaten

    def is_eaten(self):
        return self.eaten

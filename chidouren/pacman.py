
import pygame
import math
from constants import *


class Pacman:
    def __init__(self, start_pos):
        self.start_grid_x, self.start_grid_y = start_pos
        self.reset()

    def reset(self):
        self.grid_x = self.start_grid_x
        self.grid_y = self.start_grid_y
        self.x = self.grid_x * CELL_SIZE + CELL_SIZE // 2
        self.y = self.grid_y * CELL_SIZE + CELL_SIZE // 2
        self.direction = LEFT
        self.next_direction = None
        self.speed = PACMAN_SPEED
        self.mouth_angle = 0
        self.mouth_open = True
        self.mouth_speed = 0.2
        self.invincible = False
        self.invincible_timer = 0

    def set_next_direction(self, direction):
        self.next_direction = direction

    def can_move(self, game_map, direction):
        dx, dy = direction
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        return game_map.can_move_to(new_x, new_y)

    def update(self, game_map):
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        if self.next_direction and self.can_move(game_map, self.next_direction):
            self.direction = self.next_direction
            self.next_direction = None

        center_x = self.grid_x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.grid_y * CELL_SIZE + CELL_SIZE // 2

        dist_to_center = math.hypot(self.x - center_x, self.y - center_y)

        if dist_to_center < self.speed:
            self.x = center_x
            self.y = center_y

            if self.can_move(game_map, self.direction):
                dx, dy = self.direction
                self.grid_x += dx
                self.grid_y += dy
            elif self.next_direction and self.can_move(game_map, self.next_direction):
                self.direction = self.next_direction
                self.next_direction = None
                dx, dy = self.direction
                self.grid_x += dx
                self.grid_y += dy
        else:
            dx, dy = self.direction
            self.x += dx * self.speed
            self.y += dy * self.speed

        if self.mouth_open:
            self.mouth_angle += self.mouth_speed
            if self.mouth_angle >= 0.5:
                self.mouth_open = False
        else:
            self.mouth_angle -= self.mouth_speed
            if self.mouth_angle <= 0:
                self.mouth_open = True

    def draw(self, surface):
        if self.invincible:
            if int(pygame.time.get_ticks() / 100) % 2 == 0:
                return

        center_x = int(self.x)
        center_y = int(self.y)
        radius = CELL_SIZE // 2 - 4

        start_angle = 0
        end_angle = 2 * math.pi

        if self.mouth_angle > 0:
            if self.direction == RIGHT:
                start_angle = self.mouth_angle * math.pi
                end_angle = (2 - self.mouth_angle) * math.pi
            elif self.direction == LEFT:
                start_angle = (1 + self.mouth_angle) * math.pi
                end_angle = (1 - self.mouth_angle) * math.pi
            elif self.direction == UP:
                start_angle = (0.5 + self.mouth_angle) * math.pi
                end_angle = (0.5 - self.mouth_angle) * math.pi
            elif self.direction == DOWN:
                start_angle = (1.5 + self.mouth_angle) * math.pi
                end_angle = (1.5 - self.mouth_angle) * math.pi

        pygame.draw.circle(surface, YELLOW, (center_x, center_y), radius)
        
        if self.mouth_angle > 0:
            points = [(center_x, center_y)]
            num_points = 10
            for i in range(num_points + 1):
                angle = start_angle + (end_angle - start_angle) * i / num_points
                px = center_x + math.cos(angle) * radius
                py = center_y + math.sin(angle) * radius
                points.append((px, py))
            
            if len(points) > 2:
                pygame.draw.polygon(surface, BLACK, points)

    def get_grid_pos(self):
        return (self.grid_x, self.grid_y)

    def get_pos(self):
        return (self.x, self.y)

    def set_invincible(self, duration):
        self.invincible = True
        self.invincible_timer = duration

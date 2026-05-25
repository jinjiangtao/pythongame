import random
from collections import deque

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = None

    def generate(self):
        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        stack = []
        start_x, start_y = 1, 1
        self.maze[start_y][start_x] = 0
        stack.append((start_x, start_y))

        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        while stack:
            current_x, current_y = stack[-1]
            neighbors = []

            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                if 1 <= nx < self.width - 1 and 1 <= ny < self.height - 1:
                    if self.maze[ny][nx] == 1:
                        neighbors.append((nx, ny, dx // 2, dy // 2))

            if neighbors:
                nx, ny, wall_x, wall_y = random.choice(neighbors)
                self.maze[ny][nx] = 0
                self.maze[current_y + wall_y][current_x + wall_x] = 0
                stack.append((nx, ny))
            else:
                stack.pop()

        return self.maze

    def get_empty_positions(self):
        positions = []
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 0:
                    positions.append((x, y))
        return positions

class Maze:
    def __init__(self, level):
        self.level = level
        self.base_size = 15
        self.size = self.base_size + level * 2
        self.cell_size = 30
        self.width = self.size
        self.height = self.size
        self.grid = None
        self.start = None
        self.end = None
        self.generate_maze()

    def generate_maze(self):
        generator = MazeGenerator(self.width, self.height)
        self.grid = generator.generate()
        empty_positions = generator.get_empty_positions()
        
        self.start = empty_positions[0]
        self.end = empty_positions[-1]
        
        if self.start == self.end and len(empty_positions) > 1:
            self.end = empty_positions[1]

    def is_wall(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.grid[y][x] == 1

    def get_screen_coords(self, grid_x, grid_y):
        return grid_x * self.cell_size, grid_y * self.cell_size
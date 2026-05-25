import random

class ItemType:
    HEALTH = 'health'
    TRAP = 'trap'

class Item:
    def __init__(self, item_type, grid_x, grid_y):
        self.type = item_type
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.collected = False

    def get_screen_coords(self, maze):
        return maze.get_screen_coords(self.grid_x, self.grid_y)

class ItemManager:
    def __init__(self, maze):
        self.maze = maze
        self.items = []
        self.generate_items()

    def generate_items(self):
        self.items = []
        empty_positions = []
        
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 0 and (x, y) != self.maze.start and (x, y) != self.maze.end:
                    empty_positions.append((x, y))
        
        random.shuffle(empty_positions)
        num_items = min(len(empty_positions) // 5, 3 + self.maze.level)
        
        trap_count = max(1, num_items // 2)
        health_count = num_items - trap_count
        
        used_positions = set()
        
        for _ in range(trap_count):
            if empty_positions:
                pos = empty_positions.pop()
                while pos in used_positions:
                    if not empty_positions:
                        break
                    pos = empty_positions.pop()
                if pos not in used_positions:
                    used_positions.add(pos)
                    self.items.append(Item(ItemType.TRAP, pos[0], pos[1]))
        
        for _ in range(health_count):
            if empty_positions:
                pos = empty_positions.pop()
                while pos in used_positions:
                    if not empty_positions:
                        break
                    pos = empty_positions.pop()
                if pos not in used_positions:
                    used_positions.add(pos)
                    self.items.append(Item(ItemType.HEALTH, pos[0], pos[1]))

    def check_collision(self, player):
        for item in self.items:
            if not item.collected and item.grid_x == player.grid_x and item.grid_y == player.grid_y:
                item.collected = True
                return item
        return None

    def reset(self):
        self.generate_items()
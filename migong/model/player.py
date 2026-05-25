class Player:
    def __init__(self, maze):
        self.maze = maze
        self.reset()

    def reset(self):
        self.grid_x, self.grid_y = self.maze.start
        self.screen_x, self.screen_y = self.maze.get_screen_coords(self.grid_x, self.grid_y)
        self.health = 3
        self.max_health = 3
        self.steps = 0
        self.is_alive = True

    def move(self, dx, dy):
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        
        if not self.maze.is_wall(new_x, new_y):
            self.grid_x = new_x
            self.grid_y = new_y
            self.screen_x, self.screen_y = self.maze.get_screen_coords(self.grid_x, self.grid_y)
            self.steps += 1
            return True
        return False

    def take_damage(self, amount=1):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_alive = False

    def heal(self, amount=1):
        self.health = min(self.health + amount, self.max_health)

    def has_reached_end(self):
        return self.grid_x == self.maze.end[0] and self.grid_y == self.maze.end[1]
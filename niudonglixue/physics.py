import math
from config import GRAVITY, TIME_STEP

class PhysicsObject:
    def __init__(self, x, y, width, height, mass=1.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = 0
        self.vy = 0
        self.mass = mass
        self.ax = 0
        self.ay = 0
        self.is_moving = False
        self.is_grounded = False

    def apply_force(self, fx, fy):
        self.ax += fx / self.mass
        self.ay += fy / self.mass

    def update(self, dt=TIME_STEP):
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.ax = 0
        self.ay = 0
        self.is_moving = abs(self.vx) > 0.1 or abs(self.vy) > 0.1

    def get_center(self):
        return (self.x + self.width / 2, self.y + self.height / 2)

    def check_collision(self, other):
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)

class Ball(PhysicsObject):
    def __init__(self, x, y, radius, mass=1.0):
        super().__init__(x, y, radius * 2, radius * 2, mass)
        self.radius = radius

    def get_center(self):
        return (self.x + self.radius, self.y + self.radius)

class Block(PhysicsObject):
    def __init__(self, x, y, width, height, mass=1.0):
        super().__init__(x, y, width, height, mass)

class Spring:
    def __init__(self, x1, y1, x2, y2, k=100, rest_length=100):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.k = k
        self.rest_length = rest_length
        self.connected_object = None

    def get_length(self):
        return math.hypot(self.x2 - self.x1, self.y2 - self.y1)

    def get_force(self):
        length = self.get_length()
        extension = length - self.rest_length
        if abs(extension) < 1:
            return 0, 0
        force_magnitude = self.k * extension
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        if length > 0:
            fx = -force_magnitude * (dx / length)
            fy = -force_magnitude * (dy / length)
            return fx, fy
        return 0, 0

    def update(self):
        if self.connected_object:
            fx, fy = self.get_force()
            self.connected_object.apply_force(fx, fy)

class Lever:
    def __init__(self, pivot_x, pivot_y, length=200, angle=0):
        self.pivot_x = pivot_x
        self.pivot_y = pivot_y
        self.length = length
        self.angle = angle
        self.left_weight = 0
        self.right_weight = 0
        self.left_distance = length / 2
        self.right_distance = length / 2
        self.angular_velocity = 0

    def update(self):
        torque = (self.right_weight * self.right_distance - 
                  self.left_weight * self.left_distance) * 10
        self.angular_velocity += torque * TIME_STEP * 0.1
        self.angular_velocity *= 0.98
        self.angle += self.angular_velocity

    def get_end_points(self):
        left_x = self.pivot_x - math.cos(self.angle) * self.left_distance
        left_y = self.pivot_y - math.sin(self.angle) * self.left_distance
        right_x = self.pivot_x + math.cos(self.angle) * self.right_distance
        right_y = self.pivot_y + math.sin(self.angle) * self.right_distance
        return (left_x, left_y), (right_x, right_y)

class PhysicsEngine:
    def __init__(self):
        self.objects = []
        self.gravity_enabled = True

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def update(self):
        for obj in self.objects:
            if self.gravity_enabled:
                obj.apply_force(0, obj.mass * GRAVITY)
            obj.update()

    def clear(self):
        self.objects.clear()

    def set_gravity(self, enabled):
        self.gravity_enabled = enabled
import math
import customtkinter as ctk
from physics import Ball, Block, Spring, Lever

class GravityScene:
    def __init__(self, canvas, colors):
        self.canvas = canvas
        self.colors = colors
        self.ground_y = 420
        self.is_dropped = False
        self.drop_time = 0
        self.ball_x = 375
        self.ball_y = 50
        self.ball_radius = 30
        self.ball_vy = 0
        self.init_scene()

    def init_scene(self):
        self.canvas.delete("all")
        self.draw_ground()
        self.draw_ball()
        self.is_dropped = False
        self.drop_time = 0
        self.ball_y = 50
        self.ball_vy = 0

    def draw_ground(self):
        self.canvas.create_rectangle(0, self.ground_y, 800, 500, fill=self.colors["accent"], outline="")
        self.canvas.create_text(400, 465, text="地面", fill=self.colors["text"], font=("Arial", 12))

    def draw_ball(self):
        self.canvas.create_oval(
            self.ball_x, self.ball_y,
            self.ball_x + self.ball_radius * 2,
            self.ball_y + self.ball_radius * 2,
            fill="#ff4444", outline="#cc0000", width=3, tags="ball"
        )

    def drop(self):
        if not self.is_dropped:
            self.is_dropped = True

    def update(self):
        if self.is_dropped:
            self.ball_vy += 9.8 * 0.016 * 10
            self.ball_y += self.ball_vy * 0.016 * 60
            
            if self.ball_y + self.ball_radius * 2 >= self.ground_y:
                self.ball_y = self.ground_y - self.ball_radius * 2
                self.ball_vy = 0
                self.is_dropped = False
            
            self.canvas.delete("ball")
            self.canvas.create_oval(
                self.ball_x, self.ball_y,
                self.ball_x + self.ball_radius * 2,
                self.ball_y + self.ball_radius * 2,
                fill="#ff4444", outline="#cc0000", width=3, tags="ball"
            )

    def get_data(self):
        return {
            "速度": f"{abs(self.ball_vy):.2f} m/s",
            "下落时间": f"{self.drop_time:.2f} s",
            "状态": "下落中" if self.is_dropped else "静止"
        }

    def reset(self):
        self.init_scene()

class FrictionScene:
    def __init__(self, canvas, colors):
        self.canvas = canvas
        self.colors = colors
        self.block = Block(50, 310, 60, 60, mass=3.0)
        self.friction = 0.5
        self.surface_type = "rough"
        self.start_x = 50
        self.total_distance = 0
        self.is_sliding = False
        self.init_scene()

    def init_scene(self):
        self.canvas.delete("all")
        self.draw_surface()
        self.draw_block()
        self.is_sliding = False
        self.total_distance = 0

    def draw_surface(self):
        if self.surface_type == "rough":
            color = "#8b4513"
            pattern = "////////"
        else:
            color = "#add8e6"
            pattern = "~~~~~~~~"
        
        self.canvas.create_rectangle(0, 380, 800, 460, fill=color, outline="")
        for i in range(0, 800, 30):
            self.canvas.create_text(i + 15, 420, text=pattern[:5], fill="white", font=("Arial", 8))
        self.canvas.create_text(400, 445, text=f"接触面: {self.surface_type == '粗糙' and '粗糙' or '光滑'}", fill=self.colors["text"], font=("Arial", 12))

    def draw_block(self):
        if self.block:
            self.block.x = self.start_x
            self.block.vx = 0
            self.canvas.create_rectangle(
                self.block.x, self.block.y,
                self.block.x + self.block.width,
                self.block.y + self.block.height,
                fill="#3498db", outline="#2980b9", width=2, tags="block"
            )

    def set_friction(self, value):
        self.friction = value
        self.surface_type = "rough" if value > 0.3 else "smooth"
        self.init_scene()

    def push(self):
        if not self.is_sliding:
            self.block.vx = 15
            self.is_sliding = True
            self.total_distance = 0

    def update(self):
        if self.is_sliding and self.block:
            friction_force = -self.block.vx * self.friction * 2
            self.block.apply_force(friction_force, 0)
            self.block.update()
            self.total_distance += abs(self.block.vx * 0.016)
            
            if abs(self.block.vx) < 0.1:
                self.block.vx = 0
                self.is_sliding = False
            
            self.canvas.delete("block")
            self.canvas.create_rectangle(
                self.block.x, self.block.y,
                self.block.x + self.block.width,
                self.block.y + self.block.height,
                fill="#3498db", outline="#2980b9", width=2, tags="block"
            )

    def get_data(self):
        return {
            "速度": f"{self.block.vx:.2f} m/s",
            "滑行距离": f"{self.total_distance:.2f} m",
            "摩擦力系数": f"{self.friction:.2f}",
            "状态": "滑行中" if self.is_sliding else "静止"
        }

    def reset(self):
        self.init_scene()

class InclineScene:
    def __init__(self, canvas, colors):
        self.canvas = canvas
        self.colors = colors
        self.angle = 30
        self.incline_length = 300
        self.is_sliding = False
        self.slide_distance = 0
        self.incline_start = None
        self.incline_end = None
        self.init_scene()

    def init_scene(self):
        self.canvas.delete("all")
        self.draw_incline()
        self.draw_block()
        self.is_sliding = False
        self.slide_distance = 0

    def draw_incline(self):
        angle_rad = math.radians(self.angle)
        x1, y1 = 100, 450
        x2 = x1 + self.incline_length * math.cos(angle_rad)
        y2 = y1 - self.incline_length * math.sin(angle_rad)
        
        self.canvas.create_polygon(x1, y1, x2, y2, x1, y2, fill="#f39c12", outline="#e67e22", width=2)
        self.canvas.create_text(x1 + 30, y2 + 15, text=f"斜面角度: {self.angle}°", fill=self.colors["text"], font=("Arial", 12))

        self.incline_start = (x2, y2)
        self.incline_end = (x1, y1)
        self.block = Block(x2 - 20, y2 - 30, 40, 30, mass=2.0)

    def draw_block(self):
        if self.block and self.incline_start:
            x, y = self.incline_start
            self.block.x = x - 20
            self.block.y = y - 30
            self.block.vx = 0
            self.block.vy = 0
            self.canvas.create_rectangle(
                self.block.x, self.block.y,
                self.block.x + self.block.width,
                self.block.y + self.block.height,
                fill="#9b59b6", outline="#8e44ad", width=2, tags="block"
            )

    def set_angle(self, angle):
        self.angle = angle
        self.init_scene()

    def release(self):
        if not self.is_sliding:
            self.is_sliding = True

    def update(self):
        if self.is_sliding and self.block:
            angle_rad = math.radians(self.angle)
            gravity_force = self.block.mass * 9.8
            fx = gravity_force * math.sin(angle_rad)
            fy = -gravity_force * math.cos(angle_rad)
            
            self.block.apply_force(fx * 0.5, fy * 0.5)
            self.block.update()
            
            self.slide_distance += abs(self.block.vx * 0.016)
            
            if self.block.x <= self.incline_end[0]:
                self.block.x = self.incline_end[0]
                self.block.vx = 0
                self.is_sliding = False
            
            self.canvas.delete("block")
            self.canvas.create_rectangle(
                self.block.x, self.block.y,
                self.block.x + self.block.width,
                self.block.y + self.block.height,
                fill="#9b59b6", outline="#8e44ad", width=2, tags="block"
            )

    def get_data(self):
        return {
            "速度": f"{self.block.vx:.2f} m/s",
            "滑行距离": f"{self.slide_distance:.2f} m",
            "斜面角度": f"{self.angle}°",
            "状态": "下滑中" if self.is_sliding else "静止"
        }

    def reset(self):
        self.init_scene()

class LeverScene:
    def __init__(self, canvas, colors):
        self.canvas = canvas
        self.colors = colors
        self.lever = None
        self.left_weight = 2
        self.right_weight = 2
        self.pivot_position = 0.5
        self.init_scene()

    def init_scene(self):
        self.canvas.delete("all")
        self.draw_pivot()
        self.draw_lever()
        self.draw_weights()

    def draw_pivot(self):
        self.pivot_x = 400
        self.pivot_y = 300
        self.canvas.create_oval(self.pivot_x - 15, self.pivot_y - 15,
                               self.pivot_x + 15, self.pivot_y + 15,
                               fill="#2ecc71", outline="#27ae60", width=2)

    def draw_lever(self):
        if self.lever:
            self.lever.angle = 0
            self.lever.angular_velocity = 0
        else:
            self.lever = Lever(self.pivot_x, self.pivot_y, length=350)
        
        self.lever.left_distance = 350 * self.pivot_position
        self.lever.right_distance = 350 * (1 - self.pivot_position)
        self.lever.left_weight = self.left_weight
        self.lever.right_weight = self.right_weight
        
        self.update_display()

    def draw_weights(self):
        pass

    def set_weights(self, left, right):
        self.left_weight = left
        self.right_weight = right
        if self.lever:
            self.lever.left_weight = left
            self.lever.right_weight = right

    def set_pivot(self, position):
        self.pivot_position = position
        if self.lever:
            self.lever.left_distance = 350 * position
            self.lever.right_distance = 350 * (1 - position)

    def release(self):
        pass

    def update(self):
        if self.lever:
            self.lever.update()
            self.update_display()

    def update_display(self):
        self.canvas.delete("lever", "weight_left", "weight_right")
        
        (left_x, left_y), (right_x, right_y) = self.lever.get_end_points()
        
        self.canvas.create_line(left_x, left_y, right_x, right_y, 
                               fill="#34495e", width=8, tags="lever")
        
        weight_size = 20
        
        self.canvas.create_oval(left_x - weight_size, left_y,
                               left_x + weight_size, left_y + weight_size * 2,
                               fill="#e74c3c", outline="#c0392b", tags="weight_left")
        self.canvas.create_text(left_x, left_y + weight_size + 15, 
                               text=f"{self.left_weight}kg", fill=self.colors["text"], font=("Arial", 10))
        
        self.canvas.create_oval(right_x - weight_size, right_y,
                               right_x + weight_size, right_y + weight_size * 2,
                               fill="#3498db", outline="#2980b9", tags="weight_right")
        self.canvas.create_text(right_x, right_y + weight_size + 15, 
                               text=f"{self.right_weight}kg", fill=self.colors["text"], font=("Arial", 10))

    def get_data(self):
        return {
            "左侧重量": f"{self.left_weight} kg",
            "右侧重量": f"{self.right_weight} kg",
            "支点位置": f"{int(self.pivot_position * 100)}%",
            "状态": "平衡中" if abs(self.lever.angular_velocity) < 0.01 else "转动中"
        }

    def reset(self):
        self.init_scene()

class SpringScene:
    def __init__(self, canvas, colors):
        self.canvas = canvas
        self.colors = colors
        self.block = Block(250, 270, 60, 60, mass=2.0)
        self.spring = Spring(90, 300, 250, 300, k=50, rest_length=160)
        self.spring.connected_object = self.block
        self.is_released = False
        self.max_compression = 0
        self.init_scene()

    def init_scene(self):
        self.canvas.delete("all")
        self.draw_wall()
        self.draw_spring()
        self.draw_block()
        self.is_released = False
        self.max_compression = 0

    def draw_wall(self):
        self.canvas.create_rectangle(50, 150, 90, 450, fill="#7f8c8d", outline="#7f8c8d")

    def draw_spring(self):
        self.canvas.create_line(self.spring.x1, self.spring.y1,
                               self.spring.x2, self.spring.y2,
                               fill="#f1c40f", width=4, tags="spring")
        
        coils = 10
        dx = self.spring.x2 - self.spring.x1
        dy = self.spring.y2 - self.spring.y1
        length = math.hypot(dx, dy)
        
        if length > 0:
            step = length / coils
            px, py = self.spring.x1, self.spring.y1
            for i in range(coils):
                nx = px + dx * step / length
                ny = py + dy * step / length
                self.canvas.create_line(px, py, nx, ny, fill="#f1c40f", width=4)
                px, py = nx, ny

    def draw_block(self):
        self.canvas.create_rectangle(
            self.block.x, self.block.y,
            self.block.x + self.block.width,
            self.block.y + self.block.height,
            fill="#1abc9c", outline="#16a085", width=2, tags="block"
        )

    def compress(self, distance):
        target_x = 250 - distance
        if target_x > 120:
            self.block.x = target_x
            self.max_compression = max(self.max_compression, distance)
            self.spring.x2 = self.block.x
            self.init_scene()

    def release(self):
        if not self.is_released:
            self.is_released = True

    def update(self):
        if self.is_released and self.spring and self.block:
            self.spring.update()
            self.block.update()
            
            if self.block.x > 550:
                self.block.x = 550
                self.block.vx = 0
                self.is_released = False
            
            self.spring.x2 = self.block.x
            self.spring.y2 = self.block.y + self.block.height / 2
            
            self.canvas.delete("spring", "block")
            self.draw_spring()
            self.draw_block()

    def get_data(self):
        compression = 120 - self.spring.get_length() if self.spring else 0
        return {
            "弹力": f"{abs(compression * 0.5):.2f} N",
            "最大压缩": f"{self.max_compression:.2f} px",
            "当前压缩": f"{max(0, -compression):.2f} px",
            "状态": "回弹中" if self.is_released else "静止"
        }

    def reset(self):
        self.init_scene()

class InertiaScene:
    def __init__(self, canvas, colors):
        self.canvas = canvas
        self.colors = colors
        self.platform = None
        self.block = None
        self.is_pulled = False
        self.init_scene()

    def init_scene(self):
        self.canvas.delete("all")
        self.draw_platform()
        self.draw_block()
        self.is_pulled = False
        self.update_display()

    def draw_platform(self):
        if self.platform:
            self.platform.x = 250
            self.platform.vx = 0
        else:
            self.platform = Block(250, 380, 250, 30, mass=1.0)

    def draw_block(self):
        if self.block:
            self.block.x = 320
            self.block.y = 320
            self.block.vx = 0
        else:
            self.block = Block(320, 320, 100, 50, mass=2.0)

    def pull(self):
        if not self.is_pulled:
            self.platform.vx = 30
            self.is_pulled = True

    def update(self):
        if self.is_pulled and self.platform:
            self.platform.update()
            
            if self.platform.x > 500:
                self.platform.x = 500
                self.platform.vx = 0
            
            self.update_display()

    def update_display(self):
        self.canvas.delete("platform", "block")
        
        self.canvas.create_rectangle(
            self.platform.x, self.platform.y,
            self.platform.x + self.platform.width,
            self.platform.y + self.platform.height,
            fill="#95a5a6", outline="#7f8c8d", width=2, tags="platform"
        )
        self.canvas.create_text(self.platform.x + 125, self.platform.y + 15, 
                               text="书本", fill=self.colors["text"], font=("Arial", 12))
        
        self.canvas.create_rectangle(
            self.block.x, self.block.y,
            self.block.x + self.block.width,
            self.block.y + self.block.height,
            fill="#e67e22", outline="#d35400", width=2, tags="block"
        )
        self.canvas.create_text(self.block.x + 50, self.block.y + 25, 
                               text="鸡蛋", fill="white", font=("Arial", 12))

    def get_data(self):
        return {
            "平台速度": f"{self.platform.vx:.2f} m/s",
            "状态": "抽离中" if self.is_pulled and self.platform.vx > 0 else "静止"
        }

    def reset(self):
        self.init_scene()
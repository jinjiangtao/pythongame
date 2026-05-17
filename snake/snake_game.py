"""
经典贪吃蛇游戏 - Python + Pygame
功能完善，单文件实现，可直接运行
"""

import pygame
import sys
import random
import json
import os

# 游戏常量配置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = (SCREEN_HEIGHT - 100) // GRID_SIZE  # 留出顶部信息栏空间
INFO_HEIGHT = 80

# 颜色配置
BLACK = (20, 20, 30)
DARK_BLUE = (30, 30, 50)
WHITE = (255, 255, 255)
GREEN = (0, 200, 100)
DARK_GREEN = (0, 150, 80)
RED = (255, 80, 80)
GRAY = (100, 100, 120)
LIGHT_GRAY = (150, 150, 170)
GOLD = (255, 215, 0)

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 速度配置（FPS）
INITIAL_SPEED = 10
MAX_SPEED = 25
SPEED_INCREMENT = 0.5

# 分数配置
SCORE_PER_FOOD = 10
HIGH_SCORE_FILE = "snake_high_score.json"


class Snake:
    """贪吃蛇类"""

    def __init__(self):
        self.reset()

    def reset(self):
        """重置蛇到初始状态"""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False

    @property
    def head(self):
        """获取蛇头位置"""
        return self.positions[0]

    def move(self):
        """移动蛇"""
        head_x, head_y = self.head
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        if self.grow:
            self.positions = [new_head] + self.positions
            self.grow = False
        else:
            self.positions = [new_head] + self.positions[:-1]

    def change_direction(self, new_direction):
        """改变蛇的方向（防止反向掉头）"""
        if (new_direction[0] + self.direction[0] != 0 or
            new_direction[1] + self.direction[1] != 0):
            self.direction = new_direction

    def check_collision(self):
        """检测碰撞"""
        head_x, head_y = self.head
        if (head_x < 0 or head_x >= GRID_WIDTH or
            head_y < 0 or head_y >= GRID_HEIGHT):
            return True
        if self.head in self.positions[1:]:
            return True
        return False

    def draw(self, screen):
        """绘制蛇"""
        for i, (x, y) in enumerate(self.positions):
            rect = pygame.Rect(
                x * GRID_SIZE,
                y * GRID_SIZE + INFO_HEIGHT,
                GRID_SIZE - 2,
                GRID_SIZE - 2
            )
            if i == 0:
                pygame.draw.rect(screen, GREEN, rect, border_radius=5)
                pygame.draw.circle(
                    screen, WHITE,
                    (rect.centerx - 3, rect.centery - 2), 2
                )
                pygame.draw.circle(
                    screen, WHITE,
                    (rect.centerx + 3, rect.centery - 2), 2
                )
            else:
                pygame.draw.rect(screen, DARK_GREEN, rect, border_radius=4)


class Food:
    """食物类"""

    def __init__(self):
        self.position = (0, 0)
        self.spawn()

    def spawn(self, snake_positions=None):
        """生成食物位置"""
        while True:
            self.position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if snake_positions is None or self.position not in snake_positions:
                break

    def draw(self, screen):
        """绘制食物"""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE + 1,
            self.position[1] * GRID_SIZE + INFO_HEIGHT + 1,
            GRID_SIZE - 2,
            GRID_SIZE - 2
        )
        pygame.draw.ellipse(screen, RED, rect, border_radius=5)


class Game:
    """游戏主类"""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("经典贪吃蛇游戏")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 48)

        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_state = "start"  # start, running, paused, game_over
        self.speed = INITIAL_SPEED

    def load_high_score(self):
        """从本地文件加载最高分"""
        try:
            if os.path.exists(HIGH_SCORE_FILE):
                with open(HIGH_SCORE_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except Exception:
            pass
        return 0

    def save_high_score(self):
        """保存最高分到本地文件"""
        try:
            with open(HIGH_SCORE_FILE, 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except Exception:
            pass

    def start_new_game(self):
        """开始新游戏"""
        self.snake.reset()
        self.food.spawn(self.snake.positions)
        self.score = 0
        self.speed = INITIAL_SPEED
        self.game_state = "running"

    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if self.game_state == "start":
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.start_new_game()

                elif self.game_state == "running":
                    if event.key == pygame.K_SPACE:
                        self.game_state = "paused"
                    elif event.key in [pygame.K_UP, pygame.K_w]:
                        self.snake.change_direction(UP)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.snake.change_direction(DOWN)
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        self.snake.change_direction(LEFT)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        self.snake.change_direction(RIGHT)

                elif self.game_state == "paused":
                    if event.key == pygame.K_SPACE:
                        self.game_state = "running"

                elif self.game_state == "game_over":
                    if event.key == pygame.K_r:
                        self.start_new_game()
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        return False

        return True

    def update(self):
        """更新游戏逻辑"""
        if self.game_state != "running":
            return

        self.snake.move()

        if self.snake.check_collision():
            self.game_state = "game_over"
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            return

        if self.snake.head == self.food.position:
            self.score += SCORE_PER_FOOD
            self.snake.grow = True
            self.food.spawn(self.snake.positions)
            self.speed = min(MAX_SPEED, INITIAL_SPEED + (self.score // 50) * SPEED_INCREMENT)

    def draw_info_bar(self):
        """绘制顶部信息栏"""
        pygame.draw.rect(self.screen, DARK_BLUE, (0, 0, SCREEN_WIDTH, INFO_HEIGHT))

        score_text = self.font.render(f"得分: {self.score}", True, WHITE)
        high_score_text = self.font.render(f"最高分: {self.high_score}", True, GOLD)

        self.screen.blit(score_text, (20, 25))
        self.screen.blit(high_score_text, (200, 25))

        if self.game_state == "running":
            state_text = self.small_font.render("游戏进行中 - 按空格键暂停", True, GREEN)
        elif self.game_state == "paused":
            state_text = self.small_font.render("游戏已暂停 - 按空格键继续", True, GOLD)
        elif self.game_state == "game_over":
            state_text = self.small_font.render("游戏结束", True, RED)
        else:
            state_text = self.small_font.render("按 Enter 或空格键开始游戏", True, LIGHT_GRAY)

        self.screen.blit(state_text, (450, 30))

    def draw_grid(self):
        """绘制网格背景"""
        self.screen.fill(BLACK)
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, DARK_BLUE, (x, INFO_HEIGHT), (x, SCREEN_HEIGHT))
        for y in range(INFO_HEIGHT, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, DARK_BLUE, (0, y), (SCREEN_WIDTH, y))

    def draw_border(self):
        """绘制游戏边界"""
        border_rect = pygame.Rect(0, INFO_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - INFO_HEIGHT)
        pygame.draw.rect(self.screen, GRAY, border_rect, 3)

    def draw_start_screen(self):
        """绘制开始界面"""
        title = self.title_font.render("经典贪吃蛇游戏", True, GREEN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(title, title_rect)

        instructions = [
            "使用 方向键 或 WASD 控制蛇的移动",
            "吃到食物得分，蛇身变长",
            "撞到边界或自己的身体游戏结束",
            "按 空格键 暂停/继续游戏",
            "",
            f"当前最高分: {self.high_score}",
            "",
            "按 Enter 或空格键开始游戏"
        ]

        for i, text in enumerate(instructions):
            color = WHITE if i < 4 else GOLD if i == 5 else LIGHT_GRAY
            font = self.small_font if i != 7 else self.font
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 30))
            self.screen.blit(text_surface, text_rect)

    def draw_game_over_screen(self):
        """绘制游戏结束界面"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.title_font.render("游戏结束", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(game_over_text, game_over_rect)

        score_text = self.font.render(f"您的得分: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(score_text, score_rect)

        if self.score == self.high_score and self.score > 0:
            new_record_text = self.font.render("恭喜打破最高分记录！", True, GOLD)
            new_record_rect = new_record_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            self.screen.blit(new_record_text, new_record_rect)
            y_offset = 60
        else:
            y_offset = 20

        high_score_text = self.font.render(f"最高分: {self.high_score}", True, GOLD)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
        self.screen.blit(high_score_text, high_score_rect)

        restart_text = self.small_font.render("按 R 键重新开始", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(restart_text, restart_rect)

        quit_text = self.small_font.render("按 Q 或 ESC 退出游戏", True, GRAY)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 130))
        self.screen.blit(quit_text, quit_rect)

    def draw_pause_overlay(self):
        """绘制暂停遮罩"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))

        pause_text = self.title_font.render("游戏暂停", True, GOLD)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(pause_text, pause_rect)

        continue_text = self.font.render("按空格键继续游戏", True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(continue_text, continue_rect)

    def draw(self):
        """绘制所有游戏元素"""
        self.draw_grid()
        self.draw_border()
        self.draw_info_bar()

        if self.game_state == "start":
            self.draw_start_screen()
        else:
            self.food.draw(self.screen)
            self.snake.draw(self.screen)

            if self.game_state == "paused":
                self.draw_pause_overlay()
            elif self.game_state == "game_over":
                self.draw_game_over_screen()

        pygame.display.flip()

    def run(self):
        """游戏主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.speed)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    print("=" * 50)
    print("经典贪吃蛇游戏")
    print("=" * 50)
    print("\n依赖安装命令:")
    print("pip install pygame")
    print("\n运行步骤:")
    print("1. 确保已安装 pygame: pip install pygame")
    print("2. 直接运行本文件: python snake_game.py")
    print("\n游戏说明:")
    print("- 使用方向键或WASD控制蛇的移动")
    print("- 按空格键暂停/继续游戏")
    print("- 按R键重新开始，按Q或ESC退出")
    print("\n" + "=" * 50)

    game = Game()
    game.run()

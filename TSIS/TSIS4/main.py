import pygame
import json
import os
import sys
import random
from config import *
from db import *
from game import Food, generate_level_obstacles

class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game - TSIS 4 Submission")
        self.clock = pygame.time.Clock()
        
        self.load_settings() # Task 3.5
        self.load_assets()
        self.load_sounds()
        
        self.state = "MENU"
        self.user_input = ""
        self.reset_game("Guest", 0, 0)

    def load_settings(self):
        """Task 3.5: Load JSON settings safely using .get() to avoid KeyError"""
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r") as f:
                    self.settings = json.load(f)
            except:
                self.settings = {}
        else:
            self.settings = {}
        
        # Using .get(key, default_value) prevents KeyError if the key is missing
        self.snake_color = self.settings.get("snake_color", [0, 255, 0])
        self.show_grid = self.settings.get("grid", True)
        self.sound_on = self.settings.get("sound", True)
        
    def save_settings_to_file(self):
        """Task 3.5: Save current settings to JSON"""
        data = {"snake_color": self.snake_color, "grid": self.show_grid, "sound": self.sound_on}
        with open("settings.json", "w") as f: json.dump(data, f)

    def load_assets(self):
        path = r"C:\Users\tamer\OneDrive\Documents\PP2\TSIS\TSIS4\assets"
        try:
            self.img_head = pygame.transform.scale(pygame.image.load(os.path.join(path, "head.png")), (20, 20))
            self.img_apple = pygame.transform.scale(pygame.image.load(os.path.join(path, "apple.png")), (20, 20))
            self.img_poison = pygame.transform.scale(pygame.image.load(os.path.join(path, "poison.png")), (20, 20))
            self.img_wall = pygame.transform.scale(pygame.image.load(os.path.join(path, "wall.png")), (20, 20))
        except: print("Error: PNG files missing in assets!"); sys.exit()

    def load_sounds(self):
        path = r"C:\Users\tamer\OneDrive\Documents\PP2\TSIS\TSIS4\assets"
        try:
            self.snd_eat = pygame.mixer.Sound(os.path.join(path, "eat.wav"))
            pygame.mixer.music.load(os.path.join(path, "background.mp3"))
            if self.sound_on: pygame.mixer.music.play(-1)
        except: pass

    def reset_game(self, user, p_id, pb):
        self.username, self.player_id, self.personal_best = user, p_id, pb
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.direction = pygame.K_RIGHT
        self.score, self.level = 0, 1
        self.base_fps = FPS
        self.current_fps = FPS
        self.obstacles = []
        self.food = Food(self.snake, self.obstacles)
        self.poison = Food(self.snake, self.obstacles, True)
        self.powerup = None
        self.powerup_timer = 0
        self.effect_timer = 0
        self.shield_active = False

    def spawn_powerup(self):
        """Task 3.3: Temporary power-ups logic"""
        self.powerup_type = random.choice(['speed', 'slow', 'shield'])
        self.powerup = Food(self.snake, self.obstacles)
        self.powerup_timer = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        # Task 3.3: Power-up despawn after 8s
        if self.powerup and (now - self.powerup_timer > 8000): self.powerup = None
        # Task 3.3: Effect duration 5s
        if now > self.effect_timer: self.current_fps = self.base_fps

        head = list(self.snake[0])
        if self.direction == pygame.K_UP: head[1] -= 20
        elif self.direction == pygame.K_DOWN: head[1] += 20
        elif self.direction == pygame.K_LEFT: head[0] -= 20
        elif self.direction == pygame.K_RIGHT: head[0] += 20

        # Task 3.4: Collision with walls or boundaries
        if head in self.snake or head in self.obstacles or \
           head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            if self.shield_active: self.shield_active = False
            else: self.game_over()

        self.snake.insert(0, head)

        # Task 3.2: Poison logic (shorten by 2)
        if head == self.poison.pos:
            if len(self.snake) <= 3: self.game_over()
            else:
                self.snake.pop(); self.snake.pop()
                self.poison = Food(self.snake, self.obstacles, True)
        # Normal food
        elif head == self.food.pos:
            if self.sound_on: self.snd_eat.play()
            self.score += 1
            self.food = Food(self.snake, self.obstacles)
            if self.score % 3 == 0:
                self.level += 1; self.base_fps += 2
                self.obstacles = generate_level_obstacles(self.level, self.snake)
            if random.random() < 0.3: self.spawn_powerup()
        # Task 3.3: Power-up pickup
        elif self.powerup and head == self.powerup.pos:
            if self.powerup_type == 'speed': self.current_fps += 10; self.effect_timer = now + 5000
            elif self.powerup_type == 'slow': self.current_fps = 5; self.effect_timer = now + 5000
            elif self.powerup_type == 'shield': self.shield_active = True
            self.powerup = None
        else: self.snake.pop()

    def game_over(self):
        save_game_session(self.player_id, self.score, self.level)
        self.state = "GAMEOVER"

    def draw_button(self, text, x, y, w, h, color, h_color, action):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, h_color if rect.collidepoint(mouse) else color, rect, border_radius=8)
        txt = pygame.font.SysFont("Arial", 22, bold=True).render(text, True, (255, 255, 255))
        self.screen.blit(txt, (x + (w - txt.get_width())//2, y + (h - txt.get_height())//2))
        if rect.collidepoint(mouse) and click[0]: pygame.time.delay(150); action()

    def run(self):
        while True:
            if self.state == "MENU": self.menu_screen()
            elif self.state == "PLAYING":
                self.clock.tick(self.current_fps)
                self.handle_input(); self.update(); self.draw_game()
            elif self.state == "SETTINGS": self.settings_screen()
            elif self.state == "LEADERBOARD": self.leaderboard_screen()
            elif self.state == "GAMEOVER": self.game_over_screen()

    def menu_screen(self):
        self.screen.fill((20, 20, 20))
        title = pygame.font.SysFont("Arial", 60, bold=True).render("SNAKE TSIS 4", True, (0, 255, 0))
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
        
        # Task 3.1 & 3.6: Name Entry
        label = pygame.font.SysFont("Arial", 25).render(f"Enter Username: {self.user_input}_", True, (255, 255, 0))
        self.screen.blit(label, (WIDTH//2 - label.get_width()//2, 160))
        
        self.draw_button("PLAY", 300, 250, 200, 50, (0, 120, 0), (0, 180, 0), self.start_play)
        self.draw_button("LEADERBOARD", 300, 320, 200, 50, (0, 0, 120), (0, 0, 180), lambda: setattr(self, 'state', 'LEADERBOARD'))
        self.draw_button("SETTINGS", 300, 390, 200, 50, (60, 60, 60), (90, 90, 90), lambda: setattr(self, 'state', 'SETTINGS'))
        self.draw_button("QUIT", 300, 460, 200, 50, (120, 0, 0), (180, 0, 0), sys.exit)
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE: self.user_input = self.user_input[:-1]
                elif len(self.user_input) < 12: self.user_input += event.unicode

    def start_play(self):
        if self.user_input:
            p_id, pb = get_or_create_player(self.user_input)
            self.reset_game(self.user_input, p_id, pb)
            self.state = "PLAYING"

    def draw_game(self):
        self.screen.fill((10, 10, 10))
        if self.show_grid: # Task 3.5 Grid
            for x in range(0, WIDTH, 20): pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, 20): pygame.draw.line(self.screen, (30, 30, 30), (0, y), (WIDTH, y))
        
        for obs in self.obstacles: self.screen.blit(self.img_wall, (obs[0], obs[1]))
        self.screen.blit(self.img_apple, (self.food.pos[0], self.food.pos[1]))
        self.screen.blit(self.img_poison, (self.poison.pos[0], self.poison.pos[1]))
        if self.powerup: # Power-up visual
            color = (255, 255, 0) if self.powerup_type == 'shield' else (0, 255, 255)
            pygame.draw.circle(self.screen, color, (self.powerup.pos[0]+10, self.powerup.pos[1]+10), 8)
        
        for i, b in enumerate(self.snake):
            if i == 0: self.screen.blit(self.img_head, (b[0], b[1]))
            else: pygame.draw.rect(self.screen, self.snake_color, (b[0], b[1], 20, 20))
            
        # UI Gameplay Info (Task 3.1 Personal Best)
        txt = pygame.font.SysFont("Arial", 20).render(f"Score: {self.score} | Lvl: {self.level} | Best: {self.personal_best}", True, (255, 255, 255))
        self.screen.blit(txt, (10, 10))
        if self.shield_active: pygame.draw.circle(self.screen, (255, 255, 255), (self.snake[0][0]+10, self.snake[0][1]+10), 12, 2)
        pygame.display.flip()

    def settings_screen(self):
        self.screen.fill((40, 40, 40))
        self.draw_button(f"GRID: {'ON' if self.show_grid else 'OFF'}", 300, 150, 200, 50, (100, 50, 0), (150, 100, 0), self.toggle_grid)
        self.draw_button(f"SOUND: {'ON' if self.sound_on else 'OFF'}", 300, 220, 200, 50, (100, 50, 0), (150, 100, 0), self.toggle_sound)
        self.draw_button("COLOR: GREEN", 200, 300, 180, 50, (0, 100, 0), (0, 150, 0), lambda: self.set_color([0, 255, 0]))
        self.draw_button("COLOR: BLUE", 420, 300, 180, 50, (0, 0, 100), (0, 0, 150), lambda: self.set_color([0, 100, 255]))
        self.draw_button("SAVE & BACK", 300, 450, 200, 50, (50, 50, 50), (80, 80, 80), self.save_and_exit)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

    def toggle_grid(self): self.show_grid = not self.show_grid
    def toggle_sound(self):
        self.sound_on = not self.sound_on
        if self.sound_on: pygame.mixer.music.play(-1)
        else: pygame.mixer.music.stop()
    def set_color(self, c): self.snake_color = c
    def save_and_exit(self): self.save_settings_to_file(); self.state = "MENU"

    def leaderboard_screen(self):
        self.screen.fill((20, 20, 20))
        data = get_leaderboard_data()
        font = pygame.font.SysFont("Courier", 18)
        header = font.render("RANK  NAME           SCORE  LVL   DATE", True, (255, 200, 0))
        self.screen.blit(header, (140, 80))
        for i, row in enumerate(data):
            entry = f"{i+1:<5} {row[0]:<14} {row[1]:<6} {row[2]:<5} {row[3].strftime('%Y-%m-%d')}"
            self.screen.blit(font.render(entry, True, (255, 255, 255)), (140, 120 + i*30))
        self.draw_button("BACK", 300, 500, 200, 40, (60, 60, 60), (90, 90, 90), lambda: setattr(self, 'state', 'MENU'))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

    def game_over_screen(self):
        self.screen.fill((50, 0, 0))
        font = pygame.font.SysFont("Arial", 50, bold=True).render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(font, (WIDTH//2 - font.get_width()//2, 120))
        info = pygame.font.SysFont("Arial", 25).render(f"Final Score: {self.score} | Lvl: {self.level} | Best: {self.personal_best}", True, (255, 255, 255))
        self.screen.blit(info, (WIDTH//2 - info.get_width()//2, 200))
        self.draw_button("RETRY", 300, 320, 200, 50, (0, 100, 0), (0, 150, 0), self.start_play)
        self.draw_button("MENU", 300, 390, 200, 50, (60, 60, 60), (90, 90, 90), lambda: setattr(self, 'state', 'MENU'))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != pygame.K_DOWN: self.direction = pygame.K_UP
                if event.key == pygame.K_DOWN and self.direction != pygame.K_UP: self.direction = pygame.K_DOWN
                if event.key == pygame.K_LEFT and self.direction != pygame.K_RIGHT: self.direction = pygame.K_LEFT
                if event.key == pygame.K_RIGHT and self.direction != pygame.K_LEFT: self.direction = pygame.K_RIGHT

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
    
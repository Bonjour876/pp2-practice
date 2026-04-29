import pygame
import random

ASSETS_PATH = r"C:\Users\tamer\OneDrive\Documents\PP2\TSIS\TSIS3\assets\\"

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load(ASSETS_PATH + "Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.shield_active = False # For shield power-up logic

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < 400:        
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(5, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load(ASSETS_PATH + "Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 360), 0)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, 360), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load(ASSETS_PATH + "Coin.png")
        self.weight = random.choice([1, 1, 1, 3, 5])
        size = 20 + (self.weight * 5)
        self.image = pygame.transform.scale(img, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, 360), -100)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > 600: self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, p_type, w, h):
        super().__init__()
        self.type = p_type # nitro, shield, repair
        # Load and scale up the image for better visibility
        img = pygame.image.load(ASSETS_PATH + f"{p_type}.png")
        self.image = pygame.transform.scale(img, (int(w * 1.8), int(h * 1.8)))
        self.rect = self.image.get_rect()
        # Random spawn within road lanes
        self.rect.center = (random.randint(60, 340), -50)
        self.spawn_time = pygame.time.get_ticks()

    def move(self, speed):
        self.rect.move_ip(0, speed)
        # Despawn if not collected within 7 seconds
        if pygame.time.get_ticks() - self.spawn_time > 7000:
            self.kill()

class Hazard(pygame.sprite.Sprite):
    def __init__(self, h_type, w, h):
        super().__init__()
        self.type = h_type # oil
        # Make hazards significantly larger to be visible obstacles
        img = pygame.image.load(ASSETS_PATH + f"{h_type}.png")
        self.image = pygame.transform.scale(img, (int(w * 2.5), int(h * 2.5)))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(60, 340), -50)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        # Remove if it goes off-screen
        if self.rect.top > 600:
            self.kill()
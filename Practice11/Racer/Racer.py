import pygame, sys
from pygame.locals import *
import random, time
 
pygame.init()
 
# Screen and timing settings
FPS = 60
FramePerSec = pygame.time.Clock()
 
# Color constants for easy access
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Window dimensions and starting stats
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 3
SCORE = 0
COIN_SCORE = 0

# Fonts for UI text
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Road background image
background = pygame.image.load(r"C:\Users\tamer\OneDrive\Documents\PP2\Practice11\Racer\images\AnimatedStreet.png")

# Setup the display surface
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
# Enemy class for oncoming traffic
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load(r"C:\Users\tamer\OneDrive\Documents\PP2\Practice11\Racer\images\Enemy.png")
        self.rect = self.image.get_rect()
        # Spawn at a random X position at the top of the screen
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0) 
 
      def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED) # Moves down based on current SPEED variable       
        if (self.rect.bottom > 600):
            SCORE += 1 # Bonus point for dodging the enemy
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

# Player car class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load(r"C:\Users\tamer\OneDrive\Documents\PP2\Practice11\Racer\images\Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520) # Starting position near the bottom

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # Left and right movement with screen border checks
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

# Coin class with variable weights and sizes
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(r"C:\Users\tamer\OneDrive\Documents\PP2\Practice11\Racer\images\Coin.png")
        self.reset()

    def reset(self):
        # Randomly choose weight: 1, 3, or 5. 1 is most common.
        self.weight = random.choice([1, 1, 1, 3, 5])
        # Scaling the image: higher weight coins appear larger on the road
        size = 20 + (self.weight * 5)
        self.image = pygame.transform.scale(self.original_image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, 5) # Coins fall at a constant speed
        if (self.rect.top > 600):
            self.reset() # Re-spawn the coin once it leaves the screen

# Create object instances
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Sprite grouping for collision detection and rendering
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Background music
pygame.mixer.music.load(r"C:\Users\tamer\OneDrive\Documents\PP2\Practice11\Racer\images\background.wav")
pygame.mixer.music.play(-1)

# MAIN GAME LOOP
while True:     
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # Draw background first
    DISPLAYSURF.blit(background, (0,0))
    
    # Render scores and coin counts to screen
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    coin_scores = font_small.render("Coins: " + str(COIN_SCORE), True, BLACK)
    DISPLAYSURF.blit(coin_scores, (SCREEN_WIDTH - 120, 10))

    # Update positions and draw all entities
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Logic for picking up coins
    collided_coin = pygame.sprite.spritecollideany(P1, coins)
    if collided_coin:
        COIN_SCORE += collided_coin.weight # Increment score by the coin's specific weight
        SPEED += 0.3 # Enemy speed increases every time we collect a coin
        collided_coin.reset()

    # Logic for crashing into enemies
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound(r"C:\Users\tamer\OneDrive\Documents\PP2\Practice11\Racer\images\crash.wav").play()
          time.sleep(0.5)
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
          pygame.display.update()
          # Clean up and exit on crash
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()         
          
    pygame.display.update()
    FramePerSec.tick(FPS)
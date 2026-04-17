import pygame # graphics engine
from ball import Ball # import ball class

pygame.init() # initialize pygame

WIDTH, HEIGHT = 800, 600 # screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # create window
pygame.display.set_caption("Moving Ball") # set title

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Create ball object at center
ball = Ball(WIDTH // 2, HEIGHT // 2, 25, RED, WIDTH, HEIGHT)

clock = pygame.time.Clock() # framerate controller
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move("up") # move up
            elif event.key == pygame.K_DOWN:
                ball.move("down") # move down
            elif event.key == pygame.K_LEFT:
                ball.move("left") # move left
            elif event.key == pygame.K_RIGHT:
                ball.move("right") # move right

    screen.fill(WHITE) # clear background
    ball.draw(screen) # render ball
    
    pygame.display.flip() # update screen
    clock.tick(60) # cap at 60 FPS

pygame.quit() # shutdown
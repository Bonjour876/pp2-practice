import pygame

class Ball:
    def __init__(self, x, y, radius, color, screen_width, screen_height):
        self.x = x # horizontal position
        self.y = y # vertical position
        self.radius = radius # ball size
        self.color = color # ball color
        self.screen_width = screen_width # boundary limit X
        self.screen_height = screen_height # boundary limit Y
        self.step = 20 # movement speed

    def move(self, direction):
        if direction == "up":
            # check top boundary
            if self.y - self.radius - self.step >= 0:
                self.y -= self.step
        elif direction == "down":
            # check bottom boundary
            if self.y + self.radius + self.step <= self.screen_height:
                self.y += self.step
        elif direction == "left":
            # check left boundary
            if self.x - self.radius - self.step >= 0:
                self.x -= self.step
        elif direction == "right":
            # check right boundary
            if self.x + self.radius + self.step <= self.screen_width:
                self.x += self.step

    def draw(self, screen):
        # render circle on screen
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
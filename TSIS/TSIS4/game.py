import pygame
import random

class GameObject:
    """Base class for items spawning on the field"""
    def __init__(self, snake_body, obstacles):
        self.pos = self.generate_safe_pos(snake_body, obstacles)

    def generate_safe_pos(self, snake_body, obstacles):
        """Task 3.4: Ensures items don't spawn on walls or the snake"""
        while True:
            x = random.randrange(0, 800, 20)
            y = random.randrange(0, 600, 20)
            if [x, y] not in snake_body and [x, y] not in obstacles:
                return [x, y]

class Food(GameObject):
    """Represents normal food or poison (Task 3.2)"""
    def __init__(self, snake_body, obstacles, is_poison=False):
        super().__init__(snake_body, obstacles)
        self.is_poison = is_poison

def generate_level_obstacles(level, snake_body):
    """Task 3.4: Spawns static walls starting from Level 3"""
    obs = []
    if level < 3: return obs
    for _ in range(level * 2):
        while True:
            wall = [random.randrange(0, 800, 20), random.randrange(0, 600, 20)]
            # Don't trap the snake's head area
            if wall not in snake_body and abs(wall[0] - snake_body[0][0]) > 60:
                obs.append(wall)
                break
    return obs
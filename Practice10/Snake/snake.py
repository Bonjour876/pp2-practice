import pygame
import random
import math

class SceneBase:
    def __init__(self):
        self.next = self
    
    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)

class SnakeScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.cell_size = 20
        # Координаты: голова [0], потом хвост
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.direction = pygame.K_RIGHT 
        self.food_pos = self.generate_food()
        self.score = 0
        self.level = 1
        self.speed = 10 
        self.game_over = False

    def generate_food(self):
        while True:
            x = random.randrange(0, 800, self.cell_size)
            y = random.randrange(0, 600, self.cell_size)
            if [x, y] not in self.snake:
                return [x, y]

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != pygame.K_DOWN:
                    self.direction = pygame.K_UP
                elif event.key == pygame.K_DOWN and self.direction != pygame.K_UP:
                    self.direction = pygame.K_DOWN
                elif event.key == pygame.K_LEFT and self.direction != pygame.K_RIGHT:
                    self.direction = pygame.K_LEFT
                elif event.key == pygame.K_RIGHT and self.direction != pygame.K_LEFT:
                    self.direction = pygame.K_RIGHT
                
                # Рестарт на R
                if self.game_over and event.key == pygame.K_r:
                    self.__init__()

    def Update(self):
        if self.game_over: return

        new_head = list(self.snake[0])
        if self.direction == pygame.K_UP:    new_head[1] -= self.cell_size
        if self.direction == pygame.K_DOWN:  new_head[1] += self.cell_size
        if self.direction == pygame.K_LEFT:  new_head[0] -= self.cell_size
        if self.direction == pygame.K_RIGHT: new_head[0] += self.cell_size

        if new_head[0] < 0 or new_head[0] >= 800 or new_head[1] < 0 or new_head[1] >= 600:
            self.game_over = True
            return

        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food_pos:
            self.score += 1
            self.food_pos = self.generate_food()
            # Уровни: каждые 3 очка ускоряемся
            if self.score % 3 == 0:
                self.level += 1
                self.speed += 2 
        else:
            self.snake.pop()

    def Render(self, screen):
        screen.fill((30, 30, 30)) # Фон
        

        pygame.draw.rect(screen, (255, 0, 0), (self.food_pos[0], self.food_pos[1], self.cell_size-1, self.cell_size-1))


        for i, block in enumerate(self.snake):
            color = (0, 255, 0) if i == 0 else (0, 180, 0)
            pygame.draw.rect(screen, color, (block[0], block[1], self.cell_size-1, self.cell_size-1))

        
        font = pygame.font.SysFont("Arial", 22)
        txt = font.render(f"Score: {self.score}  Level: {self.level}  Speed: {self.speed}", True, (255, 255, 255))
        screen.blit(txt, (10, 10))

        if self.game_over:
            msg = font.render("GAME OVER! Press R to Restart", True, (255, 50, 50))
            screen.blit(msg, (260, 280))

def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    active_scene = starting_scene

    while active_scene != None:
        current_fps = active_scene.speed if hasattr(active_scene, 'speed') else fps
        
        pressed_keys = pygame.key.get_pressed()
        filtered_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)
        
        active_scene = active_scene.next
        pygame.display.flip()
        clock.tick(current_fps) 

run_game(800, 600, 10, SnakeScene())
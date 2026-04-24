import pygame
import math

class SceneBase:
    def __init__(self):
        self.next = self
    def ProcessInput(self, events, pressed_keys): pass
    def Update(self): pass
    def Render(self, screen): pass
    def SwitchToScene(self, next_scene):
        self.next = next_scene
    def Terminate(self):
        self.SwitchToScene(None)

class PaintScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.color = (0, 0, 0)      
        self.mode = 'brush'         
        self.drawing = False        
        self.start_pos = None       
        
        self.canvas = pygame.Surface((800, 600))
        self.canvas.fill((255, 255, 255)) 

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.drawing = True
                self.start_pos = event.pos 
                
            if event.type == pygame.MOUSEBUTTONUP:
                if self.drawing and self.mode in ['rect', 'circle']:
                    self.draw_shape(self.canvas, self.start_pos, event.pos)
                self.drawing = False
                self.start_pos = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: self.color = (255, 0, 0)   # R - Red
                if event.key == pygame.K_g: self.color = (0, 255, 0)   # G - Green
                if event.key == pygame.K_b: self.color = (0, 0, 255)   # B - Blue
                if event.key == pygame.K_k: self.color = (0, 0, 0)     # K - Black
                
                if event.key == pygame.K_1: self.mode = 'brush'
                if event.key == pygame.K_2: self.mode = 'rect'
                if event.key == pygame.K_3: self.mode = 'circle'
                if event.key == pygame.K_4: self.mode = 'eraser'

    def draw_shape(self, surface, start, end, temp_color=None):
        """Функция для рисования прямоугольника и круга"""
        draw_color = temp_color if temp_color else self.color
        
        if self.mode == 'rect':
            x = min(start[0], end[0])
            y = min(start[1], end[1])
            width = abs(start[0] - end[0])
            height = abs(start[1] - end[1])
            pygame.draw.rect(surface, draw_color, (x, y, width, height), 2)
            
        elif self.mode == 'circle':
            radius = int(math.hypot(start[0] - end[0], start[1] - end[1]))
            pygame.draw.circle(surface, draw_color, start, radius, 2)

    def Update(self):
        if self.drawing and (self.mode == 'brush' or self.mode == 'eraser'):
            mouse_pos = pygame.mouse.get_pos()
            draw_color = (255, 255, 255) if self.mode == 'eraser' else self.color
            pygame.draw.circle(self.canvas, draw_color, mouse_pos, 5)

    def Render(self, screen):
        screen.blit(self.canvas, (0, 0))
        
        if self.drawing and self.mode in ['rect', 'circle'] and self.start_pos:
            self.draw_shape(screen, self.start_pos, pygame.mouse.get_pos(), (200, 200, 200))
        
        font = pygame.font.SysFont("Verdana", 16)
        
        color_name = "Red" if self.color == (255, 0, 0) else "Green" if self.color == (0, 255, 0) else "Blue" if self.color == (0, 0, 255) else "Black"
        menu_text = f"MODE: {self.mode.upper()} | COLOR: {color_name} | KEYS: [1-4] Tools, [R,G,B,K] Colors"
        
        pygame.draw.rect(screen, (240, 240, 240), (0, 0, 800, 30))
        text_surf = font.render(menu_text, True, (50, 50, 50))
        screen.blit(text_surf, (10, 5))

def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("My Paint Project")
    clock = pygame.time.Clock()
    active_scene = starting_scene

    while active_scene != None:
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
        clock.tick(fps)

run_game(800, 600, 60, PaintScene())
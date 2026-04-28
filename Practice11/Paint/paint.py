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
        
        # Main drawing surface
        self.canvas = pygame.Surface((800, 600))
        self.canvas.fill((255, 255, 255)) 

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.drawing = True
                self.start_pos = event.pos 
                
            if event.type == pygame.MOUSEBUTTONUP:
                if self.drawing and self.mode not in ['brush', 'eraser']:
                    self.draw_shape(self.canvas, self.start_pos, event.pos)
                self.drawing = False
                self.start_pos = None

            if event.type == pygame.KEYDOWN:
                # Color Selection
                if event.key == pygame.K_r: self.color = (255, 0, 0)
                if event.key == pygame.K_g: self.color = (0, 255, 0)
                if event.key == pygame.K_b: self.color = (0, 0, 255)
                if event.key == pygame.K_k: self.color = (0, 0, 0)
                
                # Tool Selection
                if event.key == pygame.K_1: self.mode = 'brush'
                if event.key == pygame.K_2: self.mode = 'rect'
                if event.key == pygame.K_3: self.mode = 'circle'
                if event.key == pygame.K_4: self.mode = 'eraser'
                if event.key == pygame.K_5: self.mode = 'square'
                if event.key == pygame.K_6: self.mode = 'right_triangle'
                if event.key == pygame.K_7: self.mode = 'equilateral_triangle'
                if event.key == pygame.K_8: self.mode = 'rhombus'

    def draw_shape(self, surface, start, end, temp_color=None):
        """Logic for drawing all geometric shapes"""
        draw_color = temp_color if temp_color else self.color
        x1, y1 = start
        x2, y2 = end
        
        if self.mode == 'rect':
            pygame.draw.rect(surface, draw_color, (min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2)), 2)
            
        elif self.mode == 'circle':
            radius = int(math.hypot(x1 - x2, y1 - y2))
            pygame.draw.circle(surface, draw_color, start, radius, 2)

        elif self.mode == 'square':
            # Side length is the maximum of width or height to keep it a square
            side = max(abs(x1 - x2), abs(y1 - y2))
            # Adjust coordinates based on direction of drag
            new_x = x1 if x2 > x1 else x1 - side
            new_y = y1 if y2 > y1 else y1 - side
            pygame.draw.rect(surface, draw_color, (new_x, new_y, side, side), 2)

        elif self.mode == 'right_triangle':
            # Points: Start (top), Bottom-Start (below start), End (tip)
            points = [start, (x1, y2), end]
            pygame.draw.polygon(surface, draw_color, points, 2)

        elif self.mode == 'equilateral_triangle':
            # Simple math to find the 3rd point of a triangle
            height = (y2 - y1)
            points = [start, (x1 - height/1.5, y2), (x1 + height/1.5, y2)]
            pygame.draw.polygon(surface, draw_color, points, 2)

        elif self.mode == 'rhombus':
            # Midpoints of the bounding box created by mouse drag
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            points = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
            pygame.draw.polygon(surface, draw_color, points, 2)

    def Update(self):
        # Continuous drawing for brush and eraser
        if self.drawing and (self.mode == 'brush' or self.mode == 'eraser'):
            mouse_pos = pygame.mouse.get_pos()
            draw_color = (255, 255, 255) if self.mode == 'eraser' else self.color
            pygame.draw.circle(self.canvas, draw_color, mouse_pos, 5)

    def Render(self, screen):
        screen.blit(self.canvas, (0, 0))
        
        # Preview shape while dragging
        if self.drawing and self.mode not in ['brush', 'eraser'] and self.start_pos:
            self.draw_shape(screen, self.start_pos, pygame.mouse.get_pos(), (200, 200, 200))
        
        # Simple HUD / Menu
        font = pygame.font.SysFont("Verdana", 14)
        menu_text = f"MODE: {self.mode.upper()} | 1-8: Tools | R,G,B,K: Colors"
        pygame.draw.rect(screen, (240, 240, 240), (0, 0, 800, 30))
        text_surf = font.render(menu_text, True, (50, 50, 50))
        screen.blit(text_surf, (10, 5))

def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Paint Pro")
    clock = pygame.time.Clock()
    active_scene = starting_scene

    while active_scene != None:
        filtered_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT: active_scene.Terminate()
            else: filtered_events.append(event)
        
        active_scene.ProcessInput(filtered_events, pygame.key.get_pressed())
        active_scene.Update()
        active_scene.Render(screen)
        
        active_scene = active_scene.next
        pygame.display.flip()
        clock.tick(fps)

run_game(800, 600, 60, PaintScene())
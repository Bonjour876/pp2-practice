import pygame
import os
from datetime import datetime
from tools import flood_fill, draw_custom_shape

class PaintApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("Pygame Paint Pro")
        
        self.canvas = pygame.Surface((1000, 700))
        self.canvas.fill((255, 255, 255))
        
        self.clock = pygame.time.Clock()
        self.color = (0, 0, 0)
        self.thickness = 2
        self.mode = 'pencil'
        self.drawing = False
        self.start_pos = None
        self.last_pos = None

        self.text_active = False
        self.text_content = ""
        self.text_pos = (0, 0)
        self.font = pygame.font.SysFont("Arial", 22)
        self.ui_font = pygame.font.SysFont("Verdana", 10, bold=True)

        # Asset path
        self.assets_path = r"C:\Users\tamer\OneDrive\Documents\PP2\TSIS\TSIS2\assets"
        
        # Tool configuration with FIXED KEYS
        self.tool_config = [
            {'name': 'pencil', 'key': 'P'}, 
            {'name': 'line',   'key': 'L'},
            {'name': 'rect',   'key': 'M'}, # Changed from R to M
            {'name': 'circle', 'key': 'C'},
            {'name': 'fill',   'key': 'F'},
            {'name': 'eraser', 'key': 'E'},
            {'name': 'text',   'key': 'T'}
        ]

        self.color_config = [
            {'color': (0, 0, 0),   'key': 'K'}, 
            {'color': (255, 0, 0), 'key': 'R'}, # Red stays R
            {'color': (0, 255, 0), 'key': 'G'}, 
            {'color': (0, 0, 255), 'key': 'B'}
        ]
        
        self.icons = {}
        self.load_resources()

    def load_resources(self):
        for tool in self.tool_config:
            name = tool['name']
            path = os.path.join(self.assets_path, f"{name}.png")
            try:
                img = pygame.image.load(path).convert_alpha()
                self.icons[name] = pygame.transform.scale(img, (30, 30))
            except:
                print(f"Resource missing: {name}.png")

    def save_snapshot(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        pygame.image.save(self.canvas, f"capture_{ts}.png")

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.text_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        surf = self.font.render(self.text_content, True, self.color)
                        self.canvas.blit(surf, self.text_pos)
                        self.text_active = False
                    elif event.key == pygame.K_ESCAPE:
                        self.text_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.text_content = self.text_content[:-1]
                    else:
                        self.text_content += event.unicode
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.mode == 'fill':
                    flood_fill(self.canvas, event.pos[0], event.pos[1], self.color)
                elif self.mode == 'text':
                    self.text_active, self.text_pos, self.text_content = True, event.pos, ""
                else:
                    self.drawing, self.start_pos, self.last_pos = True, event.pos, event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if self.drawing and self.mode not in ['pencil', 'eraser']:
                    draw_custom_shape(self.canvas, self.mode, self.start_pos, event.pos, self.color, self.thickness)
                self.drawing = False

            if event.type == pygame.KEYDOWN:
                # Thickness
                if event.key == pygame.K_1: self.thickness = 2
                if event.key == pygame.K_2: self.thickness = 5
                if event.key == pygame.K_3: self.thickness = 10
                
                # Colors (R, G, B, K)
                if event.key == pygame.K_r: self.color = (255, 0, 0)
                if event.key == pygame.K_g: self.color = (0, 255, 0)
                if event.key == pygame.K_b: self.color = (0, 0, 255)
                if event.key == pygame.K_k: self.color = (0, 0, 0)

                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    self.save_snapshot()

                # Tools mapping (FIXED)
                tools = {
                    pygame.K_p: 'pencil', 
                    pygame.K_l: 'line', 
                    pygame.K_m: 'rect',    # Rectangle -> M
                    pygame.K_c: 'circle', 
                    pygame.K_f: 'fill', 
                    pygame.K_e: 'eraser',
                    pygame.K_t: 'text', 
                    pygame.K_q: 'square',  # Square -> Q
                    pygame.K_h: 'rhombus'
                }
                if event.key in tools: self.mode = tools[event.key]
        return True

    def update_frame(self):
        if self.drawing and (self.mode == 'pencil' or self.mode == 'eraser'):
            cur = pygame.mouse.get_pos()
            col = (255, 255, 255) if self.mode == 'eraser' else self.color
            pygame.draw.line(self.canvas, col, self.last_pos, cur, self.thickness)
            self.last_pos = cur

    def render_ui(self):
        pygame.draw.rect(self.screen, (240, 240, 240), (0, 0, 1000, 65))
        pygame.draw.line(self.screen, (150, 150, 150), (0, 65), (1000, 65), 1)
        
        for i, tool in enumerate(self.tool_config):
            x = 20 + i * 60
            if self.mode == tool['name']:
                pygame.draw.rect(self.screen, (210, 210, 255), (x-5, 5, 45, 55), 0, 5)
            if tool['name'] in self.icons:
                self.screen.blit(self.icons[tool['name']], (x, 22))
            self.screen.blit(self.ui_font.render(f"[{tool['key']}]", True, (80, 80, 80)), (x + 8, 8))

        for i, c_data in enumerate(self.color_config):
            x = 500 + i * 50
            if self.color == c_data['color']:
                pygame.draw.rect(self.screen, (0, 0, 0), (x-2, 20-2, 34, 34), 1)
            pygame.draw.rect(self.screen, c_data['color'], (x, 20, 30, 30))
            self.screen.blit(self.ui_font.render(f"[{c_data['key']}]", True, (50, 50, 50)), (x + 8, 5))

    def run(self):
        while self.handle_input():
            self.update_frame()
            self.screen.blit(self.canvas, (0, 0))
            if self.drawing and self.mode not in ['pencil', 'eraser', 'fill']:
                draw_custom_shape(self.screen, self.mode, self.start_pos, pygame.mouse.get_pos(), (180, 180, 180), self.thickness)
            if self.text_active:
                self.screen.blit(self.font.render(self.text_content + "|", True, self.color), self.text_pos)
            self.render_ui()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    PaintApp().run()
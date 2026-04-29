import pygame
import math

def get_distance(p1, p2):
    """Calculate Euclidean distance for circles and geometry"""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def flood_fill(surface, x, y, new_color):
    """Non-recursive stack-based flood fill algorithm"""
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    
    pixels = [(x, y)]
    w, h = surface.get_size()
    
    while pixels:
        cx, cy = pixels.pop()
        if surface.get_at((cx, cy)) != target_color:
            continue
        
        surface.set_at((cx, cy), new_color)
        
        # Checking 4-connectivity neighbors
        if cx > 0: pixels.append((cx - 1, cy))
        if cx < w - 1: pixels.append((cx + 1, cy))
        if cy > 0: pixels.append((cx, cy - 1))
        if cy < h - 1: pixels.append((cx, cy + 1))

def draw_custom_shape(surface, mode, start, end, color, width):
    """Drawing engine for primitive and custom shapes"""
    x1, y1 = start
    x2, y2 = end
    
    if mode == 'line':
        pygame.draw.line(surface, color, start, end, width)
    elif mode == 'rect':
        pygame.draw.rect(surface, color, (min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2)), width)
    elif mode == 'circle':
        rad = int(get_distance(start, end))
        pygame.draw.circle(surface, color, start, rad, width)
    elif mode == 'square':
        side = max(abs(x1 - x2), abs(y1 - y2))
        nx = x1 if x2 > x1 else x1 - side
        ny = y1 if y2 > y1 else y1 - side
        pygame.draw.rect(surface, color, (nx, ny, side, side), width)
    elif mode == 'right_triangle':
        pygame.draw.polygon(surface, color, [start, (x1, y2), end], width)
    elif mode == 'equilateral_triangle':
        h = y2 - y1
        pygame.draw.polygon(surface, color, [start, (x1 - h/1.5, y2), (x1 + h/1.5, y2)], width)
    elif mode == 'rhombus':
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        pygame.draw.polygon(surface, color, [(mx, y1), (x2, my), (mx, y2), (x1, my)], width)
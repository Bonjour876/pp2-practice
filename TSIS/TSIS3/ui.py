import pygame

# Helper function to draw buttons and check for clicks
def draw_button(screen, text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    rect = pygame.Rect(x, y, w, h)
    # Change color on hover
    current_color = hover_color if rect.collidepoint(mouse) else color
    
    pygame.draw.rect(screen, current_color, rect)
    font = pygame.font.SysFont("Verdana", 20)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    
    # Return True if clicked
    return rect.collidepoint(mouse) and click[0] == 1

def draw_text(screen, text, size, x, y, color=(0,0,0)):
    font = pygame.font.SysFont("Verdana", size)
    text_surf = font.render(text, True, color)
    screen.blit(text_surf, (x, y))
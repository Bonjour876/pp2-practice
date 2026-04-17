import pygame
from player import MusicPlayer

pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player Pro")

DARK_BLUE = (10, 20, 40)
LIGHT_BLUE = (30, 60, 120)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
GRAY = (60, 60, 80)

font_large = pygame.font.SysFont("Verdana", 32, bold=True)
font_small = pygame.font.SysFont("Verdana", 18)

tracks = [
    r"C:\Users\tamer\OneDrive\Documents\PP2\Practice9\music_player\music\WhiteStripes_Seven_nation_army.mp3",
    r"C:\Users\tamer\OneDrive\Documents\PP2\Practice9\music_player\music\KentJones_Dontmind.mp3"
]

player = MusicPlayer(tracks)
clock = pygame.time.Clock()

running = True
while running:
    
    for i in range(HEIGHT):
        color = [DARK_BLUE[j] + (LIGHT_BLUE[j] - DARK_BLUE[j]) * i // HEIGHT for j in range(3)]
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: player.play()
            elif event.key == pygame.K_s: player.stop()
            elif event.key == pygame.K_n: player.next_track()
            elif event.key == pygame.K_b: player.prev_track()
            elif event.key == pygame.K_q: running = False

    
    name_surf = font_large.render(player.get_current_name(), True, WHITE)
    screen.blit(name_surf, (WIDTH // 2 - name_surf.get_width() // 2, 120))

    
    bar_width, bar_height = 500, 10
    bar_x, bar_y = (WIDTH - bar_width) // 2, 250
    
    
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height), border_radius=5)
    
    progress = player.get_progress()
    pygame.draw.rect(screen, CYAN, (bar_x, bar_y, int(bar_width * progress), bar_height), border_radius=5)
    
    status_text = "PLAYING" if player.is_playing else "STOPPED"
    status_surf = font_small.render(status_text, True, CYAN if player.is_playing else WHITE)
    screen.blit(status_surf, (WIDTH // 2 - status_surf.get_width() // 2, 200))


    hint = font_small.render("P: Play  |  S: Stop  |  N: Next  |  B: Back  |  Q: Quit", True, (180, 180, 180))
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 420))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
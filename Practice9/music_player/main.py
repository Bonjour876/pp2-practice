import pygame # graphics engine
from player import MusicPlayer # logic import

pygame.init() # initialize pygame
WIDTH, HEIGHT = 800, 500 # window size
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # create window
pygame.display.set_caption("Music Player Pro") # window title

# Color Palette
DARK_BLUE = (10, 20, 40)
LIGHT_BLUE = (30, 60, 120)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
GRAY = (60, 60, 80)

# UI Fonts
font_large = pygame.font.SysFont("Verdana", 32, bold=True)
font_small = pygame.font.SysFont("Verdana", 18)

# Music file list
tracks = [
    r"C:\Users\tamer\OneDrive\Documents\PP2\Practice9\music_player\music\WhiteStripes_Seven_nation_army.mp3",
    r"C:\Users\tamer\OneDrive\Documents\PP2\Practice9\music_player\music\KentJones_Dontmind.mp3"
]

player = MusicPlayer(tracks) # initialize player logic
clock = pygame.time.Clock() # framerate controller

running = True
while running:
    # Draw background gradient
    for i in range(HEIGHT):
        color = [DARK_BLUE[j] + (LIGHT_BLUE[j] - DARK_BLUE[j]) * i // HEIGHT for j in range(3)]
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: player.play() # play/pause
            elif event.key == pygame.K_s: player.stop() # stop
            elif event.key == pygame.K_n: player.next_track() # skip forward
            elif event.key == pygame.K_b: player.prev_track() # skip back
            elif event.key == pygame.K_q: running = False # exit

    # UI: Header label
    info_label = font_small.render("NOW PLAYING:", True, (150, 150, 150))
    screen.blit(info_label, (WIDTH // 2 - info_label.get_width() // 2, 80))

    # UI: Track name formatting
    clean_name = player.get_current_name().replace(".mp3", "").replace("_", " ")
    name_surf = font_large.render(clean_name, True, WHITE)
    screen.blit(name_surf, (WIDTH // 2 - name_surf.get_width() // 2, 120))

    # UI: Playback status
    status_text = "STATUS: PLAYING" if player.is_playing else "STATUS: PAUSED"
    status_surf = font_small.render(status_text, True, CYAN if player.is_playing else WHITE)
    screen.blit(status_surf, (WIDTH // 2 - status_surf.get_width() // 2, 200))

    # UI: Progress bar background
    bar_width, bar_height = 500, 10
    bar_x, bar_y = (WIDTH - bar_width) // 2, 250
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height), border_radius=5)
    
    # UI: Dynamic progress fill
    progress = player.get_progress()
    pygame.draw.rect(screen, CYAN, (bar_x, bar_y, int(bar_width * progress), bar_height), border_radius=5)

    # UI: Control hints
    hint = font_small.render("P: Play  |  S: Stop  |  N: Next  |  B: Back  |  Q: Quit", True, (180, 180, 180))
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 420))

    pygame.display.flip() # update display
    clock.tick(30) # cap at 30 FPS

pygame
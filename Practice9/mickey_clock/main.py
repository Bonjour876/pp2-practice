import pygame
from clock import get_time, rotate_center

pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

bg_img = pygame.image.load(r"C:\Users\tamer\OneDrive\Documents\PP2\Practice9\mickey_clock\images\clock.png").convert_alpha()
hand_min_img = pygame.image.load(r"C:\Users\tamer\OneDrive\Documents\PP2\Practice9\mickey_clock\images\Hour.png").convert_alpha()
hand_sec_img = pygame.image.load(r"C:\Users\tamer\OneDrive\Documents\PP2\Practice9\mickey_clock\images\mickey.png").convert_alpha()

bg_sc = 1.5
min_sc = 0.3
sec_sc = 0.3

bg_img = pygame.transform.scale(bg_img, (int(bg_img.get_width() * bg_sc), int(bg_img.get_height() * bg_sc)))
hand_min_img = pygame.transform.scale(hand_min_img, (int(hand_min_img.get_width() * min_sc), int(hand_min_img.get_height() * min_sc)))
hand_sec_img = pygame.transform.scale(hand_sec_img, (int(hand_sec_img.get_width() * sec_sc), int(hand_sec_img.get_height() * sec_sc)))

CENTER = (WIDTH // 2, HEIGHT // 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sec_angle, min_angle = get_time()

    screen.fill((255, 255, 255))

    bg_rect = bg_img.get_rect(center=CENTER)
    screen.blit(bg_img, bg_rect)

    img_min, rect_min = rotate_center(hand_min_img, min_angle, CENTER[0], CENTER[1])
    screen.blit(img_min, rect_min)

    img_sec, rect_sec = rotate_center(hand_sec_img, sec_angle, CENTER[0], CENTER[1])
    screen.blit(img_sec, rect_sec)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
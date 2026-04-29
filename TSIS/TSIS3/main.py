import pygame, sys, time, random
from pygame.locals import *
from persistence import load_settings, save_settings, add_to_leaderboard, load_leaderboard
from racer import Player, Enemy, Coin, PowerUp, Hazard
from ui import draw_button, draw_text

pygame.init()
pygame.mixer.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TSIS3 Racer Pro")
FPS = 60
clock = pygame.time.Clock()

ASSETS = r"C:\Users\tamer\OneDrive\Documents\PP2\TSIS\TSIS3\assets\\"
try:
    background = pygame.image.load(ASSETS + "AnimatedStreet.png")
except:
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((50, 50, 50))

settings = load_settings()
save_settings(settings)
current_user = ""
states = {"MENU": 0, "GAME": 1, "SETTINGS": 2, "LEADERBOARD": 3, "GAMEOVER": 4}
current_state = states["MENU"]

def start_bg_music():
    if settings.get("sound"):
        try:
            pygame.mixer.music.load(ASSETS + "background.wav")
            pygame.mixer.music.play(-1)
        except:
            pass
    else:
        pygame.mixer.music.stop()

start_bg_music()

def get_username_screen():
    input_rect = pygame.Rect(100, 250, 200, 45)
    user_text = ""
    while True:
        DISPLAYSURF.fill((30, 30, 30))
        draw_text(DISPLAYSURF, "ENTER YOUR NAME:", 25, 80, 180, (255, 255, 255))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN and len(user_text) > 0:
                    return user_text
                elif event.key == K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if len(user_text) < 10:
                        user_text += event.unicode
        pygame.draw.rect(DISPLAYSURF, (255, 255, 255), input_rect, 2)
        draw_text(DISPLAYSURF, user_text, 25, input_rect.x + 10, input_rect.y + 7, (255, 255, 0))
        pygame.display.update()
        clock.tick(FPS)

def play_game():
    global current_state, settings, current_user
    diff = settings.get("difficulty", "Medium")
    speed = 3 if diff == "Easy" else (8 if diff == "Hard" else 5)
    score, distance, bg_y = 0, 0, 0
    active_powerup = None
    powerup_timer = 0
    player = Player()
    enemies = pygame.sprite.Group([Enemy()])
    coins, powerups, hazards = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
    all_sprites = pygame.sprite.Group([player, enemies.sprites()[0]])
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, 1000)
    
    while True:
        bg_y += speed
        if bg_y >= SCREEN_HEIGHT: bg_y = 0
        DISPLAYSURF.blit(background, (0, bg_y))
        DISPLAYSURF.blit(background, (0, bg_y - SCREEN_HEIGHT))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == SPAWN_EVENT:
                c = random.random()
                if c < 0.5:
                    item = Coin(); coins.add(item)
                elif c < 0.8:
                    pt = random.choice(['nitro', 'shield', 'repair'])
                    item = PowerUp(pt, 30, 20 if pt != 'repair' else 45)
                    powerups.add(item)
                else:
                    item = Hazard('oil', 50, 33); hazards.add(item)
                all_sprites.add(item)

        player.move()
        distance += speed / 10
        for s in all_sprites:
            if s != player: s.move(speed)

        if pygame.sprite.spritecollideany(player, coins):
            score += 20; speed += 0.05
            pygame.sprite.spritecollideany(player, coins).kill()
            
        p_hit = pygame.sprite.spritecollideany(player, powerups)
        if p_hit:
            if p_hit.type == 'repair': score += 100
            else:
                active_powerup = p_hit.type
                powerup_timer = time.time() + 5
                if p_hit.type == 'nitro': speed += settings.get("speed_boost", 5)
                if p_hit.type == 'shield': player.shield_active = True
            p_hit.kill()

        h_hit = pygame.sprite.spritecollideany(player, hazards)
        e_hit = pygame.sprite.spritecollideany(player, enemies)
        if h_hit or e_hit:
            if player.shield_active:
                player.shield_active = False; active_powerup = None
                if h_hit: h_hit.kill()
                if e_hit: e_hit.rect.top = -100
            else:
                if settings.get("sound"):
                    try: pygame.mixer.Sound(ASSETS + "crash.wav").play()
                    except: pass
                add_to_leaderboard(current_user, score, distance)
                return score, int(distance)

        for s in all_sprites: DISPLAYSURF.blit(s.image, s.rect)
        draw_text(DISPLAYSURF, f"Score: {score}  Dist: {int(distance)}m", 18, 10, 10, (255,255,255))
        if active_powerup:
            draw_text(DISPLAYSURF, f"BUFF: {active_powerup.upper()}", 18, 250, 10, (0,255,0))
        pygame.display.update()
        clock.tick(FPS)

final_score, final_dist = 0, 0
while True:
    DISPLAYSURF.fill((40, 40, 40))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); sys.exit()

    if current_state == states["MENU"]:
        draw_text(DISPLAYSURF, "RACER PRO ARCADE", 35, 45, 100, (255, 255, 255))
        if draw_button(DISPLAYSURF, "PLAY", 100, 200, 200, 50, (50, 150, 50), (80, 200, 80)):
            pygame.time.delay(200)
            current_user = get_username_screen()
            final_score, final_dist = play_game()
            current_state = states["GAMEOVER"]
        if draw_button(DISPLAYSURF, "LEADERBOARD", 100, 270, 200, 50, (50, 50, 150), (80, 80, 200)):
            pygame.time.delay(200)
            current_state = states["LEADERBOARD"]
        if draw_button(DISPLAYSURF, "SETTINGS", 100, 340, 200, 50, (100, 100, 100), (150, 150, 150)):
            pygame.time.delay(200)
            current_state = states["SETTINGS"]
        if draw_button(DISPLAYSURF, "QUIT", 100, 410, 200, 50, (150, 50, 50), (200, 80, 80)):
            pygame.quit(); sys.exit()

    elif current_state == states["SETTINGS"]:
        draw_text(DISPLAYSURF, "SETTINGS", 30, 130, 50, (255, 255, 255))
        sound_txt = "SOUND: ON" if settings["sound"] else "SOUND: OFF"
        if draw_button(DISPLAYSURF, sound_txt, 100, 150, 200, 50, (70, 70, 70), (100, 100, 100)):
            settings["sound"] = not settings["sound"]
            save_settings(settings)
            start_bg_music()
            pygame.time.delay(200)
        if draw_button(DISPLAYSURF, f"DIFF: {settings['difficulty']}", 100, 220, 200, 50, (70, 70, 70), (100, 100, 100)):
            modes = ["Easy", "Medium", "Hard"]
            settings["difficulty"] = modes[(modes.index(settings["difficulty"]) + 1) % 3]
            save_settings(settings); pygame.time.delay(200)
        if draw_button(DISPLAYSURF, "BACK", 100, 400, 200, 50, (50, 50, 50), (80, 80, 80)):
            pygame.time.delay(250)
            current_state = states["MENU"]
            pygame.event.clear()

    elif current_state == states["GAMEOVER"]:
        draw_text(DISPLAYSURF, "GAME OVER", 40, 85, 100, (255, 50, 50))
        draw_text(DISPLAYSURF, f"Score: {final_score}", 25, 130, 200, (255, 255, 255))
        if draw_button(DISPLAYSURF, "RETRY", 100, 300, 200, 50, (50, 150, 50), (80, 200, 80)):
            final_score, final_dist = play_game()
        if draw_button(DISPLAYSURF, "MENU", 100, 370, 200, 50, (100, 100, 100), (150, 150, 150)):
            pygame.time.delay(200)
            current_state = states["MENU"]

    elif current_state == states["LEADERBOARD"]:
        draw_text(DISPLAYSURF, "TOP 10 SCORES", 25, 100, 50, (255, 255, 0))
        lb = load_leaderboard()
        for i, entry in enumerate(lb):
            draw_text(DISPLAYSURF, f"{i+1}. {entry['name']}: {entry['score']}", 18, 50, 120 + (i*35), (255, 255, 255))
        if draw_button(DISPLAYSURF, "BACK", 100, 500, 200, 40, (70, 70, 70), (100, 100, 100)):
            pygame.time.delay(200)
            current_state = states["MENU"]

    pygame.display.update()
    clock.tick(FPS)
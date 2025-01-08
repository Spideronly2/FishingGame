import pygame
import random
import sys

# Inicialização do pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fishing Game")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)

# Configurações de áudio
pygame.mixer.init()
background_music = "background_music.mp3"
catch_sound = pygame.mixer.Sound("catch_sound.wav")
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)

# Velocidade e dimensões
boat_speed = 4
tile_size = 40

# Configurações iniciais
game_running = False
menu_active = True
options_active = False
fullscreen = False
volume_music = 1.0
volume_effects = 1.0
pygame.mixer.music.set_volume(volume_music)
catch_sound.set_volume(volume_effects)

# Elementos do jogo
boat = {"x": SCREEN_WIDTH / 2, "y": 50, "width": tile_size * 2, "height": tile_size, "color": BROWN}
hook = {"x": boat["x"] + tile_size, "y": boat["y"] + 30, "width": 5, "height": 10, "color": BLACK, "is_catching": False}
fish = {"x": random.randint(50, SCREEN_WIDTH - 50), "y": random.randint(200, SCREEN_HEIGHT - 50), "width": 20, "height": 10, "color": ORANGE, "caught": False, "dx": 2, "dy": 2}
score = 0
time_left = 30

clock = pygame.time.Clock()

# Fontes
default_font = pygame.font.Font(None, 36)

def draw_text(surface, text, x, y, color=BLACK, center=False):
    text_obj = default_font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def draw_menu():
    screen.fill(WHITE)
    draw_text(screen, "Fishing Game", SCREEN_WIDTH // 2, 150, color=BLACK, center=True)
    draw_text(screen, "[J] Play", SCREEN_WIDTH // 2, 250, color=BLACK, center=True)
    draw_text(screen, "[O] Options", SCREEN_WIDTH // 2, 300, color=BLACK, center=True)
    draw_text(screen, "[Q] Quit", SCREEN_WIDTH // 2, 350, color=BLACK, center=True)
    pygame.display.flip()

def draw_options():
    screen.fill(WHITE)
    draw_text(screen, "Options", SCREEN_WIDTH // 2, 100, color=BLACK, center=True)
    draw_text(screen, f"Volume Music: {int(volume_music * 100)}", SCREEN_WIDTH // 2, 200, color=BLACK, center=True)
    draw_text(screen, f"Volume Effects: {int(volume_effects * 100)}", SCREEN_WIDTH // 2, 250, color=BLACK, center=True)
    draw_text(screen, "[F] Toggle Fullscreen", SCREEN_WIDTH // 2, 300, color=BLACK, center=True)
    draw_text(screen, "[M] Back to Menu", SCREEN_WIDTH // 2, 350, color=BLACK, center=True)
    pygame.display.flip()

def draw_game():
    screen.fill(BLUE)

    # Desenha o barco
    pygame.draw.rect(screen, boat["color"], (boat["x"], boat["y"], boat["width"], boat["height"]))

    # Desenha a linha
    pygame.draw.line(screen, WHITE, (boat["x"] + tile_size, boat["y"] + boat["height"]), (hook["x"] + hook["width"] // 2, hook["y"]), 2)

    # Desenha o anzol
    pygame.draw.rect(screen, hook["color"], (hook["x"], hook["y"], hook["width"], hook["height"]))

    # Desenha os peixes
    if not fish["caught"]:
        pygame.draw.rect(screen, fish["color"], (fish["x"], fish["y"], fish["width"], fish["height"]))

    # Exibe o score e tempo
    draw_text(screen, f"Score: {score}", 10, 10, WHITE)
    draw_text(screen, f"Time Left: {int(time_left)}", 10, 40, WHITE)

    pygame.display.flip()

def handle_menu_events(event):
    global menu_active, options_active, game_running
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_j:
            menu_active = False
            game_running = True
        elif event.key == pygame.K_o:
            menu_active = False
            options_active = True
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()

def handle_options_events(event):
    global menu_active, options_active, volume_music, volume_effects, fullscreen
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_f:
            fullscreen = not fullscreen
            if fullscreen:
                pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
            else:
                pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        elif event.key == pygame.K_m:
            options_active = False
            menu_active = True
        elif event.key == pygame.K_UP:
            volume_music = min(1.0, volume_music + 0.1)
            pygame.mixer.music.set_volume(volume_music)
        elif event.key == pygame.K_DOWN:
            volume_music = max(0.0, volume_music - 0.1)
            pygame.mixer.music.set_volume(volume_music)
        elif event.key == pygame.K_LEFT:
            volume_effects = max(0.0, volume_effects - 0.1)
            catch_sound.set_volume(volume_effects)
        elif event.key == pygame.K_RIGHT:
            volume_effects = min(1.0, volume_effects + 0.1)
            catch_sound.set_volume(volume_effects)

def update_game():
    global score, time_left, fish

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and boat["x"] > 0:
        boat["x"] -= boat_speed
        hook["x"] -= boat_speed
    if keys[pygame.K_RIGHT] and boat["x"] < SCREEN_WIDTH - boat["width"]:
        boat["x"] += boat_speed
        hook["x"] += boat_speed
    if keys[pygame.K_DOWN]:
        hook["is_catching"] = True
    else:
        hook["is_catching"] = False

    if hook["is_catching"] and hook["y"] < SCREEN_HEIGHT:
        hook["y"] += 5
    elif not hook["is_catching"] and hook["y"] > boat["y"] + boat["height"]:
        hook["y"] -= 5

    if (hook["x"] < fish["x"] + fish["width"] and
        hook["x"] + hook["width"] > fish["x"] and
        hook["y"] < fish["y"] + fish["height"] and
        hook["y"] + hook["height"] > fish["y"]):
        fish["caught"] = True
        score += 1
        time_left += 0.2
        catch_sound.play()
        fish = {"x": random.randint(50, SCREEN_WIDTH - 50), "y": random.randint(200, SCREEN_HEIGHT - 50), "width": 20, "height": 10, "color": ORANGE, "caught": False, "dx": random.choice([-2, 2]), "dy": random.choice([-2, 2])}

    fish["x"] += fish["dx"]
    fish["y"] += fish["dy"]

    if fish["x"] <= 0 or fish["x"] >= SCREEN_WIDTH - fish["width"]:
        fish["dx"] *= -1
    if fish["y"] <= 200 or fish["y"] >= SCREEN_HEIGHT - fish["height"]:
        fish["dy"] *= -1


def main():
    global menu_active, options_active, game_running, time_left

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if menu_active:
                handle_menu_events(event)
            elif options_active:
                handle_options_events(event)

        if menu_active:
            draw_menu()
        elif options_active:
            draw_options()
        elif game_running:
            time_left -= clock.get_time() / 1000
            if time_left <= 0:
                game_running = False
                menu_active = True

            update_game()
            draw_game()

        clock.tick(60)

if __name__ == "__main__":
    main()

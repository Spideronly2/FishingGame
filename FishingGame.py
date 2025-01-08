import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60
TILE_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

# Load ocean background image
try:
    ocean_bg = pygame.image.load("background_image.png")  # Substitua pelo nome da sua imagem de fundo
    ocean_bg = pygame.transform.scale(ocean_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
except FileNotFoundError:
    print("Aviso: Imagem 'background_image.png' não encontrada! O fundo será preto.")
    ocean_bg = None

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Art Fishing Game")
clock = pygame.time.Clock()

# Boat and Hook
boat = {
    "x": SCREEN_WIDTH // 2 - TILE_SIZE,
    "y": 50,
    "width": TILE_SIZE * 2,
    "height": TILE_SIZE,
    "hook_x": SCREEN_WIDTH // 2,
    "hook_y": 80
}
hook = {
    "x": boat["hook_x"],
    "y": boat["hook_y"],
    "width": TILE_SIZE // 2,
    "height": TILE_SIZE,
    "is_catching": False
}

# Fish
fish = {
    "x": random.randint(0, SCREEN_WIDTH - TILE_SIZE),
    "y": random.randint(200, SCREEN_HEIGHT - TILE_SIZE),
    "width": TILE_SIZE,
    "height": TILE_SIZE // 2,
    "caught": False
}

# Score and Time
score = 0
time_left = 60  # seconds
font = pygame.font.Font(None, 36)
game_over = False

# Functions
def draw_boat():
    pygame.draw.rect(screen, (139, 69, 19), (boat["x"], boat["y"], boat["width"], boat["height"]))
    pygame.draw.rect(screen, BLACK, (hook["x"], hook["y"], hook["width"], hook["height"]))


def draw_fish():
    if not fish["caught"]:
        pygame.draw.rect(screen, ORANGE, (fish["x"], fish["y"], fish["width"], fish["height"]))


def detect_collision(hook, fish):
    return (
        hook["x"] < fish["x"] + fish["width"] and
        hook["x"] + hook["width"] > fish["x"] and
        hook["y"] < fish["y"] + fish["height"] and
        hook["y"] + hook["height"] > fish["y"]
    )


def render_text(text, position, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)


# Game Loop
start_ticks = pygame.time.get_ticks()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and boat["x"] > 0:
        boat["x"] -= 4
        hook["x"] -= 4
    if keys[pygame.K_RIGHT] and boat["x"] < SCREEN_WIDTH - boat["width"]:
        boat["x"] += 4
        hook["x"] += 4
    if keys[pygame.K_DOWN]:
        hook["is_catching"] = True
    else:
        hook["is_catching"] = False

    # Move hook
    if hook["is_catching"] and hook["y"] < SCREEN_HEIGHT:
        hook["y"] += 4
    elif not hook["is_catching"] and hook["y"] > boat["hook_y"]:
        hook["y"] -= 4

    # Collision
    if detect_collision(hook, fish):
        score += 1
        fish = {
            "x": random.randint(0, SCREEN_WIDTH - TILE_SIZE),
            "y": random.randint(200, SCREEN_HEIGHT - TILE_SIZE),
            "width": TILE_SIZE,
            "height": TILE_SIZE // 2,
            "caught": False
        }

    # Update time
    seconds_elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = 60 - seconds_elapsed

    # Check for game over
    if time_left <= 0:
        game_over = True

    # Draw everything
    if ocean_bg:
        screen.blit(ocean_bg, (0, 0))
    else:
        screen.fill((30, 144, 255))  # Azul padrão para simular oceano

    draw_boat()
    draw_fish()

    # Draw score and time
    render_text(f"Score: {score}", (10, 10))
    render_text(f"Time: {time_left}s", (10, 50))

    if game_over:
        render_text("Game Over!", (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2), color=(255, 0, 0))

    pygame.display.flip()
    clock.tick(FPS)

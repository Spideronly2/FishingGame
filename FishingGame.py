import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
TILE_SIZE = 20

# Colors
SKY_BLUE = (135, 206, 235)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fishing Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Boat and hook
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

# Controls
controls = {"left": False, "right": False}

def draw_boat():
    pygame.draw.rect(screen, BROWN, (boat["x"], boat["y"], boat["width"], boat["height"]))
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

def update():
    # Move boat
    if controls["left"] and boat["x"] > 0:
        boat["x"] -= 2
        hook["x"] -= 2
    if controls["right"] and boat["x"] < SCREEN_WIDTH - boat["width"]:
        boat["x"] += 2
        hook["x"] += 2

    # Lower or raise the hook
    if hook["is_catching"] and hook["y"] < SCREEN_HEIGHT:
        hook["y"] += 2
    elif not hook["is_catching"] and hook["y"] > boat["hook_y"]:
        hook["y"] -= 2

    # Detect collision
    if detect_collision(hook, fish):
        fish["caught"] = True
        hook["is_catching"] = False
        hook["y"] = boat["hook_y"]  # Reset hook
        # Spawn a new fish
        fish["x"] = random.randint(0, SCREEN_WIDTH - TILE_SIZE)
        fish["y"] = random.randint(200, SCREEN_HEIGHT - TILE_SIZE)
        fish["caught"] = False

def render():
    screen.fill(SKY_BLUE)
    draw_boat()
    draw_fish()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                controls["left"] = True
            elif event.key == pygame.K_RIGHT:
                controls["right"] = True
            elif event.key == pygame.K_DOWN:
                hook["is_catching"] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                controls["left"] = False
            elif event.key == pygame.K_RIGHT:
                controls["right"] = False
            elif event.key == pygame.K_DOWN:
                hook["is_catching"] = False

    update()
    render()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

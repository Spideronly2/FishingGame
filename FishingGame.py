import pygame
import random
import os

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fishing Game")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (135, 206, 250)
BROWN = (139, 69, 19)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Variáveis globais
tile_size = 20
boat_speed = 4
fish_speed = 2
score = 0
time_left = 30

# Carregar imagem de fundo
BACKGROUND_IMG = "background_image.png"
if not os.path.exists(BACKGROUND_IMG):
    print(f"A imagem de fundo {BACKGROUND_IMG} está faltando!")
    exit()
background = pygame.image.load(BACKGROUND_IMG).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Música de fundo
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # Loop infinito

# Definir barco
boat = pygame.Rect(WIDTH // 2 - tile_size, 50, tile_size * 2, tile_size)

# Vara de pesca
hook = pygame.Rect(boat.centerx, boat.bottom, tile_size // 2, tile_size)
hook_is_active = False

# Peixes
fish_list = [
    pygame.Rect(
        random.randint(0, WIDTH - tile_size), 
        random.randint(HEIGHT // 2, HEIGHT - tile_size), 
        tile_size, tile_size // 2
    ) for _ in range(5)
]
fish_directions = [random.choice([-1, 1]) for _ in fish_list]  # Movimento inicial dos peixes

# Fontes
font = pygame.font.Font(None, 36)

# Funções de jogo
def draw_boat():
    pygame.draw.rect(screen, BROWN, boat)
    pygame.draw.rect(screen, BLACK, hook)
    pygame.draw.line(screen, WHITE, (hook.centerx, boat.bottom), (hook.centerx, hook.bottom), 2)  # Linha de pesca

def draw_fishes():
    for fish in fish_list:
        pygame.draw.rect(screen, ORANGE, fish)

def detect_collision(hook, fish):
    return hook.colliderect(fish)

def reset_fish(index):
    fish_list[index] = pygame.Rect(
        random.randint(0, WIDTH - tile_size), 
        random.randint(HEIGHT // 2, HEIGHT - tile_size), 
        tile_size, tile_size // 2
    )
    fish_directions[index] = random.choice([-1, 1])

def update_fishes():
    for i, fish in enumerate(fish_list):
        fish.x += fish_directions[i] * fish_speed

        # Alterar direção quando atingir borda
        if fish.left <= 0 or fish.right >= WIDTH:
            fish_directions[i] *= -1

# Game loop
running = True
while running:
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controles do barco
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and boat.left > 0:
        boat.x -= boat_speed
        hook.x -= boat_speed
    if keys[pygame.K_RIGHT] and boat.right < WIDTH:
        boat.x += boat_speed
        hook.x += boat_speed

    # Controle da vara
    if keys[pygame.K_DOWN]:
        hook_is_active = True
    else:
        hook_is_active = False

    if hook_is_active and hook.bottom < HEIGHT:
        hook.y += 4
    elif not hook_is_active and hook.top > boat.bottom:
        hook.y -= 4

    # Detectar colisão
    for i, fish in enumerate(fish_list):
        if detect_collision(hook, fish):
            score += 1
            time_left += 0.2  # Adiciona 0.2 segundos ao tempo restante
            reset_fish(i)

    # Atualizar peixes
    update_fishes()

    # Atualizar tempo restante
    time_left -= 1 / FPS
    if time_left <= 0:
        running = False

    # Desenhar na tela
    draw_boat()
    draw_fishes()

    # Mostrar pontuação e tempo
    score_text = font.render(f"Score: {score}", True, WHITE)
    time_text = font.render(f"Time: {time_left:.1f}s", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (WIDTH - 150, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

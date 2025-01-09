import pygame
import random

# Inicializando o Pygame
pygame.init()

# Dimensões da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Pesca")

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 105, 148)

# Carregar imagens
background_image = pygame.image.load("background.png")  # Certifique-se de que esta imagem está no mesmo diretório
boat_image = pygame.image.load("/mnt/data/Canoepixelart.png")  # Nova imagem do barco
fish_image = pygame.image.load("/mnt/data/fishingpixelart.png")  # Nova imagem do peixe

# Escalando imagens
boat_image = pygame.transform.scale(boat_image, (100, 50))
fish_image = pygame.transform.scale(fish_image, (40, 30))

# Configurações do jogo
clock = pygame.time.Clock()
boat_x, boat_y = WIDTH // 2, HEIGHT - 100
hook_x, hook_y = boat_x + 45, boat_y + 20
boat_speed = 10  # Velocidade aumentada
timer = 30
score = 0
font = pygame.font.Font(None, 36)

# Lista de peixes
fish_list = []
for i in range(5):
    fish_x = random.randint(50, WIDTH - 50)
    fish_y = random.randint(50, HEIGHT // 2)
    fish_list.append([fish_x, fish_y])

# Reiniciar jogo
def restart_game():
    global boat_x, hook_x, hook_y, timer, score, fish_list
    boat_x = WIDTH // 2
    hook_x = boat_x + 45
    hook_y = boat_y + 20
    timer = 30
    score = 0
    fish_list = []
    for i in range(5):
        fish_x = random.randint(50, WIDTH - 50)
        fish_y = random.randint(50, HEIGHT // 2)
        fish_list.append([fish_x, fish_y])

# Loop do jogo
running = True
while running:
    screen.fill(BLUE)
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and boat_x > 0:
        boat_x -= boat_speed
    if keys[pygame.K_RIGHT] and boat_x < WIDTH - 100:
        boat_x += boat_speed

    # Atualizar posição do gancho
    hook_x = boat_x + 45

    # Desenhar barco e gancho
    screen.blit(boat_image, (boat_x, boat_y))
    pygame.draw.line(screen, WHITE, (hook_x, hook_y), (hook_x, hook_y + 50), 2)

    # Desenhar peixes
    for fish in fish_list:
        screen.blit(fish_image, (fish[0], fish[1]))

    # Detectar captura de peixes
    for fish in fish_list[:]:
        if hook_x in range(fish[0] - 20, fish[0] + 60) and hook_y + 50 in range(fish[1] - 10, fish[1] + 40):
            fish_list.remove(fish)
            score += 1
            timer += 5  # Adiciona tempo ao pegar um peixe

    # Atualizar timer
    timer -= 1 / 30
    if timer <= 0:
        running = False

    # Exibir placar e tempo
    score_text = font.render(f"Score: {score}", True, WHITE)
    timer_text = font.render(f"Time: {int(timer)}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(timer_text, (10, 50))

    # Atualizar tela
    pygame.display.flip()
    clock.tick(30)

# Exibir mensagem de fim de jogo
screen.fill(BLUE)
game_over_text = font.render("Game Over! Pressione Espaço para reiniciar.", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
pygame.display.flip()

# Esperar reinício ou sair
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                restart_game()
                running = True
                waiting = False

pygame.quit()

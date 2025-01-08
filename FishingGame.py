import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fishing Game")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonte para exibir o score e o tempo
font = pygame.font.SysFont("arial", 24)

# Variáveis globais
clock = pygame.time.Clock()
running = True

# Variáveis de pontuação e tempo
score = 0  # Pontos iniciais
time_left = 60  # Tempo inicial (segundos)

# Controladores para movimentos
controls = {"left": False, "right": False}

# Posição do gancho
hook = {
    "x": screen_width // 2,
    "y": screen_height - 100,
    "is_catching": False
}

# Evento para controlar o tempo (1000 ms = 1 segundo)
pygame.time.set_timer(pygame.USEREVENT, 1000)

# Renderizar texto na tela
def render_text():
    # Pontuação
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Tempo restante
    time_text = font.render(f"Time Left: {time_left}s", True, WHITE)
    screen.blit(time_text, (10, 40))

# Renderizar elementos na tela
def render():
    screen.fill(BLACK)  # Fundo
    render_text()  # Desenha o texto do score e do tempo
    pygame.draw.rect(screen, WHITE, (hook["x"], hook["y"], 10, 50))  # Desenha o gancho

# Atualizar lógica do jogo
def update():
    global score
    if controls["left"] and hook["x"] > 0:
        hook["x"] -= 5
    if controls["right"] and hook["x"] < screen_width - 10:
        hook["x"] += 5
    
    # Simular captura para aumentar o score
    if hook["is_catching"]:  # Aqui você pode adicionar condições reais
        score += 10  # Aumenta 10 pontos se algo é capturado

# Loop principal
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detecta teclas pressionadas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                controls["left"] = True
            elif event.key == pygame.K_RIGHT:
                controls["right"] = True
            elif event.key == pygame.K_DOWN:  # Simula "pescar"
                hook["is_catching"] = True

        # Detecta teclas soltas
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                controls["left"] = False
            elif event.key == pygame.K_RIGHT:
                controls["right"] = False
            elif event.key == pygame.K_DOWN:
                hook["is_catching"] = False

        # Evento para diminuir o tempo
        if event.type == pygame.USEREVENT:
            if time_left > 0:
                time_left -= 1
            else:
                print("Fim do jogo! O tempo acabou!")
                running = False

    # Atualizar e renderizar o jogo
    update()
    render()

    pygame.display.flip()
    clock.tick(60)

# Finalizar Pygame
pygame.quit()

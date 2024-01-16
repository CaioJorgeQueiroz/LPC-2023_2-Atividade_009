import pygame
import spritesheet
import time

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BG_COLOR = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

# Load sprite sheet image
try:
    sprite_sheet_image = pygame.image.load('trunks.png').convert_alpha()
except pygame.error as e:
    print(f"Error loading sprite sheet: {e}")
    pygame.quit()
    quit()

# Create a SpriteSheet object
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

# Animation parameters
animation_list = []
animation_steps = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 500
frame = 0
step_counter = 0
power = False
transformed = False

# Populate animation list
for animation in animation_steps:
    if step_counter == 13:  # Se for um sprite de transformação
        temp_img_list = [sprite_sheet.get_image(step_counter, 64, 68, 3, BLACK) for _ in range(animation)]
    elif 21 <= step_counter <= 25 :  # Se for um sprite de transformação
        temp_img_list = [sprite_sheet.get_image(step_counter, 50.5, 68, 3, BLACK) for _ in range(animation)]
    elif step_counter == 3:  # Se for um sprite de transformação
        temp_img_list = [sprite_sheet.get_image(step_counter, 154, 68, 3, BLACK) for _ in range(animation)]
    elif step_counter == 9:  # Se for um sprite de transformação
        temp_img_list = [sprite_sheet.get_image(step_counter, 156, 68, 3, BLACK) for _ in range(animation)]
    else:
        temp_img_list = [sprite_sheet.get_image(step_counter, 45, 68, 3, BLACK) for _ in range(animation)]
    animation_list.append(temp_img_list)
    step_counter += animation

print(animation_list)

# Variables for sprite looping
sprite_index = 0
sprite_positions = [0, 13, 10]  # Adicionado os sprites de transformação

# Variable to track if transformation has occurred
transformed = False
power = False

# Create a clock object
clock = pygame.time.Clock()

# Main game loop
run = True
shift_pressed = False
while run:

    screen.fill(BG_COLOR)

    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        last_update = current_time
        frame = (frame + 1) % len(animation_list[action])
        if frame == 0:
            sprite_index = (sprite_index + 1) % len(sprite_positions)
            action = sprite_positions[sprite_index]

    keys = pygame.key.get_pressed()
    mods = pygame.key.get_mods()
    if mods & pygame.KMOD_SHIFT:
        shift_pressed = True
        animation_cooldown = 140
        action = 13  # A ação agora será a transformação em Super Saiyajin
        frame = 0
        if not transformed:
            transformed = True
    elif shift_pressed:
        shift_pressed = False
        action = 10  # A ação será o sprite 10 quando Shift for solto
    elif mods & pygame.KMOD_CTRL and transformed:
        animation_cooldown = 140
        action = 0  # A ação agora será a transformação em Super Saiyajin
        transformed = False
    elif keys[pygame.K_RIGHT] and not transformed:
        animation_cooldown = 140
        action = 3
        frame = 0
    elif keys[pygame.K_RIGHT] and transformed:
        animation_cooldown = 140
        action = 9
        frame = 0

    elif keys[pygame.K_SPACE] and not transformed:  # Adicionado o controle para a tecla ESPAÇO
        clock.tick(10)
        animation_cooldown = 1000  # Aumentado para tornar a animação mais lenta
        if action == 2:
            action = 4
        else:
            action = (action + 1) if 1 <= action < 8 else 1

    elif keys[pygame.K_SPACE] and transformed:  # Adicionado o controle para a tecla ESPAÇO
        clock.tick(10)
        animation_cooldown = 1000  # Aumentado para tornar a animação mais lenta
        action = (action + 1) if 21 <= action < 25 else 21
    else:
        action = 20 if transformed else 0
        frame = 0

    screen.blit(animation_list[action][frame], (50, 120))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
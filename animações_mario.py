import pygame
import spritesheet

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BG_COLOR = (50, 50, 50)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

# Load sprite sheet image
try:
    sprite_sheet_image = pygame.image.load('mario-3.png').convert_alpha()
except pygame.error as e:
    print(f"Error loading sprite sheet: {e}")
    pygame.quit()
    quit()

# Create a SpriteSheet object
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

# Animation parameters
animation_list = []
animation_steps = [1, 1, 1, 1, 2, 1, 1]
action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 500  
frame = 0
step_counter = 0

# Populate animation list
for animation in animation_steps:
    temp_img_list = [sprite_sheet.get_image(step_counter, 22, 36, 3, BLACK) for _ in range(animation)]
    animation_list.append(temp_img_list)
    step_counter += animation

print(animation_list)

# Variables for sprite looping
sprite_index = 0
sprite_positions = [1, 2] 

# Main game loop
run = True
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
    if keys[pygame.K_RIGHT]:
        if mods & pygame.KMOD_SHIFT:
            animation_cooldown = 140
        else:
            animation_cooldown = 500
        action = sprite_positions[sprite_index]  
    elif keys[pygame.K_UP]:
        animation_cooldown = 250
        action = 5
        frame = 0
    else:
        action = 0
        frame = 0

    screen.blit(animation_list[action][frame], (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

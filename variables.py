import pygame
import buttons

'''
This is the file containing most of the game variables,
including the global ones, they suffer changes throughout
the game and only come back to default in cases of 'new game'
'''

#define fps
clock = pygame.time.Clock()
fps = 80

#define screen and screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Extraordinary Jobs Galaxy!")

#load title screen buttons' images
continue_button_img = pygame.image.load('src/sprites/buttons/continue.jpeg').convert_alpha()
new_game_button_img = pygame.image.load('src/sprites/buttons/continue.jpeg').convert_alpha()
shopping_button_img = pygame.image.load('src/sprites/buttons/continue.jpeg').convert_alpha()
back_button_img = pygame.image.load('src/sprites/buttons/continue.jpeg').convert_alpha()
menu_button_img = pygame.image.load('src/sprites/buttons/continue.jpeg').convert_alpha()

#create title screen buttons' instances
continue_button = buttons.Button(100, 400, continue_button_img, 0.6)
new_game_button = buttons.Button(100, 500, new_game_button_img, 0.6)
shopping_button = buttons.Button(100, 600, shopping_button_img, 0.6)
back_button = buttons.Button(10, 10, shopping_button_img, 0.6)

#load Phase Menu buttons' images
phase_img = pygame.image.load('src/sprites/buttons/continue.jpeg').convert_alpha()

#create Phase Menu buttons' instances
phase1_button = buttons.Button(100, 300, phase_img, 0.5)
phase2_button = buttons.Button(100, 400, phase_img, 0.5)
phase3_button = buttons.Button(100, 500, phase_img, 0.5)

#load spaceship sprites
spaceship_sprites = [[]]
for i in range (4):
    spaceship_sprites[0].append(pygame.image.load(f'src/sprites/spaceship/samples/main/spaceship-{i}.png'))
    spaceship_sprites[0][i] = pygame.transform.scale(spaceship_sprites[0][i], (int(spaceship_sprites[0][i].get_width() * 2), int(spaceship_sprites[0][i].get_height() * 2)))

#game sprite groups
spaceship_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
clt_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
r_item_group = pygame.sprite.Group()

#default global variables
spaceship_now = [True]
points = 0
spaceship_speed = 8
haspulse = True
pulse_speed = 3
clt_speed = 20
lifebar = 10
phases = [False, False, False]
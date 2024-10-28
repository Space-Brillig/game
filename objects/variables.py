import pygame
import objects.buttons as buttons

pygame.font.init()
pygame.init()

'''
This is the file containing most of the game variables,
including the global ones, they suffer changes throughout
the game and only come back to default in cases of 'new game'
'''

#define fps
clock = pygame.time.Clock()
fps = 80

#define screen and screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("The Extraordinary Jobs' Galaxy!")

#define global buttons
menu_button_img = pygame.image.load('assets/sprites/buttons/continue.jpeg').convert_alpha()
back_button_img = pygame.image.load('assets/sprites/buttons/back_button.jpeg').convert_alpha()
back_button = buttons.Button(back_button_img, 0.6)

#manage selected sprite
#manage selected engine: Base Engine, Big Pulse Engine, Burst Engine, Supercharged Engine
#manage selected shield: Invisibility Shield, Round Shield, Front, Side Shield
selected = {"sprite": [True], "engine": [True, False, False, False], "shield": [True, False, False, False]}
bought = {"engine": [True, False, False, False], "shield": [True, False, False, False]}

#game sprite groups
spaceship_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
clt_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
r_item_group = pygame.sprite.Group()

#default global variables
points = 10000
clt_speed = 20
lifebar = 10
screens = [True, True, True, True, True] #initial screen, phase 1, phase 2, phase 3, phase 4

#set game font text
font = pygame.font.Font('freesansbold.ttf', 24)
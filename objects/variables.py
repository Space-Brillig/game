import pygame
import objects.buttons as buttons
from objects.SaveLoad import SaveLoadSystem as SaveLoad

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
back_button_img = pygame.image.load('assets/sprites/buttons/return.png').convert_alpha()
back_button = buttons.Button(back_button_img, 0.6)
bitcoin_img = pygame.image.load('assets/sprites/buttons/bitcoin.png')
bitcoin_img = pygame.transform.scale(bitcoin_img, (bitcoin_img.get_width() * 0.15, bitcoin_img.get_height() * 0.15))

#default global variables

#manage selected sprite
#manage selected engine: Base Engine, Big Pulse Engine, Burst Engine, Supercharged Engine
#manage selected shield: Invisibility Shield, Round Shield, Front, Side Shield

saveload = SaveLoad('.save', 'objects/save_data')

points, clt_speed, lifebar, screens, selected, bought, player_name = saveload.load_game_data(["points", "clt_speed", "lifebar", "screens", "selected", "bought", "player_name"], [100, 10, 10, [False, False, False, False, False], {"sprite": [True], "engine": [True, False, False, False], "shield": [True, False, False, False]}, {"engine": [True, False, False, False], "shield": [True, False, False, False]}, ''])

#game sprite groups
spaceship_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
clt_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
r_item_group = pygame.sprite.Group()

#set game font text
font = pygame.font.Font('freesansbold.ttf', 24)
mfont = pygame.font.Font('freesansbold.ttf', 14)
tfont = pygame.font.Font('freesansbold.ttf', 64)
pmfont = pygame.font.Font('freesansbold.ttf', 30)
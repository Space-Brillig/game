import pygame
from random import randint
import objects.functions as functions
import objects.variables as variables
import objects.buttons as buttons

pygame.mixer.init()

'''
This is the first screen to be printed to the user when
the game starts (except for the user's first time). Here,
we can decide whether to:
- continue game
- start a new game
- visit the market
'''

#create title game
name_icon = variables.tfont.render("The extraordinary Job's Galaxy", True, 'white')
name_icon_width = name_icon.get_width()

#load title screen buttons' images
continue_button_img = pygame.image.load('assets/sprites/buttons/continue.png').convert_alpha()
new_game_button_img = pygame.image.load('assets/sprites/buttons/new_game.png').convert_alpha()
market_button_img = pygame.image.load('assets/sprites/buttons/market.png').convert_alpha()

#create title screen buttons' instances
continue_button = buttons.Button(continue_button_img, 0.4)
new_game_button = buttons.Button(new_game_button_img, 0.45)
market_button = buttons.Button(market_button_img, 0.6)
button_width = continue_button.image.get_width()

#load stars' images
stars = [[], [], []]
#galaxy animation
for i in range (60):
    stars[0].append(pygame.image.load(f"assets/sprites/background/galaxy/galaxia({i + 1}).gif").convert())
    stars[0][i] = pygame.transform.scale(stars[0][i], (stars[0][i].get_width() * 3, stars[0][i].get_height() * 3))
#blackhole animation
for i in range (49):
    stars[1].append(pygame.image.load(f"assets/sprites/background/blackhole/frame-{i + 1}.gif").convert())
    stars[1][i] = pygame.transform.scale(stars[1][i], (stars[0][i].get_width() * 2, stars[1][i].get_height() * 2))
#rings animation
for i in range (60):
    stars[2].append(pygame.image.load(f"assets/sprites/background/rings/anedota({i + 1}).gif").convert())
    stars[2][i] = pygame.transform.scale(stars[2][i], (stars[0][i].get_width() * 2, stars[2][i].get_height() * 2))

#Title Screen function
def Title_screen():

    #setting the background
    icon = randint(0, 2)
    star_width = stars[icon][0].get_width()
    if icon == 0:
        length1 = 60
        a_coord = (0, -50)
    elif icon == 1:
        length1 = 49
        a_coord = (0, -100)
    elif icon == 2:
        length1 = 60
        a_coord = (0, -220)
    bg = pygame.image.load("assets/sprites/background/bg.png").convert()
    bg_height = bg.get_height()
    bg_width = bg.get_width()
    index = 0

    while True:
        
        #set fps
        variables.clock.tick(variables.fps - 40)
        bg = pygame.transform.scale(bg, (variables.SCREEN_WIDTH, (variables.SCREEN_WIDTH * bg_height) // bg_width))
        bg_height = bg.get_height()
        bg_width = bg.get_width()
        functions.draw_bg(bg)

        functions.display_bitcoins('white')

        variables.screen.blit(name_icon, (variables.SCREEN_WIDTH // 2 - name_icon_width // 2, 50))
        
        # stars animation
        index += 1
        if index == length1:
            index = 0
        variables.screen.blit(stars[icon][index], (variables.SCREEN_WIDTH // 6 - star_width * 0.5 + a_coord[0], variables.SCREEN_HEIGHT // 2 + a_coord[1]))
        variables.screen.blit(stars[icon][index], (variables.SCREEN_WIDTH * (5/6) - star_width * 0.5 + a_coord[0], variables.SCREEN_HEIGHT // 2 + a_coord[1]))

        #actions depending on clicked buttons
        if continue_button.draw(variables.screen, variables.SCREEN_WIDTH // 2 - button_width // 2, variables.SCREEN_HEIGHT // 3 + 50):
            return 0 #go to phase menu function
        if new_game_button.draw(variables.screen, variables.SCREEN_WIDTH // 2 - button_width // 2 + 15, continue_button.rect.y + 125):
            return 1 #new game
        if market_button.draw(variables.screen, variables.SCREEN_WIDTH // 2 - button_width // 2 + 27, new_game_button.rect.y + 120):
            return 2 #go to the market

        #quit game
        if functions.event_handlers():
            return -1
        
        pygame.display.update()
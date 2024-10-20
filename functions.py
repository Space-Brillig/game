import pygame
import variables
import characters
from random import randint

'''
This file contains some of the created ingame
functions and events, used to facilitate things a lot
'''

#wait for mouse release in screen changing
def mouse_release():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:  # Wait until mouse button is released
                waiting = False

#draw background
def draw_bg(bg):
     
    variables.screen.blit(bg, (0,0))

#event handlers
def event_handlers():

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit game
            return True
        
#creature spawning function
def spawn_creatures(props): #spawning based on proportions, respectively: alien, meteor and regenerative item

    random = randint(1, props[-1]) #generate a number between 1 and the greatest proportion

    if random <= props[0]: 

        #spawn alien
        alien = characters.Alien(randint(30, variables.SCREEN_WIDTH - 30), randint(-100, -50))
        characters.alien_group.add(alien)
    
    elif random <= props[1] and random > props[0]: 

        #spawn meteor
        meteor = characters.Projectile(randint(10, variables.SCREEN_WIDTH - 10), randint(-100, -50), 0.05, "meteor", True)
        characters.meteor_group.add(meteor)
    
    elif random > props[0] and random > props[1]:

        #spawn regenerative item
        r_item = characters.Projectile(randint(10, variables.SCREEN_WIDTH - 10), randint(-100, -50), 0.7, "r_item", False)
        characters.r_item_group.add(r_item)
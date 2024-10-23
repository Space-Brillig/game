import pygame
import objects.buttons as buttons
import objects.variables as variables
import objects.functions as functions

'''
This file contains the screen of the game where we
can whether access the phases or go back to title
screen. It's the menu containing the passed phases
and the phases yet to be passed
'''

#load Phase Menu buttons' images
phase_img = pygame.image.load('assets/sprites/buttons/continue.jpeg').convert_alpha()

#create Phase Menu buttons' instances
phase1_button = buttons.Button(100, 300, phase_img, 0.5)
phase2_button = buttons.Button(100, 400, phase_img, 0.5)
phase3_button = buttons.Button(100, 500, phase_img, 0.5)

#Phase Menu function
def Phase_menu():

    while True:
        
        #set fps
        variables.clock.tick(variables.fps)
        
        variables.screen.fill((100, 100, 240))

        #actions depending on clicked buttons
        if variables.back_button.draw(variables.screen):
            return -1 # go back
        if phase1_button.draw(variables.screen):
            return 0 #calls the phase function with phase 1 parameters
        if variables.phases[0]:
            if phase2_button.draw(variables.screen):
                return 1 #calls the phase function with phase 2 parameters if phase 1 was passed
        else:
            rect = pygame.Rect(100, 400, 150, 100)
            pygame.draw.rect(variables.screen, (255, 0, 255), rect)
        
        if variables.phases[1]:
            if phase3_button.draw(variables.screen):
                return 2 #calls the phase function with phase 3 parameters if phase 2 was passed
        else:
            rect = pygame.Rect(100, 500, 150, 100)
            pygame.draw.rect(variables.screen, (255, 0, 255), rect)
        
        if functions.event_handlers():
            return -2 #quit game

        pygame.display.update()
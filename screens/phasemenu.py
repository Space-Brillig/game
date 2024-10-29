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
phase1_button = buttons.Button(phase_img, 0.5)
phase2_button = buttons.Button(phase_img, 0.5)
phase3_button = buttons.Button(phase_img, 0.5)
phase4_button = buttons.Button(phase_img, 0.5)
phase5_button = buttons.Button(phase_img, 0.5)

#Phase Menu function
def Phase_menu():

    while True:
        
        #set fps
        variables.clock.tick(variables.fps)
        
        variables.screen.fill((100, 100, 240))

        functions.display_bitcoins('white')

        event = functions.event_handlers()
        if event == True:
            return -2 #quit game

        #actions depending on clicked buttons
        if variables.back_button.draw(variables.screen, 10, 10) or event == False:
            return -1 # go back
        
        #calls the phase function with phase 1 parameters
        if phase1_button.draw(variables.screen, variables.SCREEN_WIDTH // 6, variables.SCREEN_HEIGHT // 6):
            return 0
        
        #calls the phase function with phase 2 parameters if phase 1 was passed
        if variables.screens[1]:
            if phase2_button.draw(variables.screen, variables.SCREEN_WIDTH * (2/3), variables.SCREEN_HEIGHT // 6):
                return 1
        else:
            rect = pygame.Rect(variables.SCREEN_WIDTH * (2/3), variables.SCREEN_HEIGHT // 6, 150, 100)
            pygame.draw.rect(variables.screen, (255, 0, 255), rect)
        
        #calls the phase function with phase 3 parameters if phase 2 was passed
        if variables.screens[2]:
            if phase3_button.draw(variables.screen, variables.SCREEN_WIDTH // 6, variables.SCREEN_HEIGHT * (2/3)):
                return 2
        else:
            rect = pygame.Rect(variables.SCREEN_WIDTH // 6, variables.SCREEN_HEIGHT * (2/3), 150, 100)
            pygame.draw.rect(variables.screen, (255, 0, 255), rect)

        #calls the phase function with phase 4 parameters if phase 2 was passed
        if variables.screens[3]:
            if phase4_button.draw(variables.screen, variables.SCREEN_WIDTH * (2/3), variables.SCREEN_HEIGHT * (2/3)):
                return 3
        else:
            rect = pygame.Rect(variables.SCREEN_WIDTH * (2/3), variables.SCREEN_HEIGHT * (2/3), 150, 100)
            pygame.draw.rect(variables.screen, (255, 0, 255), rect)

        if variables.screens[4]:
            if phase4_button.draw(variables.screen, variables.SCREEN_WIDTH // 2 - phase5_button.image.get_width() // 2, variables.SCREEN_HEIGHT // 2 - phase5_button.image.get_height() // 2):
                return 4
        else:
            rect = pygame.Rect(variables.SCREEN_WIDTH // 2, variables.SCREEN_HEIGHT // 2, 150, 100)
            pygame.draw.rect(variables.screen, (255, 0, 255), rect)

        pygame.display.update()
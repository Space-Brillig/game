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

#title
title = variables.tfont.render('Fases', True, 'white')
title_width = title.get_width()

#load Phase Menu buttons' images
phaseoff = pygame.image.load('assets/sprites/buttons/phaseoff.png').convert_alpha()
phaseoff = pygame.transform.scale(phaseoff, (phaseoff.get_width() * 0.2, phaseoff.get_height() * 0.2))
phase1on = pygame.image.load('assets/sprites/buttons/phase1on.png').convert_alpha()
phase2on = pygame.image.load('assets/sprites/buttons/phase2on.png').convert_alpha()
phase3on = pygame.image.load('assets/sprites/buttons/phase3on.png').convert_alpha()
phase4on = pygame.image.load('assets/sprites/buttons/phase4on.png').convert_alpha()
phase5on = pygame.image.load('assets/sprites/buttons/phase5on.png').convert_alpha()

#phase titles
phase_titles = []
for i in range (5):
    phase_titles.append(variables.pmfont.render(f'Fase {i + 1}', True, 'white'))
    
#create Phase Menu buttons' instances
phase_buttons = [buttons.Button(phase1on, 0.8), buttons.Button(phase2on, 0.8), buttons.Button(phase3on, 0.8), buttons.Button(phase4on, 0.8), buttons.Button(phase5on, 0.8)]

#Phase Menu function
def Phase_menu():

    bg = pygame.image.load("assets/sprites/background/bg.png").convert_alpha()
    bg_height = bg.get_height()
    bg_width = bg.get_width()

    while True:
        
        #set fps
        variables.clock.tick(variables.fps)
        
        #set background
        bg = pygame.transform.scale(bg, (variables.SCREEN_WIDTH, (variables.SCREEN_WIDTH * bg_height) // bg_width))
        bg_height = bg.get_height()
        bg_width = bg.get_width()

        functions.draw_bg(bg)

        variables.screen.blit(title, (variables.SCREEN_WIDTH // 2 - title_width // 2, 50))

        functions.display_bitcoins('white')

        event = functions.event_handlers()
        if event == True:
            return -2 #quit game

        #actions depending on clicked buttons
        if variables.back_button.draw(variables.screen, 10, 10) or event == False:
            return -1 # go back
        
        #calls the phase function with phase 1 parameters
        variables.screen.blit(phase_titles[0], (variables.SCREEN_WIDTH // 6 + 30, variables.SCREEN_HEIGHT // 6 + 180))
        if phase_buttons[0].draw(variables.screen, variables.SCREEN_WIDTH // 6, variables.SCREEN_HEIGHT // 6):
            return 0
        
        #calls the phase function with phase 2 parameters if phase 1 was passed
        if variables.screens[1]:
            variables.screen.blit(phase_titles[1], (variables.SCREEN_WIDTH * (2/3) + 30, variables.SCREEN_HEIGHT // 6 + 180))
            if phase_buttons[1].draw(variables.screen, variables.SCREEN_WIDTH * (2/3), variables.SCREEN_HEIGHT // 6):
                return 1
        else:
            variables.screen.blit(phase_titles[1], (variables.SCREEN_WIDTH * (2/3) + 60, variables.SCREEN_HEIGHT // 6 + 180))
            variables.screen.blit(phaseoff, (variables.SCREEN_WIDTH * (2/3), variables.SCREEN_HEIGHT // 6))
        #calls the phase function with phase 3 parameters if phase 2 was passed
        if variables.screens[2]:
            variables.screen.blit(phase_titles[2], (variables.SCREEN_WIDTH // 6 + 30, variables.SCREEN_HEIGHT * (2/3) + 180))
            if phase_buttons[2].draw(variables.screen, variables.SCREEN_WIDTH // 6, variables.SCREEN_HEIGHT * (2/3)):
                return 2
        else:
            variables.screen.blit(phase_titles[2], (variables.SCREEN_WIDTH // 6 + 60, variables.SCREEN_HEIGHT * (2/3) + 180))
            variables.screen.blit(phaseoff, (variables.SCREEN_WIDTH // 6, variables.SCREEN_HEIGHT * (2/3)))
        #calls the phase function with phase 4 parameters if phase 3 was passed
        if variables.screens[3]:
            variables.screen.blit(phase_titles[3], (variables.SCREEN_WIDTH * (2/3) + 30, variables.SCREEN_HEIGHT * (2/3) + 180))
            if phase_buttons[3].draw(variables.screen, variables.SCREEN_WIDTH * (2/3), variables.SCREEN_HEIGHT * (2/3)):
                return 3
        else:
            variables.screen.blit(phase_titles[3], (variables.SCREEN_WIDTH * (2/3) + 60, variables.SCREEN_HEIGHT * (2/3) + 180))
            variables.screen.blit(phaseoff, (variables.SCREEN_WIDTH * (2/3), variables.SCREEN_HEIGHT * (2/3)))
        #calls final phase
        if variables.screens[4]:
            variables.screen.blit(phase_titles[4], (variables.SCREEN_WIDTH // 2 - phase_buttons[4].image.get_width() // 2 + 30, variables.SCREEN_HEIGHT // 2 - phase_buttons[4].image.get_height() // 2 + 180))
            if phase_buttons[4].draw(variables.screen, variables.SCREEN_WIDTH // 2 - phase_buttons[4].image.get_width() // 2, variables.SCREEN_HEIGHT // 2 - phase_buttons[4].image.get_height() // 2):
                return 4
        else:
            variables.screen.blit(phase_titles[4], (variables.SCREEN_WIDTH // 2 - phase_buttons[4].image.get_width() // 2 + 20, variables.SCREEN_HEIGHT // 2 - phase_buttons[4].image.get_height() // 2 + 160))
            variables.screen.blit(phaseoff, (variables.SCREEN_WIDTH // 2 - 120, variables.SCREEN_HEIGHT // 2 - 100))
        pygame.display.update()
import pygame
import screens.initialscreen as initialscreen
import screens.titlescreen as titlescreen
import screens.phasemenu as phasemenu
import screens.phase as phase
import objects.variables as variables

pygame.init()

'''
This is the main file of the game, containing
the logic of the screen changing based on the
user's choice. All the other screens of the game appear
here in their practical form of functions
'''

#load game's songs
clairdelune = pygame.mixer.Sound('assets/music/ClairdeLune-Debussy&Vinheteiro.mp3')
sonata_1stmovement = pygame.mixer.Sound('assets/music/MoonlightSonata(1stMovement)-Beethoven&EmilGilels.mp3')
sonata_2ndmovement = pygame.mixer.Sound('assets/music/MoonlightSonata(2ndMovement)-Beethoven&Rosseou.mp3')
sonata_3rdmovement = pygame.mixer.Sound('assets/music/MoonlightSonata(3rdMovement)-Beethoven&Rosseou.mp3')
preludium = pygame.mixer.Sound('assets/music/PreludiuminCmajor-Bach&TatianaNikolayeva.mp3')

#Main game logic
def main():

    #first interaction
    if not variables.screens[0]:
        if not initialscreen.Initialscreen(clairdelune):
            return True

    sonata_1stmovement.play(-1)

    #looping between title_screen and phases_menu
    while True:

        #set fps
        variables.clock.tick(variables.fps)

        #storing the user's choice
        title_screen_result = titlescreen.Title_screen()

        #quit game
        if title_screen_result == -1:
            return True

        if title_screen_result == 0:
            #looping between phases_menu and the phases
            while True:
                
                #storing the user's choice
                phase_menu_result = phasemenu.Phase_menu()

                #go back to title_screen
                if phase_menu_result == -1:
                    break

                #quit game
                elif phase_menu_result == -2:
                    return True
                
                sonata_1stmovement.stop()

                #go to phase 1
                if phase_menu_result == 0:
                    clairdelune.play(-1)
                    phase_result = phase.Phase("assets/sprites/background/bg.png", 5, [10, 15, 17], 5, 1500) #phase 1 parameters
                    phase_passed = 1

                    clairdelune.stop()
                
                #go to phase 2
                elif phase_menu_result == 1:
                    sonata_2ndmovement.play(-1)
                    phase_result = phase.Phase("assets/sprites/background/space.png", 7, [4, 12, 17], 30, 1000) #phase 2 parameters
                    phase_passed = 2

                    sonata_2ndmovement.stop()
                
                #go to phase 3
                elif phase_menu_result == 2:
                    sonata_3rdmovement.play(-1)
                    phase_result = phase.Phase("assets/sprites/background/bg.png", 10, [2, 20, 25], 45, 500) #phase 3 parameters
                    phase_passed = 3

                    sonata_3rdmovement.stop()

                if phase_result == -2:
                    return True #game is closed
                elif phase_result == 0:
                    variables.screens[phase_passed] = True #phase is passed
                
                sonata_1stmovement.play(-1)

                pygame.display.update()

        #new game
        elif title_screen_result == 1: #reboot global variables
            print ("new game")

        #go to the market
        elif title_screen_result == 2:
            print ('market')

if main():
    pygame.quit()
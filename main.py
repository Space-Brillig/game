import pygame
import title_screen
import phase_menu
import phase
import variables

pygame.init()

'''
This is the main file of the game, containing
the logic of the screen changing based on the
user's choice. All the other screens of the game appear
here in their practical form of functionwwss
'''

#Main game logic
def main():

    #looping between title_screen and phases_menu
    while True:

        #set fps
        variables.clock.tick(variables.fps)
        
        #storing the user's choice
        title_screen_result = title_screen.Title_screen()

        #quit game
        if title_screen_result == -1:
            return True

        if title_screen_result == 0:
            #looping between phases_menu and the phases
            while True:
                
                #storing the user's choice
                phase_menu_result = phase_menu.Phase_menu()

                #quit game
                if phase_menu_result == -2:
                    return True

                #go back to title_screen
                elif phase_menu_result == -1:
                    break
                
                #go to phase 1
                if phase_menu_result == 0:
                    phase_result = phase.Phase("src/sprites/background/bg.png", 5, [10, 15, 17], 5, 1500) #phase 1 parameters
                    if phase_result == -2:
                        return True #game is closed
                    elif phase_result == -1:
                        continue #go back to phase_menu
                    elif phase_result == 0:
                        variables.phases[0] = True #phase is passed
                
                #go to phase 2
                elif phase_menu_result == 1:
                    phase_result = phase.Phase("src/sprites/background/space.png", 7, [4, 12, 17], 30, 1000) #phase 2 parameters
                    if phase_result == -2:
                        return True #game is closed
                    elif phase_result == -1:
                        continue #go back to phase_menu
                    elif phase_result == 0:
                        variables.phases[-2] = True #phase is passed
                
                #go to phase 3
                elif phase_menu_result == 2:
                    phase_result = phase.Phase("src/sprites/background/bg.png", 10, [2, 20, 25], 45, 500) #phase 3 parameters
                    if phase_result == -2:
                        return True #game is closed
                    elif phase_result == -1:
                        continue #go back to phase_menu
                    elif phase_result == 0:
                        variables.phases[-1] = True #phase is passed
                
                pygame.display.update()

        #new game
        elif title_screen_result == 1: #reboot global variables
            print ("calma voy")

        #go to the market
        elif title_screen_result == 2:
            print ('pero vaz')

if main():
    pygame.quit()
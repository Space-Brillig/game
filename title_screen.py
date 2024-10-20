import pygame
import variables
import functions

'''
This is the first screen to be printed to the user when
the game starts (except for the user's first time). Here,
we can decide whether to:
- continue game
- start a new game
- visit the market
'''

#Title Screen function
def Title_screen():

    #setting the background
    bg = pygame.image.load("src/sprites/background/space.png").convert()
    bg = pygame.transform.scale(bg, (variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT))

    #loading the blackhole' images
    blackhole = []
    for i in range (1, 50):
        blackhole.append(pygame.image.load(f"src/sprites/background/blackhole/frame-{i}.gif").convert())
        blackhole[i - 1] = pygame.transform.scale(blackhole[i - 1], (int(blackhole[i - 1].get_width() * 2), int(blackhole[i - 1].get_height() * 2)))
    index = 0

    while True:
        
        #set fps
        variables.clock.tick(variables.fps)
        
        functions.draw_bg(bg)
        
        # blackhole animation
        index += 1
        if index == 49:
            index = 0
        variables.screen.blit(blackhole[index], (variables.SCREEN_WIDTH // 6, 10))

        #actions depending on clicked buttons
        if variables.continue_button.draw(variables.screen):
            return 0 #go to phase menu function
        if variables.new_game_button.draw(variables.screen):
            return 1 #new game
        if variables.shopping_button.draw(variables.screen):
            return 2 #go to the market
        
        #quit game
        if functions.event_handlers():
            return -1

        pygame.display.update()
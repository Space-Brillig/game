import pygame
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

#load title screen buttons' images
continue_button_img = pygame.image.load('assets/sprites/buttons/continue.jpeg').convert_alpha()
new_game_button_img = pygame.image.load('assets/sprites/buttons/continue.jpeg').convert_alpha()
shopping_button_img = pygame.image.load('assets/sprites/buttons/continue.jpeg').convert_alpha()

#create title screen buttons' instances
continue_button = buttons.Button(continue_button_img, 0.6)
new_game_button = buttons.Button(new_game_button_img, 0.6)
shopping_button = buttons.Button(shopping_button_img, 0.6)
button_width = continue_button.image.get_width()

#load blackhole' images
blackhole = []
for i in range (1, 50):
    blackhole.append(pygame.image.load(f"assets/sprites/background/blackhole/frame-{i}.gif").convert())
    blackhole[i - 1] = pygame.transform.scale(blackhole[i - 1], (int(blackhole[i - 1].get_width() * 2), int(blackhole[i - 1].get_height() * 2)))
blackhole_width = blackhole[0].get_width()

#Title Screen function
def Title_screen():

    #setting the background
    bg = pygame.image.load("assets/sprites/background/space.png").convert()
    index = 0

    while True:
        
        #set fps
        variables.clock.tick(variables.fps)
        bg = pygame.transform.scale(bg, (variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT))
        functions.draw_bg(bg)

        functions.display_bitcoins('white')
        
        # blackhole animation
        index += 1
        if index == 49:
            index = 0
        variables.screen.blit(blackhole[index], (variables.SCREEN_WIDTH // 2 - blackhole_width * 0.5, -40))

        #actions depending on clicked buttons
        if continue_button.draw(variables.screen, variables.SCREEN_WIDTH // 2 - button_width * 0.5, variables.SCREEN_HEIGHT // 2):
            return 0 #go to phase menu function
        if new_game_button.draw(variables.screen, variables.SCREEN_WIDTH // 2 - button_width * 0.5, continue_button.rect.y + 120):
            return 1 #new game
        if shopping_button.draw(variables.screen, variables.SCREEN_WIDTH // 2 - button_width * 0.5, new_game_button.rect.y + 120):
            return 2 #go to the market
        
        #quit game
        if functions.event_handlers():
            return -1
        pygame.display.flip()
        pygame.display.update()
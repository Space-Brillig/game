import pygame
import objects.variables as variables

'''
This file contains some of the created ingame
functions and events, used to facilitate some of the
repeated process of each screen
'''

#draw background
def draw_bg(bg):
     
    variables.screen.blit(bg, (0,0))

#darken screen
def darken_screen(song, color):

    pygame.mixer.init()
    alpha = 0
    surface = pygame.Surface((variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT))
    surface.set_alpha(alpha)
    surface.fill(color)
    if not song == False:
        song.fadeout(5000)
    while surface.get_alpha() < 255:
        variables.clock.tick(2)
        alpha += 50
        surface.set_alpha(alpha)
        variables.screen.blit(surface, (0, 0))
        if event_handlers():
            return False
        pygame.display.update()

#event handlers
def event_handlers():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit game
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
        elif event.type == pygame.VIDEORESIZE:
            variables.SCREEN_WIDTH = event.w
            variables.SCREEN_HEIGHT = event.h
            if variables.SCREEN_HEIGHT < 700:
                variables.SCREEN_HEIGHT = 700
            if variables.SCREEN_WIDTH < 700:
                variables.SCREEN_WIDTH = 700
            variables.screen = pygame.display.set_mode((variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT), pygame.RESIZABLE)

#display bitcoins
def display_bitcoins(color):
    points_icon = variables.font.render(str(variables.points), True, color)
    points_width = points_icon.get_width()
    variables.screen.blit(points_icon, (variables.SCREEN_WIDTH - points_width - 20, 12))
    variables.screen.blit(variables.bitcoin_img, (variables.SCREEN_WIDTH - points_width - 75, -5))
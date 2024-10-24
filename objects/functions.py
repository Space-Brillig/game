import pygame
import objects.variables as variables
import characters.projectile as projectile
import characters.alien as alien
from random import randint

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
    surface = pygame.Surface((variables.screen.get_width(), variables.screen.get_height()))
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
            variables.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
#creature spawning function
def spawn_creatures(props): #spawning based on proportions, respectively: alien, meteor and regenerative item

    random = randint(1, props[-1]) #generate a number between 1 and the greatest proportion

    if random <= props[0]: 

        #spawn alien
        Alien = alien.Alien(randint(30, variables.screen.get_width() - 30), randint(-100, -50))
        variables.alien_group.add(Alien)
        return False
    
    elif random <= props[1] and random > props[0]: 

        #spawn meteor
        size = randint(1, 3) #generating random size
        if size == 1:
            #small meteor
            meteor = projectile.Projectile(randint(10, variables.screen.get_width() - 10), randint(-100, -50), 1, True, 1)
            meteor_points = 1
        elif size == 2:
            #medium meteor
            meteor = projectile.Projectile(randint(10, variables.screen.get_width() - 10), randint(-100, -50), 3, True, 1.5)
            meteor_points = 2
        else:
            #big meteor
            meteor = projectile.Projectile(randint(10, variables.screen.get_width() - 10), randint(-100, -50), 5, True, 2)
            meteor_points = 3
        variables.meteor_group.add(meteor)
        
        return meteor_points
    
    elif random > props[0] and random > props[1]:

        #spawn regenerative item
        r_item = projectile.Projectile(randint(10, variables.screen.get_width() - 10), randint(-100, -50), 0.7, False, 0)
        variables.r_item_group.add(r_item)
        return False
    
#clear sprites off screen at function return
def clear_sprites(sprites_groups, bg):
    for variables.sprite_group in sprites_groups:
        for sprite in variables.sprite_group:
            sprite.kill()
            variables.sprite_group.clear(variables.screen, bg)
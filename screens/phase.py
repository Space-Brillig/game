import pygame
from math import ceil
import characters.spaceship as spaceship
import characters.alien as alien
import characters.projectile as projectile
from random import randint
import objects.functions as functions
import objects.variables as variables
import screens.texts as texts

'''
This is the main function to all phases in the game.
Even though each phase is unique, we can distinguish
what changes between phase to phase and just call the same
function but with the wanted parameters. Each phase has different:
- background
- speed of the creatures
- proportions of the spawning function
- quantity of aliens to be caught
- interval of time of the spawning event
'''

#Phase function
def Phase(background, c_speed, props, quota, spawn_event, song):

    #define creature spawning event
    CREATURES_SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(CREATURES_SPAWN_EVENT, spawn_event)  # Spawn every 'spawn_event' milliseconds

    #create spaceship (had to put an 'i' not to confuse lol)
    ispaceship = spaceship.Spaceship(int(variables.SCREEN_WIDTH / 2), variables.SCREEN_HEIGHT - 100)
    variables.spaceship_group.add(ispaceship)

    #define background
    if background != 'chaotic':
        bg = pygame.image.load(background).convert_alpha()
    else:
        chaotic_animation = []
        for i in range(12):
            chaotic_animation.append(pygame.image.load(f'assets/sprites/background/chaotic/SP{i + 1}.png').convert_alpha())
            bg = chaotic_animation[0]
        index = 0
        iterate = 1
        animation_cooldown = pygame.time.get_ticks()
    bg_height = bg.get_height()
    bg_width = bg.get_width()
    scroll = 0

    points_before = variables.points
    caughts = 0
    delay = 0

    action = 5 #-2 if game's quit, -1 if going back, 0 if game's won, 1 if game's over

    run = True
    while run:

        #set fps
        variables.clock.tick(variables.fps)
        if background == 'chaotic':
            time_now = pygame.time.get_ticks()
            if time_now - animation_cooldown > 200:
                index += iterate
                animation_cooldown = time_now
                bg = chaotic_animation[index]
                if index == 11:
                    iterate = -1
                if index == 0:
                    iterate = 1
        bg = pygame.transform.scale(bg, (variables.SCREEN_WIDTH, (variables.SCREEN_WIDTH * bg_height) // bg_width))
        bg_height = bg.get_height()
        bg_width = bg.get_width()
        
        #scrolling background
        if variables.SCREEN_HEIGHT >= bg_height:
            for i in range(0, ceil(variables.SCREEN_HEIGHT // bg_height) + 1):
                variables.screen.blit(bg, (0, - (i * bg_height + scroll)))
        else:
            for i in range(0, ceil(bg_height // variables.SCREEN_HEIGHT) + 1):
                variables.screen.blit(bg, (0, - (i * bg_height + scroll)))
        scroll -= 5
        if abs(scroll) > bg_height:
            scroll = 0

        #come back to phase menu
        if variables.back_button.draw(variables.screen, 10, 10):
            action = -1 #come back

        #update spaceship and check if game's over
        if ispaceship.update() == False:
            action = 1 #game over

        #update space groups
        for clt in variables.clt_group:
            if clt.update():
                variables.points += meteor_points #points by wrecking a meteor
        for alien in variables.alien_group:
            if alien.update(c_speed, ispaceship):
                variables.points += 8 #points by catching alien
                caughts += 1

        variables.meteor_group.update(ispaceship, c_speed)
        variables.r_item_group.update(ispaceship, c_speed)

        #draw sprite groups
        variables.spaceship_group.draw(variables.screen)
        variables.clt_group.draw(variables.screen)
        variables.alien_group.draw(variables.screen)
        variables.r_item_group.draw(variables.screen)
        variables.meteor_group.draw(variables.screen)
        
        #event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #the phase hasn't being concluded, so the adquired points mustn't be counted
                variables.points = points_before
                action = -2 #quit game
            elif event.type == CREATURES_SPAWN_EVENT: #spawn creatures
                spawn_result = spawn_creatures(props)
                if spawn_result:
                    meteor_points = spawn_result
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = -1
            elif event.type == pygame.VIDEORESIZE:
                variables.SCREEN_WIDTH = event.w
                variables.SCREEN_HEIGHT = event.h
                if variables.SCREEN_HEIGHT < 700:
                    variables.SCREEN_HEIGHT = 700
                if variables.SCREEN_WIDTH < 700:
                    variables.SCREEN_WIDTH = 700
                variables.screen = pygame.display.set_mode((variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT), pygame.RESIZABLE)

        #check if the quota is reached
        if caughts == quota:
            action = 0 #game won

        #display bitcoins and number of caught aliens on screen
        caughts_icon = variables.font.render(f'RECRUTADOS: {caughts}/{quota}', True, 'white')
        caughts_width = caughts_icon.get_width()
        variables.screen.blit(caughts_icon, (variables.SCREEN_WIDTH // 2 - caughts_width * 0.5, 10))
        functions.display_bitcoins('white')

        if action != 5:
            if action == 0 or action == 1:
                #little delay before changing screen
                delay += 1
                if delay == 10:
                    run = False
            else:
                run = False
        
        pygame.display.update()
    
    #the phase hasn't being concluded, so the adquired points mustn't be counted
    if action == -1 or action == -2 or action == 1:
        pygame.mixer.init()
        song.stop()
        variables.points = points_before
    
    #phase final dialogue
    if action == 0:
        text = [
            'Muito bom, [player_name]!',
            'Já deu a nossa cota por hoje.',
            'Vamos voltar para a estação espacial...',
            '                             Phase passed'
        ]
    elif action == 1:
        text = [
            'Augh... Vamos recuar, [player_name]!',
            'Esta nave precisa de reparos...',
            '                             Phase not passed'
        ]
    if action == 0 or action == 1:
        functions.darken_screen(song, (0, 0, 0))
        if not texts.dialogue(text, False, False, True, "white",False):
            action = -2

    clear_sprites([variables.spaceship_group, variables.clt_group, variables.alien_group, variables.r_item_group, variables.meteor_group], bg)

    return action

#creature spawning function
def spawn_creatures(props): #spawning based on proportions, respectively: alien, meteor and regenerative item

    random = randint(1, props[-1]) #generate a number between 1 and the greatest proportion

    if random <= props[0]: 

        #spawn alien
        Alien = alien.Alien(randint(variables.SCREEN_WIDTH // 6, int(variables.SCREEN_WIDTH * (5/6))), randint(-100, -50))
        variables.alien_group.add(Alien)
        return False
    
    elif random <= props[1] and random > props[0]: 

        #spawn meteor
        size = randint(1, 3) #generating random size
        if size == 1:
            #small meteor
            meteor = projectile.Projectile(randint(10, variables.SCREEN_WIDTH - 10), randint(-100, -50), 2, True, 1)
            meteor_points = 1
        elif size == 2:
            #medium meteor
            meteor = projectile.Projectile(randint(variables.SCREEN_WIDTH // 6, int(variables.SCREEN_WIDTH * (5/6))), randint(-100, -50), 3, True, 1.5)
            meteor_points = 2
        else:
            #big meteor
            meteor = projectile.Projectile(randint(variables.SCREEN_WIDTH // 4, int(variables.SCREEN_WIDTH * (3/4))), randint(-100, -50), 4, True, 2)
            meteor_points = 3
        variables.meteor_group.add(meteor)
        
        return meteor_points
    
    elif random > props[0] and random > props[1]:

        #spawn regenerative item
        r_item = projectile.Projectile(randint(variables.SCREEN_WIDTH // 4, int(variables.SCREEN_WIDTH * (3/4))), randint(-100, -50), 0.7, False, 0)
        variables.r_item_group.add(r_item)
        return False
    
#clear sprites off screen at function return
def clear_sprites(sprites_groups, bg):
    for variables.sprite_group in sprites_groups:
        for sprite in variables.sprite_group:
            sprite.kill()
            variables.sprite_group.clear(variables.screen, bg)
import pygame
import math
import characters.spaceship as spaceship
import objects.functions as functions
import objects.variables as variables

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
def Phase(background, c_speed, props, quota, spawn_event):

    #define creature spawning event
    CREATURES_SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(CREATURES_SPAWN_EVENT, spawn_event)  # Spawn every 'spawn_event' milliseconds

    #create spaceship (had to put an 'i' not to confuse lol)
    ispaceship = spaceship.Spaceship(int(variables.SCREEN_WIDTH / 2), variables.SCREEN_HEIGHT - 100, variables.lifebar, variables.clt_speed)
    variables.spaceship_group.add(ispaceship)

    #define background
    bg = pygame.image.load(background).convert()
    bg = pygame.transform.scale(bg, (variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT))
    bg_height = bg.get_height()
    scroll = 0

    points_before = variables.points
    caughts = 0 #number of caught aliens

    action = 0 #-1 if going back, -2 if game's quit, 0 if game's won, 1 if game's over

    run = True
    while run:

        #set fps
        variables.clock.tick(variables.fps)

        functions.draw_bg(bg)
        
        #scrolling background
        for i in range(0, math.ceil(variables.SCREEN_HEIGHT  / bg_height) + 1):
            variables.screen.blit(bg, (0, - (i * bg_height + scroll)))
        scroll -= 5
        if abs(scroll) > bg_height:
            scroll = 0

        #come back to phase menu
        if variables.back_button.draw(variables.screen):
            #the phase hasn't being concluded, so the adquired points mustn't be counted
            variables.points = points_before
            action = -1 #come back
            run = False

        #update spaceship and check if game's over
        if ispaceship.update(variables.SCREEN_HEIGHT, variables.SCREEN_WIDTH, variables.screen) == False:
            action = 1 #game over
            run = False

        #update space groups
        for clt in variables.clt_group:
            if clt.update(variables.SCREEN_HEIGHT, ispaceship, variables.clt_speed):
                variables.points += meteor_points #points by wrecking a meteor
                print (variables.points)
        for alien in variables.alien_group:
            if alien.update(variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT, c_speed, ispaceship):
                variables.points += alien_points #points by catching alien
                print (variables.points)
                caughts += 1
        variables.meteor_group.update(variables.SCREEN_HEIGHT, ispaceship, c_speed)
        variables.r_item_group.update(variables.SCREEN_HEIGHT, ispaceship, c_speed)

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
                run = False
            elif event.type == CREATURES_SPAWN_EVENT: #spawn creatures
                spawn_result = functions.spawn_creatures(props)
                if spawn_result == 8:
                    alien_points = spawn_result
                elif spawn_result:
                    meteor_points = spawn_result

        #check if the quota is reached
        if caughts == quota:
            action = 0 #game won
            run = False

        pygame.display.update()
    
    functions.clear_sprites([variables.spaceship_group, variables.clt_group, variables.alien_group, variables.r_item_group, variables.meteor_group], bg)
    
    return action
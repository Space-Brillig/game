import pygame
import math
import characters
import functions
import variables

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

    #clear sprites off screen at function return
    def clear_sprites(sprites_groups):
        for characters.sprite_group in sprites_groups:
            for sprite in characters.sprite_group:
                sprite.kill()
                characters.sprite_group.clear(variables.screen, bg)

    #define creature spawning event
    CREATURES_SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(CREATURES_SPAWN_EVENT, spawn_event)  # Spawn every 'spawn_event' milliseconds

    #create spaceship
    spaceship = characters.Spaceship(int(variables.SCREEN_WIDTH / 2), variables.SCREEN_HEIGHT - 100, variables.lifebar, variables.clt_speed, True)
    characters.spaceship_group.add(spaceship)

    #define background
    bg = pygame.image.load(background).convert()
    bg = pygame.transform.scale(bg, (variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT))
    bg_height = bg.get_height()
    scroll = 0

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
            functions.mouse_release()
            action = -1 #come back
            run = False

        #update spaceship and check if game's over
        if spaceship.update(variables.SCREEN_HEIGHT, variables.SCREEN_WIDTH, variables.screen, variables.spaceship_speed, variables.pulse_speed) == False:
            action = 1 #game over
            run = False

        #update space groups
        for clt in characters.clt_group:
            if clt.update():
                variables.points += 3 #points by wrecking a meteor
                print (variables.points)
        for alien in characters.alien_group:
            if alien.update(variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT, c_speed, spaceship):
                variables.points += 8 #points by catching alien
                print (variables.points)
                caughts += 1
        characters.meteor_group.update(variables.SCREEN_HEIGHT, spaceship, c_speed)
        characters.r_item_group.update(variables.SCREEN_HEIGHT, spaceship, c_speed)

        #draw sprite groups
        characters.spaceship_group.draw(variables.screen)
        characters.clt_group.draw(variables.screen)
        characters.alien_group.draw(variables.screen)
        characters.r_item_group.draw(variables.screen)
        characters.meteor_group.draw(variables.screen)
        
        #event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                action = -2 #quit game
                run = False
            elif event.type == CREATURES_SPAWN_EVENT: #spawn creatures
                functions.spawn_creatures(props)

        #check if the quota is reached
        if caughts == quota:
            action = 0 #game won
            run = False

        pygame.display.update()
    
    clear_sprites([characters.spaceship_group, characters.clt_group, characters.alien_group, characters.r_item_group, characters.meteor_group])
    
    return action
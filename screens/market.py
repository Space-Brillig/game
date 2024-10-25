import pygame
import objects.variables as variables
import objects.functions as functions
import objects.buttons as buttons

#load engines icons
engine_img = pygame.image.load('assets/sprites/spaceship/engines/BaseEngine/Engine/BaseEngine.png')
BigPulseEngine = pygame.image.load('assets/sprites/spaceship/engines/BigPulseEngine/Engine/BigPulseEngine.png')
BurstEngine = pygame.image.load('assets/sprites/spaceship/engines/BurstEngine/Engine/BurstEngine.png')
SuperchargedEngine = pygame.image.load('assets/sprites/spaceship/engines/SuperchargedEngine/Engine/SuperchargedEngine.png')

#load shield icons
shield_img = pygame.image.load('assets/sprites/spaceship/shields/RoundShield/shield-12.png')
FrontShield = pygame.image.load('assets/sprites/spaceship/shields/FrontShield/shield-10.png')
FrontSideShield = pygame.image.load('assets/sprites/spaceship/shields/Front&SideShield/shield-1.png')
InvisibilityShield = pygame.image.load('assets/sprites/spaceship/shields/InvisibilityShield/shield-12.png')

buy_img = pygame.image.load('assets/sprites/buttons/buy.jpeg').convert_alpha()
select_img = pygame.image.load('assets/sprites/buttons/select.jpeg').convert_alpha()
selected_icon = pygame.image.load('assets/sprites/buttons/selected.jpeg').convert_alpha()
selected_icon = pygame.transform.scale(selected_icon, (selected_icon.get_width() * 0.15, selected_icon.get_height() * 0.15))

#create icons buttons
engine_icon = buttons.Button(engine_img, 2)
shield_icon = buttons.Button(shield_img, 2)
buy1_button = buttons.Button(buy_img, 0.2)
buy2_button = buttons.Button(buy_img, 0.2)
buy3_button = buttons.Button(buy_img, 0.2)
buy4_button = buttons.Button(buy_img, 0.2)
select1_button = buttons.Button(select_img, 0.2)
select2_button = buttons.Button(select_img, 0.2)
select3_button = buttons.Button(select_img, 0.2)
select4_button = buttons.Button(select_img, 0.2)

rect = pygame.Rect(200, 500, 200, 300)

def Market():
    while True:

        #set fps
        variables.clock.tick(variables.fps)

        #set background
        variables.screen.fill((255, 255, 255))

        #display bitcoins
        points_icon = variables.font.render(f'BITCOINS: {variables.points}', True, 'black')
        points_width = points_icon.get_width()
        variables.screen.blit(points_icon, (variables.SCREEN_WIDTH // 2 - points_width * 0.5, 10))

        #go back
        if variables.back_button.draw(variables.screen, 10, 10):
            return False

        #buy or select engine
        if engine_icon.draw(variables.screen, 20, variables.SCREEN_HEIGHT // 2):
            
            while True:

                #set fps
                variables.clock.tick(variables.fps)

                #set background
                variables.screen.fill((255, 255, 255))

                #display bitcoins
                points_icon = variables.font.render(f'BITCOINS: {variables.points}', True, 'black')
                points_width = points_icon.get_width()
                variables.screen.blit(points_icon, (variables.SCREEN_WIDTH // 2 - points_width * 0.5, 10))

                #diselect
                if engine_icon.draw(variables.screen, 20, variables.SCREEN_HEIGHT // 2):
                    break

                #go back
                if variables.back_button.draw(variables.screen, 10, 10):
                    return False
                
                #Base Engine
                variables.screen.blit(engine_img, (100, 500))
                buy_select(buy1_button, select1_button, "engine", 0, 50, 100, 600)
                
                #Big Pulse Engine
                variables.screen.blit(BigPulseEngine, (400, 500))
                buy_select(buy2_button, select2_button, "engine", 1, 80, 400, 600)
                
                #Burst Engine
                variables.screen.blit(BurstEngine, (700, 500))
                buy_select(buy3_button, select3_button, "engine", 2, 110, 700, 600)
                
                #Supercharged Engine
                variables.screen.blit(SuperchargedEngine, (1000, 500))
                buy_select(buy4_button, select4_button, "engine", 3, 140, 1000, 600)

                #quit game
                if functions.event_handlers():
                    return True

                pygame.display.update()

        #quit game
        if functions.event_handlers():
            return True
        
        pygame.display.update()

def buy_select(buy_button, select_button, product, product_index, necessary, x, y):
    #buy if it's not bought
    if not variables.bought[product][product_index]:
        if buy_button.draw(variables.screen, x, y):
            
            #buy if there's enough bitcoins
            if variables.points >= necessary:
                variables.bought[product][product_index] = True
                variables.points -= necessary
            
            #throw alert message
            else:
                print ("not enough money!")

    #select if not selected
    elif not variables.selected[product][product_index]:
        if select_button.draw(variables.screen, x, y):
            for i in range (4):
                variables.selected[product][i] = False
            variables.selected[product][product_index] = True
    
    #display selected button
    else:
        variables.screen.blit(selected_icon, (x, y))


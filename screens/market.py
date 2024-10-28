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
InvisibilityShield = pygame.image.load('assets/sprites/spaceship/shields/InvisibilityShield/shield-10.png')

#load buttons' images
buy_img = pygame.image.load('assets/sprites/buttons/buy.jpeg').convert_alpha()
select_img = pygame.image.load('assets/sprites/buttons/select.jpeg').convert_alpha()
selected_icon = pygame.image.load('assets/sprites/buttons/selected.jpeg').convert_alpha()
selected_icon = pygame.transform.scale(selected_icon, (selected_icon.get_width() * 0.15, selected_icon.get_height() * 0.15))

#create icons buttons
engine_icon = buttons.Button(engine_img, 2)
shield_icon = buttons.Button(shield_img, 2)
buy_button = []
select_button = []
for i in range (4):
    buy_button.append(buttons.Button(buy_img, 0.2))
    select_button.append(buttons.Button(select_img, 0.2))

rect = pygame.Rect(200, 500, 200, 300)

def Market():
    upgrade_result = None
    while True:

        #set fps
        variables.clock.tick(variables.fps)

        #set background
        variables.screen.fill((255, 255, 255))

        functions.display_bitcoins('black')

        #go back
        if variables.back_button.draw(variables.screen, 10, 10):
            return False

        #buy or select engine
        if engine_icon.draw(variables.screen, variables.SCREEN_WIDTH // 12, variables.SCREEN_HEIGHT * (1/3)):
            upgrade_result = upgrade("engine", [80, 140, 200, 300], engine_img, BigPulseEngine, BurstEngine, SuperchargedEngine)

        #buy or select shield
        if shield_icon.draw(variables.screen, variables.SCREEN_WIDTH // 12, variables.SCREEN_HEIGHT * (2/3)):
            upgrade_result = upgrade("shield", [150, 270, 390, 500], FrontShield, FrontSideShield, shield_img, InvisibilityShield)

        if upgrade_result == False:
            return False #go back
        elif upgrade_result == True:
            return True #quit game
            
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

def upgrade(product, necessary, icon1, icon2, icon3, icon4):
    while True:

        #set fps
        variables.clock.tick(variables.fps)

        #set background
        variables.screen.fill((255, 255, 255))

        #display bitcoins
        functions.display_bitcoins('black')

        #diselect
        if engine_icon.draw(variables.screen, variables.SCREEN_WIDTH // 12, variables.SCREEN_HEIGHT * (1/3)) or shield_icon.draw(variables.screen, variables.SCREEN_WIDTH // 12, variables.SCREEN_HEIGHT * (2/3)):
            break

        #go back
        if variables.back_button.draw(variables.screen, 10, 10):
            return False
        
        #1st upgrade
        variables.screen.blit(icon1, (variables.SCREEN_WIDTH // 3, variables.SCREEN_HEIGHT * (3/7)))
        buy_select(buy_button[0], select_button[0], product, 0, necessary[0], variables.SCREEN_WIDTH // 3, variables.SCREEN_HEIGHT * (3/7) + 100)
        
        #2nd upgrade
        variables.screen.blit(icon2, (variables.SCREEN_WIDTH // 2, variables.SCREEN_HEIGHT * (3/7)))
        buy_select(buy_button[1], select_button[1], product, 1, necessary[1], variables.SCREEN_WIDTH // 2, variables.SCREEN_HEIGHT * (3/7) + 100)
        
        #3rd upgrade
        variables.screen.blit(icon3, (variables.SCREEN_WIDTH * (2/3), variables.SCREEN_HEIGHT * (3/7)))
        buy_select(buy_button[2], select_button[2], product, 2, necessary[2], variables.SCREEN_WIDTH * (2/3), variables.SCREEN_HEIGHT * (3/7) + 100)
        
        #4th upgrade
        variables.screen.blit(icon4, (variables.SCREEN_WIDTH * (5/6), variables.SCREEN_HEIGHT * (3/7)))
        buy_select(buy_button[3], select_button[3], product, 3, necessary[3], variables.SCREEN_WIDTH * (5/6), variables.SCREEN_HEIGHT * (3/7) + 100)

        #quit game
        if functions.event_handlers():
            return True

        pygame.display.update()
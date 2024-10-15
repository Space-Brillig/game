import pygame
import buttons
import characters
import math
from random import randint
pygame.init()

#define fps
clock = pygame.time.Clock()

#define screen and screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brillig: The Extraordinary Jobs Galaxy!")

#load title screen buttons' images
continue_button_img = pygame.image.load('src/sprites/buttons/continue.jpeg').convert_alpha()
new_game_button_img = pygame.image.load('src/sprites/buttons/new_game.jpeg').convert_alpha()

#create title screen buttons' instances
continue_button = buttons.Button(110, 100, continue_button_img, 0.8)
new_game_button = buttons.Button(100, 700, new_game_button_img, 0.8)

#load Phase Menu buttons' images
phase_img = pygame.image.load('src/sprites/buttons/continue.jpeg').convert_alpha()

#create Phase Menu buttons' instances
phase1_button = buttons.Button(100, 300, phase_img, 0.5)
phase2_button = buttons.Button(100, 400, phase_img, 0.5)
phase3_button = buttons.Button(100, 500, phase_img, 0.5)

#global variables
points = 0
speed = 8
shooting_speed = 10
lifebar = 1
phases = [True, True, True]

#creature spawning function
def spawn_creatures(props): #spawning based on proportions, respectively: alien, meteor and regenerative item

    random = randint(1, props[-1]) #generate a number between 1 and the greatest proportion

    if random <= props[0]: #spawn alien

        alien = characters.Alien(randint(30, SCREEN_WIDTH - 30), randint(-100, -50))
        characters.alien_group.add(alien)
    
    elif random <= props[-2] and random > props[0]: #spawn meteor

        meteor = characters.Meteor(randint(10, SCREEN_WIDTH - 10), randint(-100, -50), 0.05, "meteor", True)
        characters.meteor_group.add(meteor)
    
    elif random <= props[-1] and random <= props[-2]: #spawn regenerative item

        meteor = characters.Meteor(randint(10, SCREEN_WIDTH - 10), randint(-100, -50), 0.7, "r_item", False)
        characters.meteor_group.add(meteor)

#draw background
def draw_bg(bg):
     
    screen.blit(bg, (0,0))

#event handlers
def event_handlers():

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit game
            return True

#Title Screen function
def title_screen():

    #setting the background
    bg = pygame.image.load("src/sprites/background/space.png").convert()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    i = 0

    run = True
    while run:
        
        clock.tick(80)

        draw_bg(bg)
        
        # blackhole animation
        i += 1
        if i == 50:
            i = 1
        blackhole = pygame.image.load(f"src/sprites/background/blackhole/frame-{i}.gif").convert()
        blackhole = pygame.transform.scale(blackhole, (int(blackhole.get_width() * 2), int(blackhole.get_height() * 2)))
        screen.blit(blackhole, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100))

        #actions depending on clicked buttons
        if continue_button.draw(screen):
            return (0) #calls the phase_menu function
        if new_game_button.draw(screen):
            return (1) #clear global variables
        
        if event_handlers():
            run = False

        pygame.display.update()

#Phase Menu function
def phase_menu():
    
    run = True
    while run:  

        clock.tick(80)

        screen.fill((100, 100, 240))

        #actions depending on clicked buttons
        if phase1_button.draw(screen):

            return (0) #calls the phase function with phase 1 parameters
        
        if phases[0] == True:
            if phase2_button.draw(screen):
        
                return (1) #calls the phase function with phase 2 parameters
        
        else:
            rect = pygame.Rect(100, 400, 150, 100)
            pygame.draw.rect(screen, (255, 0, 255), rect)
        
        if phases[1] == True:
            if phase3_button.draw(screen):
                return (2) #calls the phase function with phase 3 parameters
        
        else:
            rect = pygame.Rect(100, 500, 150, 100)
            pygame.draw.rect(screen, (255, 0, 255), rect)
        
        if event_handlers():
            run = False

        pygame.display.update()

#Phase function
def phase(background, c_speed, props, quota, spawn_event):

    global points

    #define creature spawning event
    CREATURES_SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(CREATURES_SPAWN_EVENT, spawn_event)  # Spawn every 'spawn_event' milliseconds

    #create spaceship
    spaceship = characters.Spaceship(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 100, lifebar, speed, shooting_speed)
    characters.spaceship_group.add(spaceship)

    #define background
    bg = pygame.image.load(background).convert()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_height = bg.get_height()
    scroll = 0

    caughts = 0 #number of caught aliens

    run = True
    while run:

        clock.tick(80)

        draw_bg(bg)
        
        #scrolling background
        for i in range(0, math.ceil(SCREEN_HEIGHT  / bg_height) + 1):
            screen.blit(bg, (0, - (i * bg_height + scroll)))
        scroll -= 5
        if abs(scroll) > bg_height:
            scroll = 0

        #update spaceship
        if spaceship.update(SCREEN_HEIGHT, SCREEN_WIDTH, screen) == False:
            pygame.display.update()
            return 1 #game over

        #update space groups
        characters.clt_group.update()
        for alien in characters.alien_group:
            if alien.update(SCREEN_WIDTH, SCREEN_HEIGHT, c_speed):
                points += 10
                print (points)
                caughts += 1
        characters.meteor_group.update(SCREEN_HEIGHT, spaceship, c_speed)

        #draw sprite groups
        characters.spaceship_group.draw(screen)
        characters.clt_group.draw(screen)
        characters.alien_group.draw(screen)
        characters.meteor_group.draw(screen)
        
        #event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                spaceship.kill()
                pygame.display.update()
                run = False
                return 2 #quit game
            elif event.type == CREATURES_SPAWN_EVENT: #spawn creatures
                spawn_creatures(props)

        if caughts == quota:
            return 0 #game won

        pygame.display.update()

#Main game logic
def main():
    
    title_result = title_screen() #storing the user's choice

    if title_result == 0:

        while True: #looping between phases_menu and the phases

            phase_menu_result = phase_menu()
            
            if phase_menu_result == 0:
                phase_result = phase("src/sprites/background/bg.png", 5, [5, 10, 15], 20, 1500) #phase 1 parameters
                if phase_result == 0:
                    phases[0] = True #phase is passed
            
            elif phase_menu_result == 1:
                phase_result = phase("src/sprites/background/space.png", 7, [4, 12, 17], 30, 1000) #phase 2 parameters
                if phase_result == 0:
                    phases[-2] = True #phase is passed
            
            elif phase_menu_result == 2:
                phase_result = phase("src/sprites/background/bg.png", 10, [2, 20, 25], 45, 500) #phase 3 parameters
                if phase_result == 0:
                    phases[-1] = True #phase is passed
            
            else:
                break
            
            if phase_result == 2:
                break

    elif title_result == 1: #reboot global variables (new game)
        print ("calma voy")
    else:
        pygame.quit()

main()
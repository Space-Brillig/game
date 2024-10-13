import pygame
import buttons
import characters
import math
from random import randint
pygame.init()

#define fps
clock = pygame.time.Clock()
fps = 60

#define screen size
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

#define creature spawning event
CREATURES_SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(CREATURES_SPAWN_EVENT, 1500)  # Spawn every 1500 milliseconds

#creature spawning function
def spawn_creatures(a_prop, m_prop, r_prop): #spawning based on proportions, respectively: alien, meteor and regenerative item

    props = [a_prop, m_prop, r_prop]
    props.sort()
    random = randint(1, props[2])
    for item in props:
        if item == a_prop and random <= item:
            alien = characters.Alien(randint(30, SCREEN_WIDTH - 30), randint(-100, -50))
            characters.alien_group.add(alien)
            break
        elif item == m_prop and random <= item:
            meteor = characters.Meteor(randint(10, SCREEN_WIDTH - 10), randint(-100, -50), 0.05, "meteor", True)
            characters.meteor_group.add(meteor)
            break
        elif item == r_prop and random <= item:
            meteor = characters.Meteor(randint(10, SCREEN_WIDTH - 10), randint(-100, -50), 0.7, "r_item", False)
            characters.meteor_group.add(meteor)
            break

#create spaceship
spaceship = characters.Spaceship(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 100, 5)
characters.spaceship_group.add(spaceship)

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

    clock.tick(fps - 30)

    #setting the background
    bg = pygame.image.load("src/sprites/background/space.png").convert()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    i = 0

    run = True
    while run:
        
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

        screen.fill((100, 100, 240))

        #actions depending on clicked buttons
        if phase1_button.draw(screen):
            return (0) #calls the phase function with phase 1 parameters
        if phase2_button.draw(screen):
            return (1) #calls the phase function with phase 2 parameters
        if phase3_button.draw(screen):
            return (2) #calls the phase function with phase 3 parameters
        
        if event_handlers():
            run = False

        pygame.display.update()

#Phase function
def phase(background):

    #define background
    bg = pygame.image.load(background).convert()
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_height = bg.get_height()
    scroll = 0

    run = True
    while run:

        clock.tick(fps)

        draw_bg(bg)
        
        #scrolling background
        for i in range(0, math.ceil(SCREEN_HEIGHT  / bg_height) + 1):
            screen.blit(bg, (0, - (i * bg_height + scroll)))
        scroll -= 5
        if abs(scroll) > bg_height:
            scroll = 0

        #update spaceship
        spaceship.update(SCREEN_HEIGHT, SCREEN_WIDTH, screen)

        #update space groups
        characters.clt_group.update()
        characters.alien_group.update(SCREEN_WIDTH, SCREEN_HEIGHT)
        characters.meteor_group.update(SCREEN_HEIGHT, spaceship)

        #draw sprite groups
        characters.spaceship_group.draw(screen)
        characters.clt_group.draw(screen)
        characters.alien_group.draw(screen)
        characters.meteor_group.draw(screen)
        
        #event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #quit game
                run = False
            elif event.type == CREATURES_SPAWN_EVENT: #spawn creatures
                spawn_creatures(5, 7, 10)

        pygame.display.update()

#Main game logic
def main():

    title_result = title_screen()

    if title_result == 0:

        phase_result = phase_menu()
        if phase_result == 0:
            phase("src/sprites/background/bg.png") #phase 1
        elif phase_result == 1:
            phase("src/sprites/background/space.png") #phase 2
        elif phase_result == 2:
            phase("src/sprites/background/bg.png") #phase 3

    elif title_result == 1:
        phase() 
    else:
        pygame.quit()

main()
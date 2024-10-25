import pygame
import objects.variables as variables
import objects.functions as functions

pygame.mixer.init()

pygame.font.init()

#set dialogue text
font = pygame.font.Font('freesansbold.ttf', 24)

def dialogue(text, background, text_box, hasfade, color, song):
    
    #load background image
    if not background == False:
        bg = pygame.image.load('assets/sprites/background/initialscenebackground.png')
        bg = pygame.transform.scale(bg, (variables.screen.get_width(), variables.screen.get_height()))

    if not song == False:
        song.play(-1)
    sentence = font.render('', True, 'white')   
    index = 0
    counter = 0
    speed = 3
    done = False
    
    while True:

        #set background
        if not background == False:
            functions.draw_bg(bg)
        else:
            pygame.draw.rect(variables.screen, 'black', [0, 0, variables.screen.get_width(), variables.screen.get_height()])

        #set fps
        variables.clock.tick(60)

        #set box text
        if not text_box == False:
            pygame.draw.rect(variables.screen, 'grey', [0, 500, 800, 300])

        #check if sentence is fully drawn into the screen
        if counter < speed * len(text[index]):
            counter += 1
        elif counter >= speed * len(text[index]):
            done = True

        #next sentence if space is pressed
        key = pygame.key.get_pressed()
        if (key[pygame.K_RETURN] or key[pygame.K_SPACE] or pygame.mouse.get_pressed()[0] == 1) and done and index < len(text):
            index += 1
            done = False
            counter = 0

        #quit game
        if functions.event_handlers():
            return False
        
        #text is finished
        if index == len(text):
            if hasfade:
                functions.darken_screen(song, color)
            variables.screens[0] = True
            return True
        
        #piece of text drawn into the screen
        if not background == False:
            sentence = font.render(text[index][0:counter//speed], True, 'black')
        else:
            sentence = font.render(text[index][0:counter//speed], True, 'white')
        variables.screen.blit(sentence, (10, 510))

        pygame.display.update()
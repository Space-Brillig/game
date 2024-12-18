import pygame
import objects.variables as variables
import objects.input as input
import objects.functions as functions

pygame.mixer.init()

pygame.font.init()

#set dialogue text

def dialogue(text, background, text_box, hasfade, color, song):
    
    #load background image
    if not background == False:
        bg = pygame.image.load('assets/sprites/background/initialscenebackground.png')

    if not song == False:
        song.play(-1)
    sentence = variables.font.render('', True, 'white')   
    index = 0
    counter = 0
    speed = 3
    done = False
    
    while True:

        #set background
        if not background == False:
            functions.draw_bg(bg)
            bg = pygame.transform.scale(bg, (variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT))
        else:
            pygame.draw.rect(variables.screen, 'black', [0, 0, variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT])

        #set fps
        variables.clock.tick(60)

        #set textbox
        if not text_box == False:
            pygame.draw.rect(variables.screen, 'grey', [0, 500, variables.SCREEN_WIDTH, 500])

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

        #get player's name input
        if not background == False and index == 2 and variables.player_name == '':
            variables.player_name = input.Input()
            text[3] = f'Ah... sim... deixe-me te contar uma história, {variables.player_name}...'
            index += 1

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
            sentence = variables.font.render(text[index][0:counter//speed], True, 'black')
        else:
            sentence = variables.font.render(text[index][0:counter//speed], True, 'white')
        variables.screen.blit(sentence, (10, 510))

        pygame.display.update()
import pygame
import objects.variables as variables
import objects.functions as functions

pygame.mixer.init()

pygame.font.init()

#load background image
bg = pygame.image.load('assets/sprites/background/initialscenebackground.png')
bg = pygame.transform.scale(bg, (variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT))

#set dialogue text
font = pygame.font.Font('freesansbold.ttf', 24)
text = [
'Hum... o que fazes aí? Erm...',
'Qual é o seu nome?',
'Ah... sim... deixe-me te contar uma história, [player_name]...',
'Tudo começou há cerca de 10000 atrás...',
'Numa época em que as bússolas apontavam para o sul...',
'Quando a água não satisfazia a sede...',
'E quando o céu não era azul...',
'Quando os arvoredos não eram verdes...',
'E quando em todas coisas faltava luz...',
'Isto, meu querido...',
'Quando o mundo era Briluz.',
'Você talvez já tenha ouvido falar...',
'Ante a infinita multiplicidade do universo disperso em facetas...',
'Havia um planeta.',
'O planeta mais próspero que você pode imaginar...',
'E era o homem quem ditava as regras neste lugar.',
'Mas, afinal de contas...',
'O que era o homem?',
'O que era o homem, a não ser um bicho...',
'Um bicho egoísta, ganancioso e avarento...',
'. . .',
]

def Initialscreen(song):
    
    song.play(-1)
    sentence = font.render('', True, 'white')   
    index = 0
    counter = 0
    speed = 3
    done = False
    
    while True:

        #set background
        functions.draw_bg(bg)

        #set fps
        variables.clock.tick(60)

        #set box text
        pygame.draw.rect(variables.screen, 'grey', [0, 500, 800, 300])

        #check if sentence is fully drawn into the screen
        if counter < speed * len(text[index]):
            counter += 1
        elif counter >= speed * len(text[index]):
            done = True

        #next sentence if space is pressed
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN] and done and index < len(text):
            index += 1
            done = False
            counter = 0

        #quit game
        if functions.event_handlers():
            return False
        
        #text is finished
        if index == len(text):
            functions.darken_screen(song, (0, 0, 0))
            variables.screens[0] = True
            return True
        
        #piece of text drawn into the screen
        sentence = font.render(text[index][0:counter//speed], True, 'black')
        variables.screen.blit(sentence, (10, 510))

        pygame.display.update()
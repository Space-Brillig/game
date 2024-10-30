import pygame
import screens.texts as texts
import screens.titlescreen as titlescreen
import screens.market as market
import screens.phasemenu as phasemenu
import screens.phase as phase
import objects.variables as variables

pygame.init()

'''
This is the main file of the game, containing
the logic of the screen changing based on the
user's choice. All the other screens of the game appear
here in their practical form of functions
'''

#load game's songs
clairdelune = pygame.mixer.Sound('assets/music/ClairdeLune-Debussy&Vinheteiro.mp3')
sonata_1stmovement = pygame.mixer.Sound('assets/music/MoonlightSonata(1stMovement)-Beethoven&EmilGilels.mp3')
sonata_2ndmovement = pygame.mixer.Sound('assets/music/MoonlightSonata(2ndMovement)-Beethoven&Rosseou.mp3')
sonata_3rdmovement = pygame.mixer.Sound('assets/music/MoonlightSonata(3rdMovement)-Beethoven&Rosseou.mp3')
nocturne = pygame.mixer.Sound('assets/music/NocturneinEbop9no2-Chopin&Rosseou.mp3')
winterwind = pygame.mixer.Sound('assets/music/WinterWind-Chopin&Rosseou.mp3')
preludium = pygame.mixer.Sound('assets/music/PreludiuminCmajor-Bach&TatianaNikolayeva.mp3')

#Main game logic
def main():
    #first interaction
    if not variables.screens[0]:
        text = [
            'Hum... o que fazes aí? Erm...',
            'Qual é o seu nome?',
            '',
            f'Ah... sim... deixe-me te contar uma história, {variables.player_name}...',
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
            '. . .'
            ]
        if not texts.dialogue(text, True, True, True, "black", clairdelune):
            return True

    sonata_1stmovement.play(-1)

    #looping between title_screen and phases_menu
    while True:

        #set fps
        variables.clock.tick(variables.fps)

        #storing the user's choice
        title_screen_result = titlescreen.Title_screen()

        #quit game
        if title_screen_result == -1:
            return True

        if title_screen_result == 0:
            #looping between phases_menu and the phases
            while True:
                
                #storing the user's choice
                phase_menu_result = phasemenu.Phase_menu()

                #go back to title_screen
                if phase_menu_result == -1:
                    break

                #quit game
                elif phase_menu_result == -2:
                    return True
                
                sonata_1stmovement.stop()

                #go to phase 1
                if phase_menu_result == 0:
                    nocturne.play(-1)
                    phase_result = phase.Phase("assets/sprites/background/antdream.png", 5, [10, 15, 17], 10, 1500, nocturne) #phase 1 parameters
                    phase_passed = 1
                
                #go to phase 2
                elif phase_menu_result == 1:
                    sonata_2ndmovement.play(-1)
                    phase_result = phase.Phase("assets/sprites/background/space.png", 7, [4, 12, 17], 20, 1000, sonata_2ndmovement) #phase 2 parameters
                    phase_passed = 2
                
                #go to phase 3
                elif phase_menu_result == 2:
                    winterwind.play(-1)
                    phase_result = phase.Phase("chaotic", 10, [7, 20, 25], 25, 500, winterwind) #phase 3 parameters
                    phase_passed = 3

                #go to phase 4
                elif phase_menu_result == 3:
                    sonata_3rdmovement.play(-1)
                    phase_result = phase.Phase("assets/sprites/background/hampered'stomb.png", 15, [5, 20, 27], 30, 200, sonata_3rdmovement) #phase 4 parameters
                    phase_passed = 4

                elif phase_menu_result == 4:
                    text = [
                        'Hmmmmm... cá estamos de volta...',
                        'Que bom que ainda não dormistes enquanto estava a contar a história',
                        'Foi quando aquele moço com seu nome veio até mim...',
                        '...'
                        'Hmmmm... estão viestes até mim...'
                        'Saiba que desde sempre pus-me a observar a sua nação',
                        'E a observar que em cada conduta da espécie humana',
                        'Os fins de seu fracasso eram os mesmos que a tornava grande',
                        'Agora olhe só para ti, em que condição que te encontras...',
                        'Você e sua espécie:',
                        'Destruíram com o próprio planeta...',
                        'Humilhados, tomaram-me meus fiéis',
                        'E depois de tudo isto ainda vinde a mim?',
                        'O que achas que eu deveria fazer?',
                        'Bem... Irei propor algo que eu sei que não deveria.',
                        'O desespero, o desamparo, o ódio, a guerra...',
                        'Todos os conflitos angustiantes da vida se encontram numa única indagação.',
                        'Por quê?',
                        'Por que viver assim, em injustiça e em desonestidade?',
                        'Não seria bom se vivessemos todos juntos...',
                        'No tipo de mundo onde todos são iguais',
                        'E regidos pelo amor...',
                        '. . .',
                    ]
                    if not texts.dialogue(text, True, True, True, "black", preludium):
                        return True
                    
                    return True -5

                if phase_result == -2:
                    return True #game is closed
                
                elif phase_result == 0:
                    variables.screens[phase_passed] = True #phase is passed
                
                sonata_1stmovement.play(-1)

                pygame.display.update()

        #new game
        elif title_screen_result == 1:
            #reboot global variables
            variables.player_name = ''

            variables.selected = {"sprite": [True], "engine": [True, False, False, False], "shield": [True, False, False, False]}
            variables.bought = {"engine": [True, False, False, False], "shield": [True, False, False, False]}
            
            variables.points = 100
            variables.clt_speed = 20
            variables.lifebar = 10
            variables.screens = [False, False, False, False, False]

            return False

        #go to the market
        elif title_screen_result == 2:
            market_result = market.Market()
            if market_result:
                return True

while True:
    main_result = main()
    if main_result:
        break

variables.saveload.save_game_data([variables.points, variables.clt_speed, variables.lifebar, variables.screens, variables.selected, variables.bought, variables.player_name], ["points", "clt_speed", "lifebar", "screens", "selected", "bought", "player_name"])

pygame.quit()
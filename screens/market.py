import pygame
import objects.variables as variables
import objects.functions as functions
import objects.buttons as buttons

#load engines icons
engine_img = pygame.image.load('assets/sprites/spaceship/engines/BaseEngine/Engine/BaseEngine.png')
engine_img = pygame.transform.scale(engine_img, (engine_img.get_width() * 2, engine_img.get_height() * 2))
BigPulseEngine = pygame.image.load('assets/sprites/spaceship/engines/BigPulseEngine/Engine/BigPulseEngine.png')
BigPulseEngine = pygame.transform.scale(BigPulseEngine, (BigPulseEngine.get_width() * 2, BigPulseEngine.get_height() * 2))
BurstEngine = pygame.image.load('assets/sprites/spaceship/engines/BurstEngine/Engine/BurstEngine.png')
BurstEngine = pygame.transform.scale(BurstEngine, (BurstEngine.get_width() * 2, BurstEngine.get_height() * 2))
SuperchargedEngine = pygame.image.load('assets/sprites/spaceship/engines/SuperchargedEngine/Engine/SuperchargedEngine.png')
SuperchargedEngine = pygame.transform.scale(SuperchargedEngine, (SuperchargedEngine.get_width() * 2, SuperchargedEngine.get_height() * 2))
engine_descriptions = ['Pluma (o efeito de fumaça ou energia saindo da nave) de forma padrão,',
                        'quando ela estiver funcionando sem o uso de um booster de velocidade.',
                        'Esse efeito vem do motor base, transmitindo a sensação de que a nave,',
                        'está ativa e em operação normal.',
                       
                       'O "Grande Pulso" é um disparo de energia explosiva que proporciona à nave',
                       'um impulso imediato e rápido. Ele é ativado em momentos críticos, como uma',
                       'manobra de emergência, permitindo que a nave acelere instantaneamente. É',
                       'ideal para fugir de tiros inimigos, desviar de obstáculos ou realizar ataques',
                       'rápidos. Por ser uma explosão curta, o efeito dura apenas alguns segundos',
                       'e depois retorna à velocidade normal da nave.',
                       
                       'Essa pluma emite uma explosão de energia que impulsiona a nave com força',
                       'imediata e poderosa. A pluma é de cor azul intensa, simbolizando o disparo,',
                        'energético. Ela aparece por alguns segundos, transmitindo uma sensação de',
                        'explosão súbita e de alto impacto. Seu efeito visual é mais agressivo e de',
                        'maior escala, com rajadas brilhantes e pulsantes que destacam o momento crítico.',
                        'Após o impulso, a pluma volta ao estado padrão, indicando que a nave',
                        'retorna à sua operação normal.',

                       'Esta pluma surge quando a nave atinge seu estado mais poderoso, ativando um supercarregamento que',
                       'libera uma enorme quantidade de energia. A pluma tem uma cor laranja vibrante, cheia de intensidade',
                        'e com efeitos visuais dramáticos, como faíscas e ondas de choque de energia. Representa o pico de',
                        'de desempenho da nave, transimitindo a ideia de que o motor está operando no limite máximo, com uma',
                        'com uma aceleração e potência impressionantes. Ela é maior e mais explosiva que todas as outras',
                        'plumas, indicando a força massiva do supercarregamento. Ao terminar a pluma retorna ao estado padrão.',
                       ]

#load shield icons
shield_img = pygame.image.load('assets/sprites/spaceship/shields/RoundShield/shield-12.png')
FrontShield = pygame.image.load('assets/sprites/spaceship/shields/FrontShield/shield-10.png')
FrontSideShield = pygame.image.load('assets/sprites/spaceship/shields/Front&SideShield/shield-1.png')
InvisibilityShield = pygame.image.load('assets/sprites/spaceship/shields/InvisibilityShield/shield-10.png')
shield_descriptions = ['Protege apenas a parte frontal da nave, o que o torna o menos eficaz em situações com múltiplas ameaças.',
                       'É mais útil quando a nave está avançando contra inimigos, mas oferece proteção limitada.',

                       'Protege a parte frontal e lateral da nave, sendo eficaz contra ataques direcionados. Embora não cubra a',
                       'parte traseira, é uma boa escolha para enfrentar ondas de inimigos que atacam de frente ou pelos lados.',

                       'Oferece proteção em todas as direções, tornando-se muito versátil em combate. É',
                       'ideal quando a nave está cercada por inimigos ou atacada de múltiplas direções.',

                       'Proporciona proteção total e temporária, permitindo que a nave atravesse qualquer',
                       'ataque sem sofrer danos. É o mais poderoso e ideal para situações críticas',
                       ]

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
    descriptions = [[], [], [], []]
    if product == 'engine':
        for i in range(4):
            descriptions[0].append(variables.mfont.render(engine_descriptions[i], True, 'black'))
        for i in range(4, 10):
            descriptions[1].append(variables.mfont.render(engine_descriptions[i], True, 'black'))
        for i in range(10, 17):
            descriptions[2].append(variables.mfont.render(engine_descriptions[i], True, 'black'))
        for i in range(17, 23):
            descriptions[3].append(variables.mfont.render(engine_descriptions[i], True, 'black'))
    else:
        for i in range(2):
            descriptions[0].append(variables.mfont.render(shield_descriptions[i], True, 'black'))
        for i in range(2, 4):
            descriptions[1].append(variables.mfont.render(shield_descriptions[i], True, 'black'))
        for i in range(4, 6):
            descriptions[2].append(variables.mfont.render(shield_descriptions[i], True, 'black'))
        for i in range(6, 8):
            descriptions[3].append(variables.mfont.render(shield_descriptions[i], True, 'black'))
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
        variables.screen.blit(icon1, (variables.SCREEN_WIDTH // 3, variables.SCREEN_HEIGHT // 12))
        for i in range(len(descriptions[0])):
            variables.screen.blit(descriptions[0][i], (variables.SCREEN_WIDTH // 3 + 150, variables.SCREEN_HEIGHT // 10 + i*25))
        buy_select(buy_button[0], select_button[0], product, 0, necessary[0], variables.SCREEN_WIDTH // 3, variables.SCREEN_HEIGHT // 10 + 80)
        
        #2nd upgrade
        variables.screen.blit(icon2, (variables.SCREEN_WIDTH // 3, variables.SCREEN_HEIGHT // 10 + 200))
        for i in range(len(descriptions[1])):
            variables.screen.blit(descriptions[1][i], (variables.SCREEN_WIDTH // 3 + 150, variables.SCREEN_HEIGHT // 10 + 200 + i*25))
        buy_select(buy_button[1], select_button[1], product, 1, necessary[1], variables.SCREEN_WIDTH // 3, variables.SCREEN_HEIGHT // 10 + 280)
        
        #3rd upgrade
        variables.screen.blit(icon3, (variables.SCREEN_WIDTH // 3, variables.SCREEN_HEIGHT // 10 + 400))
        for i in range(len(descriptions[2])):
            variables.screen.blit(descriptions[2][i], (variables.SCREEN_WIDTH // 3 + 150, variables.SCREEN_HEIGHT // 10 + 400 + i*25))
        buy_select(buy_button[2], select_button[2], product, 2, necessary[2], variables.SCREEN_WIDTH // 3, variables.SCREEN_HEIGHT // 10 + 480)
        
        #4th upgrade
        variables.screen.blit(icon4, (variables.SCREEN_WIDTH // 3, variables.SCREEN_HEIGHT * (5/6)))
        for i in range(len(descriptions[3])):
            variables.screen.blit(descriptions[3][i], (variables.SCREEN_WIDTH // 3 + 150, variables.SCREEN_HEIGHT * (5/6) + i*25))
        buy_select(buy_button[3], select_button[3], product, 3, necessary[3], variables.SCREEN_WIDTH // 3, variables.SCREEN_HEIGHT * (5/6) + 80)

        #quit game
        if functions.event_handlers():
            return True

        pygame.display.update()
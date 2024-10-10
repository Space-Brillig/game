import pygame
import math
pygame.init()

clock = pygame.time.Clock()
fps = 100

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game-Test!")

bg = pygame.image.load("bg.png").convert()
bg_width = bg.get_width()

def draw_bg():
    screen.blit(bg, (0,0))

# for the scrolling background
scroll = 0
bg = pygame.image.load("bg.png").convert()

#Declaring the Spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('spaceship.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()
    
    #set movement on the spaceship
    def movement(self):
		#set movement speed
        speed = 10
		#set a cooldown variable
        cooldown = 500 #milliseconds
         
		#key press and movement
        key = pygame.key.get_pressed()
        if (key[pygame.K_w] or key[pygame.K_UP]) and self.rect.top > 10:
            self.rect.y -= speed
        if (key[pygame.K_a] or key[pygame.K_LEFT]) and self.rect.left > 10:
            self.rect.x -= speed
        if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.rect.bottom < SCREEN_HEIGHT - 10:
            self.rect.y += speed
        if (key[pygame.K_d] or key[pygame.K_RIGHT]) and self.rect.right < SCREEN_WIDTH - 10:
            self.rect.x += speed

        time_now = pygame.time.get_ticks()
        #CLT shooting mechanism
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            clt = CLT(self.rect.centerx, self.rect.top)
            clt_group.add(clt)
            self.last_shot = time_now
        
#CLT class
class CLT(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("clt.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    def movement(self):
        self.rect.y -= 5

#game sprite groups
spaceship_group = pygame.sprite.Group()
clt_group = pygame.sprite.Group()

spaceship = Spaceship(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 100)
spaceship_group.add(spaceship) 

run = True
while run:

    clock.tick(fps)

    draw_bg()
    
    #scrolling background
    for i in range(0, math.ceil(SCREEN_WIDTH  / bg_width) + 1):
        screen.blit(bg, (0, - (i * bg_width + scroll)))
        spaceship_group.draw(screen)
    scroll -= 5
    if abs(scroll) > bg_width:
        scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #move spaceship
    spaceship.movement()

    #draw sprite groups
    spaceship_group.draw(screen)
    clt_group.draw(screen)

    pygame.display.update()
    
pygame.quit()
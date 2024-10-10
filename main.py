import pygame
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

#define background
scroll = 0
bg = pygame.image.load("bg.png").convert()
bg_height = bg.get_width()

def draw_bg():
    screen.blit(bg, (0,0))

#define alien spawning event
ALIEN_SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ALIEN_SPAWN_EVENT, 2500)  # Spawn every 200 milliseconds

#Spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('spaceship.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.last_shot = pygame.time.get_ticks()
    
    #set movement on the spaceship
    def update(self):
        if self.rect.bottom < SCREEN_HEIGHT - 10:
            self.rect.y += 3
		#set movement speed
        speed = 8
		#set a cooldown variable
        cooldown = 500 #milliseconds
         
		#key press and movement
        key = pygame.key.get_pressed()
        if (key[pygame.K_w] or key[pygame.K_UP]) and self.rect.top > 10:
            self.rect.y -= speed + 3
        if (key[pygame.K_a] or key[pygame.K_LEFT]) and self.rect.left > 10:
            self.rect.x -= speed
        if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.rect.bottom < SCREEN_HEIGHT - 10:
            self.rect.y += speed
        if (key[pygame.K_d] or key[pygame.K_RIGHT]) and self.rect.right < SCREEN_WIDTH - 10:
            self.rect.x += speed
        
        #CLT shooting mechanism
        time_now = pygame.time.get_ticks()
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
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

#Alien class
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("shrek.jpeg")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.last_creation = pygame.time.get_ticks()
    
    def update(self):
        self.rect.y += 4
        if pygame.sprite.spritecollide(self, clt_group, False, pygame.sprite.collide_mask):
            self.kill()

#alien spawning function
def create_aliens():
    alien = Alien(randint(10, SCREEN_WIDTH - 20), randint(-100, -50))
    alien_group.add(alien)

#game sprite groups
spaceship_group = pygame.sprite.Group()
clt_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()

#create spaceship
spaceship = Spaceship(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 100)
spaceship_group.add(spaceship) 

run = True
while run:

    clock.tick(fps)

    draw_bg()
    
    #scrolling background
    for i in range(0, math.ceil(SCREEN_HEIGHT  / bg_height) + 1):
        screen.blit(bg, (0, - (i * bg_height + scroll)))
        spaceship_group.draw(screen)
    scroll -= 5
    if abs(scroll) > bg_height:
        scroll = 0

    #update spaceship
    spaceship.update()

    #update space groups
    clt_group.update()
    alien_group.update()

    #draw sprite groups
    spaceship_group.draw(screen)
    clt_group.draw(screen)
    alien_group.draw(screen)
    
    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit game
            run = False
        elif event.type == ALIEN_SPAWN_EVENT: #spawn alien
            create_aliens()

    pygame.display.update()
    
pygame.quit()
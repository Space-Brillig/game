import pygame

#define colours
red = (255, 0, 0)
green = (0, 255, 0)

#Spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health, speed, shooting_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('src/sprites/spaceship/spaceship.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = speed
        self.health_start = health
        self.shooting_speed = shooting_speed
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
    
    #set movement on the spaceship
    def update(self, SURFACE_HEIGHT, SURFACE_WIDTH, SURFACE):
        if self.rect.bottom < SURFACE_HEIGHT - 35:
            self.rect.y += self.speed

		#set a cooldown variable
        cooldown = 500 #milliseconds
         
		#key press and movement
        key = pygame.key.get_pressed()
        if (key[pygame.K_w] or key[pygame.K_UP]) and self.rect.top > 10:
            self.rect.y -= 2 * self.speed
        if (key[pygame.K_a] or key[pygame.K_LEFT]) and self.rect.left > 10:
            self.rect.x -= self.speed
        if (key[pygame.K_s] or key[pygame.K_DOWN] or key[pygame.K_LSHIFT]) and self.rect.bottom < SURFACE_HEIGHT - 35:
            self.rect.y += self.speed
        if (key[pygame.K_d] or key[pygame.K_RIGHT]) and self.rect.right < SURFACE_WIDTH - 10:
            self.rect.x += self.speed
        
        #CLT shooting mechanism
        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            clt = CLT(self.rect.centerx, self.rect.top, self.shooting_speed)
            clt_group.add(clt)
            self.last_shot = time_now

        #update mask
        self.mask = pygame.mask.from_surface(self.image)
        
        #draw health bar
        pygame.draw.rect(SURFACE, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(SURFACE, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        else:
            self.kill()
            return False
        
#CLT class
class CLT(pygame.sprite.Sprite):
    def __init__(self, x, y, shooting_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("src/sprites/clt/clt.png")
        self.rect = self.image.get_rect()
        self.shooting_speed = shooting_speed
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= self.shooting_speed
        if self.rect.bottom < 0 or pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
            self.kill()

#Alien class
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("src/sprites/alien/shrek.jpeg")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.caught = False
    
    def update(self, SURFACE_WIDTH, SURFACE_HEIGHT, speed):
        self.rect.y += speed
        if pygame.sprite.spritecollide(self, clt_group, True, pygame.sprite.collide_mask):
            self.caught = True #catch by collision
            return self.caught

        #drag to the closest side if it's caught
        if self.caught:
            if self.rect.x >= SURFACE_WIDTH // 2:
                self.rect.x += 4
            else:
                self.rect.x -= 4
            self.rect.y += 4

        if self.rect.top > SURFACE_HEIGHT or self.rect.left > SURFACE_WIDTH or self.rect.right < 0:
            self.kill()

#Meteor class
class Meteor(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, image, isharmful):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'src/sprites/meteor/{image}.png')
        self.isharmful = isharmful
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.image = pygame.transform.scale(self.image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, SURFACE_HEIGHT, spaceship, speed):
        self.rect.y += speed
        if self.rect.top > SURFACE_HEIGHT:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()

            #if it's the regenerative item or not
            if self.isharmful:
                spaceship.health_remaining -= 1
            elif spaceship.health_remaining > 0 and spaceship.health_remaining < spaceship.health_start:
                spaceship.health_remaining += 1


#game sprite groups
spaceship_group = pygame.sprite.Group()
clt_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
import pygame

'''
This file contains the classes, functions and methods
inherent to the main charachters of the game:
spaceship, alien, CLT, meteor and regenerative item
'''

#define colours
red = (255, 0, 0)
green = (0, 255, 0)

#Spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health, clt_speed, haspulse):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('src/sprites/spaceship/samples/spaceship.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.clt_speed = clt_speed
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
        self.haspulse = haspulse
        self.animations = [[], []] #idle fire and boost pulse
        #load animation images
        for i in range(1, 4):
            self.animations[0].append(pygame.image.load(f'src/sprites/spaceship/idle/pluma-off{i}.png'))
            self.animations[0][i - 1] = pygame.transform.scale(self.animations[0][i - 1], (int(self.animations[0][i - 1].get_width() * 2), int(self.animations[0][i - 1].get_height() * 2)))
        if self.haspulse:
            for i in range(1, 5):
                self.animations[1].append(pygame.image.load(f'src/sprites/spaceship/movement/pluma-on{i}.png'))
                self.animations[1][i - 1] = pygame.transform.scale(self.animations[1][i - 1], (int(self.animations[1][i - 1].get_width() * 2), int(self.animations[1][i - 1].get_height() * 2)))
            self.p_index = 1 #pulse image index
            self.isonpulse = False #check if it's on pulse to change between animations
        self.i_index = 1 #idle image index
    
    #set movement on the spaceship
    def update(self, SURFACE_HEIGHT, SURFACE_WIDTH, SURFACE, speed, pulse_speed):
        self.speed = speed #return speed to default

        #keep being dragged downwards
        if self.rect.bottom < SURFACE_HEIGHT - 35:
            self.rect.y += self.speed

        #key press and movement
        key = pygame.key.get_pressed()
        #pulse animation
        if key[pygame.K_LSHIFT] and (key[pygame.K_w] or key[pygame.K_UP] or key[pygame.K_a] or key[pygame.K_LEFT] or key[pygame.K_s] or key[pygame.K_DOWN] or key[pygame.K_d] or key[pygame.K_RIGHT]):
            self.speed += pulse_speed
            self.isonpulse = True
            SURFACE.blit(self.animations[1][self.p_index], (self.rect.x - 9.4, self.rect.y + 10))
            self.p_index += 1
            if self.p_index == 4:
                self.p_index = 1
        if (key[pygame.K_w] or key[pygame.K_UP]) and self.rect.top > 10:
            self.rect.y -= 2 * self.speed
        if (key[pygame.K_a] or key[pygame.K_LEFT]) and self.rect.left > 10:
            self.rect.x -= self.speed
        if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.rect.bottom < SURFACE_HEIGHT - 35:
            self.rect.y += self.speed
        if (key[pygame.K_d] or key[pygame.K_RIGHT]) and self.rect.right < SURFACE_WIDTH - 10:
            self.rect.x += self.speed

        #idle fire animation (not on pulse)
        if not self.isonpulse:
            SURFACE.blit(self.animations[0][self.i_index], (self.rect.x - 9.2, self.rect.y + 10))
            self.i_index += 1
            if self.i_index == 3:
                self.i_index = 1

        self.isonpulse = False
        
        #CLT shooting mechanism
        cooldown = 500 #cooldown variable
        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            clt = CLT(self.rect.centerx, self.rect.top, self.clt_speed)
            clt_group.add(clt)
            self.last_shot = time_now

        #update mask
        self.mask = pygame.mask.from_surface(self.image)
        
        #draw health bar
        pygame.draw.rect(SURFACE, red, (self.rect.x, (self.rect.top - 20), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(SURFACE, green, (self.rect.x, (self.rect.top - 20), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        else:
            self.kill()
            return False #out of life
        
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
            return True
        if self.rect.bottom < 0 or pygame.sprite.spritecollide(self, r_item_group, True, pygame.sprite.collide_mask):
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
    
    def update(self, SURFACE_WIDTH, SURFACE_HEIGHT, speed, spaceship):
        self.rect.y += speed
        
        #catch by collision
        if pygame.sprite.spritecollide(self, clt_group, True, pygame.sprite.collide_mask) and self.caught == False:
            self.caught = True
            return self.caught

        #drag to the closest side if it's caught
        if self.caught:
            if self.rect.x >= SURFACE_WIDTH // 2:
                self.rect.x += 4
            else:
                self.rect.x -= 4
            self.rect.y += 4

        #drag by collision with the spaceship
        if pygame.sprite.spritecollide(self, spaceship_group, None, pygame.sprite.collide_mask):
            if spaceship.rect.y >= self.rect.y:
                self.rect.y -= spaceship.speed #upwards if collision from bottom
            else:
                self.rect.y += spaceship.speed #downwards if collision from top 
            
            if spaceship.rect.x >= self.rect.x:
                self.rect.x -= spaceship.speed #rightward if collision from left
            else:
                self.rect.x += spaceship.speed #leftward if collision from right

        if self.rect.top > SURFACE_HEIGHT or self.rect.left > SURFACE_WIDTH or self.rect.right < 0:
            self.kill()

#Projectile class (Meteor and Regenerative item)
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, image, isharmful):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'src/sprites/projectile/{image}.png')
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

            #whether it's the regenerative item or not
            if self.isharmful:
                spaceship.health_remaining -= 1
            elif spaceship.health_remaining > 0 and spaceship.health_remaining < spaceship.health_start:
                spaceship.health_remaining += 1

#game sprite groups
spaceship_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
clt_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
r_item_group = pygame.sprite.Group()
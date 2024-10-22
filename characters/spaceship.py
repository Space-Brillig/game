import pygame
import characters.projectile as projectile
import objects.variables as variables

#define colours
red = (255, 0, 0)
green = (0, 255, 0)

#Spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        if variables.plumes["sprite"]:
            self.image = pygame.image.load('assets/sprites/spaceship/samples/spaceship-0.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
        
        #set correct lengths depending on the selected engine
        if variables.plumes["engine"].index(True) == 0:
            engine_now = "BaseEngine"
            self.speed = 5
            length_on = 4
            length_off = 3
            self.e_coordon = (0, 8)
            self.e_coordff = self.e_coordon
        elif variables.plumes["engine"].index(True) == 1:,
            engine_now = "BigPulseEngine"
            self.speed = 6
            length_on = 4
            length_off = 4
            self.e_coordon = (32, 76)
            self.e_coordff = (-1, 10)
        elif variables.plumes["engine"].index(True) == 2:
            engine_now = "BurstEngine"
            self.speed = 7
            length_on = 6
            length_off = 7
            self.e_coordon = (39, 78)
            self.e_coordff = self.e_coordon
        elif variables.plumes["engine"].index(True) == 3:
            engine_now = "SuperchargedEngine"
            self.speed = 8
            length_on = 4
            length_off = 4
            self.e_coordon = (29, 80)
            self.e_coordff = self.e_coordon
        
        self.animations = [[], []] #engine on and engine off
        
        #load animation images
        for i in range(length_on): #on
            self.animations[0].append(pygame.image.load(f'assets/sprites/spaceship/engines/{engine_now}/on/on{i + 1}.png'))
            self.animations[0][i] = pygame.transform.scale(self.animations[0][i], (int(self.animations[0][i].get_width() * 2), int(self.animations[0][i].get_height() * 2)))
        for i in range(length_off): #off
            self.animations[1].append(pygame.image.load(f'assets/sprites/spaceship/engines/{engine_now}/off/off{i + 1}.png'))
            self.animations[1][i] = pygame.transform.scale(self.animations[1][i], (int(self.animations[1][i].get_width() * 2), int(self.animations[1][i].get_height() * 2)))
        
        self.p_index = 1 #pulse image index
        self.isonpulse = False #check if it's on pulse to change between animations
        self.i_index = 1 #idle image index
    
    #set movement on the spaceship
    def update(self, SURFACE_HEIGHT, SURFACE_WIDTH, SURFACE):
        
        speed_now = self.speed #return speed to default

        #keep being dragged downwards
        if self.rect.bottom < SURFACE_HEIGHT - 35:
            self.rect.y += speed_now // 2

        #key press and movement
        key = pygame.key.get_pressed()

        #engine on animation
        if key[pygame.K_LSHIFT] and (key[pygame.K_w] or key[pygame.K_UP] or key[pygame.K_a] or key[pygame.K_LEFT] or key[pygame.K_s] or key[pygame.K_DOWN] or key[pygame.K_d] or key[pygame.K_RIGHT]):
            speed_now += speed_now // 2
            self.isonpulse = True
            SURFACE.blit(self.animations[0][self.p_index], (self.rect.x + self.e_coordon[0], self.rect.y + self.e_coordon[1]))
            self.p_index += 1
            if self.p_index == 4:
                self.p_index = 1

        if (key[pygame.K_w] or key[pygame.K_UP]) and self.rect.top > 10:
            self.rect.y -= speed_now + speed_now // 2
        if (key[pygame.K_a] or key[pygame.K_LEFT]) and self.rect.left > 10:
            self.rect.x -= speed_now
        if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.rect.bottom < SURFACE_HEIGHT - 35:
            self.rect.y += speed_now
        if (key[pygame.K_d] or key[pygame.K_RIGHT]) and self.rect.right < SURFACE_WIDTH - 10:
            self.rect.x += speed_now

        #engine off animation (not on boost)
        if not self.isonpulse:
            SURFACE.blit(self.animations[1][self.i_index], (self.rect.x + self.e_coordff[0], self.rect.y + self.e_coordff[1]))
            self.i_index += 1
            if self.i_index == 3:
                self.i_index = 1

        self.isonpulse = False
        
        #CLT shooting mechanism
        cooldown = 500 #cooldown variable
        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            clt = projectile.Projectile(self.rect.centerx, self.rect.top, 1, "clt", 0, 0)
            variables.clt_group.add(clt)
            self.last_shot = time_now

        #update mask
        self.mask = pygame.mask.from_surface(self.image)
        
        #draw health bar
        pygame.draw.rect(SURFACE, red, (self.rect.x, (self.rect.top - 20), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(SURFACE, green, (self.rect.x, (self.rect.top - 20), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        else:
            self.kill()
            return False #game over

        #damaged spaceship sprites
        if self.health_remaining <= 3 * self.health_start // 4 and self.health_remaining > self.health_start // 2:
            self.image = variables.spaceship_sprites[variables.spaceship_now.index(True)][1] #3/4 ~ 1/2 of life
        elif self.health_remaining <= self.health_start // 2 and self.health_remaining > self.health_start // 4:
            self.image = variables.spaceship_sprites[variables.spaceship_now.index(True)][2] #1/2 ~ 1/4 of life
        elif self.health_remaining <= self.health_start // 4:
            self.image = variables.spaceship_sprites[variables.spaceship_now.index(True)][3] #1/4 ~ 0/4 of life
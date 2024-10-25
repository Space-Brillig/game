import pygame
import characters.projectile as projectile
import objects.variables as variables

#define colours
red = (255, 0, 0)
green = (0, 255, 0)

#Spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.health_start = variables.lifebar
        self.health_remaining = self.health_start
        self.last_shot = pygame.time.get_ticks()
        
        #set correct lengths depending on the selected engine
        if variables.plumes["engine"].index(True) == 0:
            sprite_now = "BaseEngine"
            self.speed = 5
            length_on = 4
            length_off = 3
            self.e_coordon = (0, 8)
            self.e_coordff = self.e_coordon
        elif variables.plumes["engine"].index(True) == 1:
            sprite_now = "BigPulseEngine"
            self.speed = 6
            length_on = 4
            length_off = 4
            self.e_coordon = (32, 76)
            self.e_coordff = (-1, 10)
        elif variables.plumes["engine"].index(True) == 2:
            sprite_now = "BurstEngine"
            self.speed = 7
            length_on = 6
            length_off = 7
            self.e_coordon = (39, 78)
            self.e_coordff = self.e_coordon
        elif variables.plumes["engine"].index(True) == 3:
            sprite_now = "SuperchargedEngine"
            self.speed = 8
            length_on = 4
            length_off = 4
            self.e_coordon = (29, 80)
            self.e_coordff = self.e_coordon
        
        self.animations = [[], [], [], []] #engine on, engine off, shield and damaged spaceship sprites
        
        #load engine sprites
        for i in range(length_on): #on
            self.animations[0].append(pygame.image.load(f'assets/sprites/spaceship/engines/{sprite_now}/on/on{i + 1}.png'))
            self.animations[0][i] = pygame.transform.scale(self.animations[0][i], (self.animations[0][i].get_width() * 2, self.animations[0][i].get_height() * 2))
        for i in range(length_off): #off
            self.animations[1].append(pygame.image.load(f'assets/sprites/spaceship/engines/{sprite_now}/off/off{i + 1}.png'))
            self.animations[1][i] = pygame.transform.scale(self.animations[1][i], (self.animations[1][i].get_width() * 2, self.animations[1][i].get_height() * 2))
        
        #set correct lenghts depending on selected shield
        if variables.plumes["shield"].index(True) == 0:
            sprite_now = "FrontShield"
            length_on = 6
        elif variables.plumes["shield"].index(True) == 1:
            sprite_now = "Front&SideShield"
            length_on = 6
        elif variables.plumes["shield"].index(True) == 2:
            sprite_now = "RoundShield"
            length_on = 6
        elif variables.plumes["shield"].index(True) == 3:
            sprite_now = "InvisibilityShield"
            length_on = 6

        #load shield sprites
        for i in range (length_on):
            self.animations[-2].append(pygame.image.load(f'assets/sprites/spaceship/shields/{sprite_now}/shield-{i + 1}.png'))
            self.animations[-2][i] = pygame.transform.scale(self.animations[-2][i], (self.animations[-2][i].get_width() * 2, self.animations[-2][i].get_height() * 2))

        #load spaceship damaged sprites
        if variables.plumes["sprite"]:
            for i in range (4):
                self.animations[-1].append(pygame.image.load(f'assets/sprites/spaceship/samples/main/spaceship-{i}.png'))
                self.animations[-1][i] = pygame.transform.scale(self.animations[-1][i], (self.animations[-1][i].get_width() * 2, self.animations[-1][i].get_height() * 2))
        
        self.image = self.animations[-1][0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.isonpulse = False #check if it's on pulse to change between animations
        self.indexes = [0, 0, 0] #indexes of: engine on, engine off and shield
    
    #set movement on the spaceship
    def update(self):
        
        speed_now = self.speed #return speed to default

        #keep being dragged downwards
        if self.rect.bottom < variables.screen.get_height() - 35:
            self.rect.y += speed_now * (3/4)

        #key press and movement
        key = pygame.key.get_pressed()

        #engine on animation
        if key[pygame.K_LSHIFT] and (key[pygame.K_w]  or key[pygame.K_a] or key[pygame.K_s] or key[pygame.K_d]):
            speed_now += speed_now // 2
            self.isonpulse = True
            variables.screen.blit(self.animations[0][self.indexes[0]], (self.rect.x + self.e_coordon[0], self.rect.y + self.e_coordon[1]))
            self.indexes[0] += 1
            if self.indexes[0] == len(self.animations[0]) - 1:
                self.indexes[0] = 0

        #shield animation
        if key[pygame.K_f]:
            variables.screen.blit(self.animations[-2][self.indexes[-1]], (self.rect.x, self.rect.y))
            self.indexes[-1] += 1
            if self.indexes[-1] == len(self.animations[-2]) - 1:
                self.indexes[-1] = 0

        if key[pygame.K_w] and self.rect.top > 10:
            self.rect.y -= speed_now + speed_now * (3/4)
        if key[pygame.K_a] and self.rect.left > 10:
            self.rect.x -= speed_now 
        if key[pygame.K_s] and self.rect.bottom < variables.screen.get_height() - 35:
            self.rect.y += speed_now
        if key[pygame.K_d] and self.rect.right < variables.screen.get_width() - 10:
            self.rect.x += speed_now

        #engine off animation (not on boost)
        if not self.isonpulse:
            variables.screen.blit(self.animations[1][self.indexes[1]], (self.rect.x + self.e_coordff[0], self.rect.y + self.e_coordff[1]))
            self.indexes[1] += 1
            if self.indexes[1] == len(self.animations[1]) - 1:
                self.indexes[1] = 1

        self.isonpulse = False
        
        #CLT shooting mechanism
        cooldown = 500 #cooldown variable
        time_now = pygame.time.get_ticks()
        if (key[pygame.K_SPACE] or pygame.mouse.get_pressed()[0] == 1) and time_now - self.last_shot > cooldown:
            clt = projectile.CLT(self.rect.centerx, self.rect.top)
            variables.clt_group.add(clt)
            self.last_shot = time_now

        #update mask
        self.mask = pygame.mask.from_surface(self.image)
        
        #draw health bar
        pygame.draw.rect(variables.screen, red, (self.rect.x, (self.rect.top - 20), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(variables.screen, green, (self.rect.x, (self.rect.top - 20), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        else:
            return False #game over

        #damaged spaceship sprites
        if self.health_remaining <= 3 * self.health_start // 4 and self.health_remaining > self.health_start // 2:
            self.image = self.animations[-1][1] #3/4 ~ 1/2 of life
        elif self.health_remaining <= self.health_start // 2 and self.health_remaining > self.health_start // 4:
            self.image = self.animations[-1][2] #1/2 ~ 1/4 of life
        elif self.health_remaining <= self.health_start // 4:
            self.image = self.animations[-1][3] #1/4 ~ 0/4 of life
        else:
            self.image = self.animations[-1][0] #full life
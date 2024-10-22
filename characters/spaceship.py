import pygame
import characters.projectile as projectile
import objects.variables as variables

#define colours
red = (255, 0, 0)
green = (0, 255, 0)

#Spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health, clt_speed, haspulse):
        pygame.sprite.Sprite.__init__(self)
        self.image = variables.spaceship_sprites[variables.spaceship_now.index(True)][0]
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
            self.animations[0].append(pygame.image.load(f'assets/sprites/spaceship/idle/pluma-off{i}.png'))
            self.animations[0][i - 1] = pygame.transform.scale(self.animations[0][i - 1], (int(self.animations[0][i - 1].get_width() * 2), int(self.animations[0][i - 1].get_height() * 2)))
        if self.haspulse:
            for i in range(1, 5):
                self.animations[1].append(pygame.image.load(f'assets/sprites/spaceship/movement/pluma-on{i}.png'))
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
            SURFACE.blit(self.animations[1][self.p_index], (self.rect.x, self.rect.y + 8))
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
            SURFACE.blit(self.animations[0][self.i_index], (self.rect.x, self.rect.y + 8))
            self.i_index += 1
            if self.i_index == 3:
                self.i_index = 1

        self.isonpulse = False
        
        #CLT shooting mechanism
        cooldown = 500 #cooldown variable
        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            clt = projectile.Projectile(self.rect.centerx, self.rect.top, 1, "clt", False, True, self.clt_speed, 0, 0)
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
            return False #out of life
        #damaged spaceship sprites
        if self.health_remaining <= 3 * self.health_start // 4 and self.health_remaining > self.health_start // 2:
            self.image = variables.spaceship_sprites[variables.spaceship_now.index(True)][1] #3/4 ~ 1/2 of life
        elif self.health_remaining <= self.health_start // 2 and self.health_remaining > self.health_start // 4:
            self.image = variables.spaceship_sprites[variables.spaceship_now.index(True)][2] #1/2 ~ 1/4 of life
        elif self.health_remaining <= self.health_start // 4:
            self.image = variables.spaceship_sprites[variables.spaceship_now.index(True)][3] #1/4 ~ 0/4 of life
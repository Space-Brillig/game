import pygame
import objects.variables as variables

#Projectile class (Everything that travels across the screen and bangs: Meteor, Regenerative item and CLT)
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, isharmful, damage):
        pygame.sprite.Sprite.__init__(self)
        self.isharmful = isharmful
        #load projectile sprites
        if isharmful:
            self.animations = [[], []]
            for i in range (7):
                self.animations[0].append(pygame.image.load(f'assets/sprites/projectile/meteor/destroyed/detroyed{i + 1}.png'))
                self.animations[0][i] = pygame.transform.scale(self.animations[0][i], (self.animations[0][i].get_width() * scale, self.animations[0][i].get_height() * scale))
            for i in range (3):
                self.animations[1].append(pygame.image.load(f'assets/sprites/projectile/meteor/tail/tail{i + 1}.png'))
                self.animations[1][i] = pygame.transform.scale(self.animations[1][i], (self.animations[1][i].get_width() * scale + 20, self.animations[1][i].get_height() * 2*scale))
            self.image = self.animations[0][1]
            self.height = self.image.get_height() // 2
        else:
            self.image = pygame.image.load(f'assets/sprites/projectile/r_item.png')
        self.damage = damage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        if isharmful:
            variables.screen.blit(self.animations[1][0], (self.rect.x, self.rect.y - 5*self.height))
        self.mask = pygame.mask.from_surface(self.image)
        self.collided = False
        self.last_collision = pygame.time.get_ticks()
        self.index = 0
        self.tail = 0

    def update(self, ispaceship, speed):
        self.rect.y += speed
        if self.rect.top > variables.screen.get_height() or self.rect.bottom > variables.screen.get_height():
            self.kill()
        
        if not self.collided and self.isharmful:
            variables.screen.blit(self.animations[1][self.tail], (self.rect.x, self.rect.y - 4*self.height))
            if self.tail < 2:
                self.tail += 1
        
        #animation by collision
        if self.collided and self.isharmful:
            self.image = self.animations[0][self.index]
            self.index += 1
            if self.index == 7:
                self.kill()
        
        if pygame.sprite.spritecollide(self, variables.clt_group, True, pygame.sprite.collide_mask):
            self.collided = True
        if pygame.sprite.spritecollide(self, variables.spaceship_group, False, pygame.sprite.collide_mask):
            #it's meteor
            if self.isharmful:
                collision_now = pygame.time.get_ticks()
                if collision_now - self.last_collision > 500:
                    self.collided = True
                    ispaceship.health_remaining -= self.damage
                self.last_collision = collision_now
            #it's regenerative item
            else:
                if ispaceship.health_remaining < ispaceship.health_start:
                    ispaceship.health_remaining += 1
                self.kill()

class CLT(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #load clt sprites
        self.animation = []
        for i in range (7):
            self.animation.append(pygame.image.load(f'assets/sprites/projectile/clt/clt-{i + 1}.png'))
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.index = 0
    
    def update(self):
        #spinning animation
        self.image = self.animation[self.index]
        self.index += 1
        if self.index == 7:
            self.index = 0
        self.rect.y -= variables.clt_speed
        #collisions
        if pygame.sprite.spritecollide(self, variables.meteor_group, None, pygame.sprite.collide_mask):
            return True
        if self.rect.bottom < 0 or pygame.sprite.spritecollide(self, variables.r_item_group, True, pygame.sprite.collide_mask):
            self.kill()
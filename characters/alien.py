import pygame
import objects.variables as variables

#Alien class
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/sprites/alien/shrek.jpeg")
        self.width = self.image.get_width()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.caught = False
    
    def update(self, SURFACE_WIDTH, SURFACE_HEIGHT, speed, spaceship):
        self.rect.y += speed
        
        #catch by collision
        if pygame.sprite.spritecollide(self, variables.clt_group, True, pygame.sprite.collide_mask) and not self.caught:
            self.caught = True
            return self.caught

        #drag offscreen to the closest side if it's caught
        if self.caught:
            if self.rect.x >= SURFACE_WIDTH // 2:
                self.rect.x += 4
            else:
                self.rect.x -= 4
            self.rect.y += 4

        #drag by collision with the spaceship
        if pygame.sprite.spritecollide(self, variables.spaceship_group, None, pygame.sprite.collide_mask):
            if spaceship.rect.y >= self.rect.y:
                self.rect.y -= spaceship.speed #upwards if collision from bottom
            else:
                self.rect.y += spaceship.speed #downwards if collision from top 
            
            if spaceship.rect.x >= self.rect.x and self.rect.x > 0:
                self.rect.x -= spaceship.speed #leftward if collision from left
            elif spaceship.rect.x < self.rect.x and self.rect.x < SURFACE_WIDTH - self.width:
                self.rect.x += spaceship.speed #rightward if collision from right

        if self.rect.top > SURFACE_HEIGHT or self.rect.left > SURFACE_WIDTH or self.rect.right < 0:
            self.kill()
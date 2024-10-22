import pygame
import objects.variables as variables

#Projectile class (Everything that travels across the screen and bangs: Meteor, Regenerative item and CLT)
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, image, isharmful, isclt, shooting_speed, damage, points):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'assets/sprites/projectile/{image}.png')
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        self.isharmful = isharmful
        self.isclt = isclt
        self.shooting_speed = shooting_speed
        self.damage = damage
        self.points = points
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, SURFACE_HEIGHT, ispaceship, speed):
        if not self.isclt:
            #what every projectile does, except for the clt
            self.rect.y += speed
            if self.rect.top > SURFACE_HEIGHT or self.rect.bottom > SURFACE_HEIGHT:
                self.kill()
            if pygame.sprite.spritecollide(self, variables.spaceship_group, False, pygame.sprite.collide_mask):
                self.kill()

                #it's meteor
                if self.isharmful:
                    ispaceship.health_remaining -= self.damage
                #it's regenerative item
                elif ispaceship.health_remaining > 0 and ispaceship.health_remaining < ispaceship.health_start:
                    ispaceship.health_remaining += 1
        #it's clt
        else:
            self.rect.y -= self.shooting_speed
            if pygame.sprite.spritecollide(self, variables.meteor_group, True, pygame.sprite.collide_mask):
                self.kill()
                return True
            if self.rect.bottom < 0 or pygame.sprite.spritecollide(self, variables.r_item_group, True, pygame.sprite.collide_mask):
                self.kill()
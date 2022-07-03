"""https://github.com/russs123/Explosion/blob/main/explosion.py"""
import pygame
import math

"""SHIP EXPLOSION"""

class ShipExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 16):
            img = pygame.image.load(f"Assets/Blast{num}.png")
            img = pygame.transform.scale(img, (90, 90))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 2
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


"""MISSILE EXPLOSION"""

class MissileExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, exp_radius):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 11):
            img = pygame.image.load(f"Assets/smallblast{num}.png")
            img = pygame.transform.scale(img, (exp_radius * 2, exp_radius * 2))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 2
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


"""WEAPON TYPES"""

class BulletTypes():
    def __init__(self, bullet_type):
        if bullet_type == 'HV':
            self.velocity = 10
            self.damage = 2
            self.energy = 15
            self.delay = 12

class MissileTypes():
    def __init__(self, missile_type):
        if missile_type == 'HE':
            self.velocity = 9
            self.angular_velocity = 1.5
            self.damage = 1
            self.explosion_damage = 4
            self.energy = 140
            self.delay = 60
            self.explosion_radius = 50


"""FIND NEAREST ENTITY IN LIST"""

def FindNearest(xo, yo, target_list):
    if len(target_list) > 0:
        d = []
        for target in target_list:
            if target.health > 0:
                d.append(math.sqrt((target.centerx - xo) ** 2 + (target.centery - yo) ** 2))
            else:
                d.append(math.inf)

        ind = d.index(min(d))
        return target_list[ind]
    else:
        return None



def ExplosionDamage(max_damage, xo, yo, exp, target_list, explosion_group):
    for target in target_list:
            d = (math.sqrt((target.centerx - xo) ** 2 + (target.centery - yo) ** 2))
            r = math.sqrt(target.height * target.width / 2)
            target.health -= round(max_damage / (1 + (d / (r + exp)) ** 3))
            # print(round(max_damage / (1 + (d / (r + exp)) ** 3)))
            if target.health <= 0:
                explosion = ShipExplosion(target.centerx, target.centery)
                explosion_group.add(explosion)


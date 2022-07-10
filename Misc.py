"""https://github.com/russs123/Explosion/blob/main/explosion.py"""
import pygame
import math
import os
import numpy as np

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


"""GLOBAL STATE CLASS"""

class GlobalState():
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.cx = 0
        self.cy = 0
        self.height = height
        self.width = width


"""WEAPON TYPES"""

class BulletTypes():
    def __init__(self, bullet_type):
        if bullet_type == 'HV':
            self.velocity = 20
            self.damage = 2
            self.energy = 12
            self.range = 3000
            self.delay = 10
            self.height = 2
            self.width = 2
            self.image = pygame.image.load(os.path.join('Assets', 'bullet.png'))  # bullet
        elif bullet_type == 'PA':
            self.velocity = 15
            self.damage = 25
            self.energy = 130
            self.range = 2000
            self.delay = 120
            self.height = 15
            self.width = 15
            self.image = pygame.image.load(os.path.join('Assets', 'Plasma.png'))  # bullet


class MissileTypes():
    def __init__(self, missile_type):
        if missile_type == 'HE':
            self.velocity = 13
            self.angular_velocity = 1.5
            self.damage = 1
            self.explosion_damage = 5
            self.energy = 150
            self.range = 5000
            self.delay = 60
            self.explosion_radius = 50
            self.image = pygame.image.load(os.path.join('Assets', 'smallmissile1.png'))  # missile


class ShipTypes():
    def __init__(self, ship_type, color):
        if ship_type == 'Fighter':
            self.velocity = 8
            self.acc = 0.3
            self.av = 2
            self.energy = 500
            self.health = 50
            self.height = 50
            self.width = 50
        if ship_type == 'Sprinter':
            self.velocity = 11
            self.acc = 0.4
            self.av = 3
            self.energy = 150
            self.health = 20
            self.height = 30
            self.width = 30
        self.image = pygame.image.load(os.path.join('Assets', f'{ship_type}_{color}.png'))  # image with no flame
        self.imagef = pygame.image.load(os.path.join('Assets', f'{ship_type}_{color}_f.png'))  # image with flame

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


"""EXPLOSION DAMAGE CALCULATION"""


def ExplosionDamage(max_damage, xo, yo, exp, target_list, explosion_group, gs):
    for target in target_list:
            d = (math.sqrt((target.centerx - xo) ** 2 + (target.centery - yo) ** 2))
            r = math.sqrt(target.height * target.width / 2)
            target.health -= round(max_damage / (1 + (d / (r + exp)) ** 3))
            # print(round(max_damage / (1 + (d / (r + exp)) ** 3)))
            if target.health <= 0:
                explosion = ShipExplosion(target.centerx - gs.x, target.centery - gs.y)
                explosion_group.add(explosion)


"""TARGETING COMPUTER LOGIC"""


def TargetingComputer(ship):
    vx = ship.target.vx
    vy = ship.target.vy
    xo = ship.target.centerx
    yo = ship.target.centery

    a = vx ** 2 + vy ** 2 - ship.bullet_type.velocity ** 2
    b = 2 * (vx * (xo - ship.centerx) + vy * (yo - ship.centery))
    c = (xo - ship.centerx) ** 2 + (yo - ship.centery) ** 2

    t = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    x = xo + vx * t
    y = yo + vy * t

    dx = x - ship.centerx
    dy = y - ship.centery

    # cos = math.cos(ship.angle * math.pi / 180)
    # sin = math.sin(ship.angle * math.pi / 180)
    #
    # Q = np.array([[cos, -sin], [sin, cos]])
    # V = np.array([[dx], [dy]])
    # V_prime = Q.dot(V)
    # angle2 = math.atan2(V_prime[0][0], V_prime[1][0])

    angle2 = math.atan2(dy, dx)

    return angle2
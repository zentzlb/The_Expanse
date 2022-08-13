"""https://github.com/russs123/Explosion/blob/main/explosion.py"""
import pygame
import math
import os
import numpy as np

"""SHIP EXPLOSION"""

class ShipExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, gs):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 16):
            img = pygame.image.load(f"Assets/Blast{num}.png")
            img = pygame.transform.scale(img, (90, 90))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.x = x
        self.y = y
        self.gs = gs
        self.rect = self.image.get_rect()
        self.rect.center = [x - gs.x, y - gs.y]
        self.counter = 0

    def update(self):
        explosion_speed = 2
        self.counter += 1
        self.rect.center = [self.x - self.gs.x, self.y - self.gs.y]

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


"""MISSILE EXPLOSION"""

class MissileExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, gs, exp_radius):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 11):
            img = pygame.image.load(f"Assets/smallblast{num}.png")
            img = pygame.transform.scale(img, (exp_radius * 2, exp_radius * 2))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.x = x
        self.y = y
        self.gs = gs
        self.rect = self.image.get_rect()
        self.rect.center = [x - gs.x, y - gs.y]
        self.counter = 0

    def update(self):
        explosion_speed = 2
        self.counter += 1

        self.rect.center = [self.x - self.gs.x, self.y - self.gs.y]

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


"""RAIL EXPLOSION"""

class RailExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, gs):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 8):
            img = pygame.image.load(f"Assets/railgun_blast{num}.png")
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.x = x
        self.y = y
        self.gs = gs
        self.rect = self.image.get_rect()
        self.rect.center = [x - gs.x, y - gs.y]
        self.counter = 0

    def update(self):
        explosion_speed = 1
        self.counter += 1
        self.rect.center = [self.x - self.gs.x, self.y - self.gs.y]

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


"""PA EXPLOSION"""

class PAExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, gs):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 14):
            img = pygame.image.load(f"Assets/pa_blast{num}.png")
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.x = x
        self.y = y
        self.gs = gs
        self.rect = self.image.get_rect()
        self.rect.center = [x - gs.x, y - gs.y]
        self.counter = 0

    def update(self):
        explosion_speed = 1
        self.counter += 1
        self.rect.center = [self.x - self.gs.x, self.y - self.gs.y]

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


"""PARTICLE CLASS"""


class Particle:
    def __init__(self, x, y, v, angle, radius, color):
        self.x = x
        self.y = y
        self.fx = x
        self.fy = y
        self.vx = v * math.sin(angle * math.pi / 180)
        self.vy = v * math.cos(angle * math.pi / 180)
        self.color = color
        self.radius = radius

    def update(self):
        self.fx += self.vx
        self.fy += self.vy
        self.x = round(self.fx)
        self.y = round(self.fy)
        self.radius -= 1


class GlobalState:
    def __init__(self, x, y, height, width, docked=None, menu=None):
        self.x = x
        self.y = y
        self.cx = x + width / 2
        self.cy = y + height / 2
        self.height = height
        self.width = width
        self.show_bars = False
        self.particle_list = []
        self.docked = docked
        self.menu = menu



"""WEAPON TYPES"""

class BulletTypes:
    def __init__(self, bullet_type):
        if bullet_type == 'HV':
            self.velocity = 11
            self.damage = 3
            self.energy = 25
            self.range = 3000
            self.delay = 25
            self.height = 10
            self.width = 10
            self.pen = False
            self.exptype = None
            self.image = pygame.image.load(os.path.join('Assets', 'bullet.png'))  # bullet
            self.sound = None
        elif bullet_type == 'PA':
            self.velocity = 8
            self.damage = 35
            self.energy = 90
            self.range = 1500
            self.delay = 120
            self.height = 15
            self.width = 15
            self.pen = False
            self.exptype = PAExplosion
            self.image = pygame.image.load(os.path.join('Assets', 'Plasma.png'))  # bullet
            self.sound = None
        elif bullet_type == 'railgun':
            self.velocity = 24
            self.damage = 10
            self.energy = 200
            self.range = 8000
            self.delay = 240
            self.height = 30
            self.width = 30
            self.pen = True
            self.exptype = RailExplosion
            self.image = pygame.image.load(os.path.join('Assets', 'railgun.png'))  # bullet
            self.sound = pygame.mixer.Sound(os.path.join('Assets', 'railgun_launch.mp3'))


class MissileTypes:
    def __init__(self, missile_type):
        if missile_type == 'HE':
            self.height = 12
            self.width = 12
            self.velocity = 8
            self.angular_velocity = 0.75
            self.damage = 1
            self.explosion_damage = 7
            self.energy = 150
            self.range = 5000
            self.delay = 120
            self.explosion_radius = 50
            self.emp = False
            self.par_str = 1
            self.par_rnd = 0
            self.image = pygame.image.load(os.path.join('Assets', 'smallmissile1.png'))  # missile
            self.sound = pygame.mixer.Sound('Assets//missile_launch.mp3')
        if missile_type == 'torpedo':
            self.height = 15
            self.width = 15
            self.velocity = 7.5
            self.angular_velocity = 0.5
            self.damage = 10
            self.explosion_damage = 35
            self.energy = 150
            self.range = 2000
            self.delay = 180
            self.explosion_radius = 80
            self.emp = True
            self.par_str = 4
            self.par_rnd = 70
            self.image = pygame.image.load(os.path.join('Assets', 'torpedo.png'))  # missile
            self.sound = pygame.mixer.Sound('Assets//missile_launch.mp3')


class ShipTypes():
    def __init__(self, ship_type, color):
        if ship_type == 'Fighter':
            self.velocity = 4.5
            self.acc = 0.3
            self.av = 2
            self.energy = 500
            self.health = 100
            self.height = 50
            self.width = 50
            self.turrets = []
            self.turret_loc = []
        if ship_type == 'Sprinter':
            self.velocity = 6
            self.acc = 0.45
            self.av = 1.5
            self.energy = 200
            self.health = 50
            self.height = 30
            self.width = 30
            self.turrets = []
            self.turret_loc = []
        if ship_type == 'Frigate':
            self.velocity = 3
            self.acc = 0.1
            self.av = 0.5
            self.energy = 5000
            self.health = 400
            self.height = 80
            self.width = 80
            self.turrets = ['PDC']
            self.turret_loc = []
        self.image = pygame.image.load(os.path.join('Assets', f'{ship_type}_{color}.png'))  # image with no flame
        self.imagef = pygame.image.load(os.path.join('Assets', f'{ship_type}_{color}_f.png'))  # image with flame


class StationTypes():
    def __init__(self, station_type):
        if station_type == 'Partrid':
            self.energy = 500
            self.health = 100
            self.height = 250
            self.width = 250
            self.turrets = ['PDC']
            self.turret_loc = []
            self.image = pygame.image.load(os.path.join('Assets', f'{station_type}.png'))  # image with no flame


class TurretTypes():
    def __init__(self, turret_type):
        if turret_type == 'PDC':
            self.av = 1.5
            self.energy = 150
            self.health = 100
            self.height = 20
            self.width = 20
            self.bullet_type = 'HV'
            self.missile_type = None
        self.image = pygame.image.load(os.path.join('Assets', f'{turret_type}.png'))  # image with no flame


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
            r = math.sqrt(target.height * target.width)
            if d < exp + r:
                damage = round(2 * max_damage / (1 + math.exp((d + 1) / (r + exp + 1))))
                target.health -= damage
                if target.health <= 0:
                    explosion = ShipExplosion(target.centerx, target.centery, gs)
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

def MoveScreen(gs):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_UP]:  # UP
        gs.y -= 15
        gs.cy -= 15
    elif keys_pressed[pygame.K_DOWN]:  # DOWN
        gs.y += 15
        gs.cy += 15
    if keys_pressed[pygame.K_RIGHT]:  # RIGHT
        gs.x += 15
        gs.cx += 15
    elif keys_pressed[pygame.K_LEFT]:  # LEFT
        gs.x -= 15
        gs.cx -= 15



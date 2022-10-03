"""https://github.com/russs123/Explosion/blob/main/explosion.py"""
import pygame
import math
import os
import numpy as np
import random as rnd

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
    def __init__(self, x, y, height, width, fonts, stations, ships, bullets, missiles, asteroids, docked=None, menu=None):
        self.x = x
        self.y = y
        self.stations = stations
        self.ships = ships
        self.bullets = bullets
        self.missiles = missiles
        self.asteroids = asteroids
        self.cx = x + width / 2
        self.cy = y + height / 2
        self.height = height
        self.width = width
        self.show_bars = False
        self.particle_list = []
        self.fonts = fonts
        self.docked = docked
        self.menu = menu
        self.targets = []
        self.update()

    def update(self):
        self.targets = []
        for i in range(len(self.ships)):
            self.targets.append([])
            for j in range(len(self.ships)):
                if j != i:
                    self.targets[i].extend(self.ships[j])



"""WEAPON TYPES"""

class BulletTypes:
    def __init__(self, bullet_type):
        if bullet_type == 'HV':
            self.velocity = 11.5
            self.damage = 3
            self.energy = 25
            self.range = 3000
            self.delay = 25
            self.height = 10
            self.width = 10
            self.cost = {"Iron": 10, "Nickel": 10, "Platinum": 1, "Gold": 0}
            self.name = "HV"
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
            self.cost = {"Iron": 10, "Nickel": 5, "Platinum": 5, "Gold": 10}
            self.name = "PA"
            self.pen = False
            self.exptype = PAExplosion
            self.image = pygame.image.load(os.path.join('Assets', 'Plasma.png'))  # bullet
            self.sound = None
        elif bullet_type == 'railgun':
            self.velocity = 25
            self.damage = 10
            self.energy = 200
            self.range = 8000
            self.delay = 240
            self.height = 30
            self.width = 30
            self.cost = {"Iron": 10, "Nickel": 25, "Platinum": 10, "Gold": 1}
            self.name = "railgun"
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
            self.drunk = False
            self.par_str = 1
            self.par_rnd = 0
            self.cost = {"Iron": 100, "Nickel": 125, "Platinum": 10, "Gold": 10}
            self.name = "HE"
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
            self.drunk = False
            self.par_str = 4
            self.par_rnd = 70
            self.cost = {"Iron": 100, "Nickel": 50, "Platinum": 15, "Gold": 50}
            self.name = "torpedo"
            self.image = pygame.image.load(os.path.join('Assets', 'torpedo.png'))  # missile
            self.sound = pygame.mixer.Sound('Assets//missile_launch.mp3')
        if missile_type == 'swarm missile':
            self.height = 10
            self.width = 10
            self.velocity = 7.5
            self.angular_velocity = 2.5
            self.damage = 1
            self.explosion_damage = 6
            self.energy = 120
            self.range = 4000
            self.delay = 40
            self.explosion_radius = 20
            self.emp = False
            self.drunk = True
            self.par_str = 2
            self.par_rnd = 30
            self.cost = {"Iron": 100, "Nickel": 50, "Platinum": 15, "Gold": 50}
            self.name = "swarm missile"
            self.image = pygame.image.load(os.path.join('Assets', 'swarm_missile.png'))  # missile
            self.sound = pygame.mixer.Sound('Assets//missile_launch.mp3')


class ShipTypes():
    def __init__(self, ship_type, color):
        crg = CargoClass()
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
            self.cargo_cap = 30
            self.cost = {"Iron": 500, "Nickel": 225, "Platinum": 60, "Gold": 120}
            self.name = "Fighter"
        if ship_type == 'Sprinter':
            self.velocity = 6
            self.acc = 0.45
            self.av = 1.5
            self.energy = 250
            self.health = 50
            self.height = 30
            self.width = 30
            self.turrets = []
            self.turret_loc = []
            self.cargo_cap = 10
            self.cost = {"Iron": 300, "Nickel": 300, "Platinum": 30, "Gold": 90}
            self.name = "Sprinter"
        if ship_type == 'Frigate':
            self.velocity = 3
            self.acc = 0.1
            self.av = 0.5
            self.energy = 2000
            self.health = 300
            self.height = 80
            self.width = 80
            self.turrets = ['PDC']
            self.turret_loc = []
            self.cargo_cap = 100
            self.cost = {"Iron": 800, "Nickel": 150, "Platinum": 600, "Gold": 30}
            self.name = "Frigate"
        self.image = pygame.image.load(os.path.join('Assets', f'{ship_type}_{color}.png'))  # image with no flame
        self.imagef = pygame.image.load(os.path.join('Assets', f'{ship_type}_{color}_f.png'))  # image with flame


class CargoClass(dict):
    def __init__(self):
        super().__init__()
        self.cargo = assign_ore('Cargo')

    def __missing__(self, key):
        return 0


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
            self.energy = 200
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
            r = math.sqrt((target.centerx - xo) ** 2 + (target.centery - yo) ** 2)  # distance to target
            a = target.is_visible  # is uncloaked
            b = r < 1500  # is within visual range
            if (a or b) and target.health > 0:  # only add ships to the target list if they're visible
                d.append(r)
            # else:
                # d.append(math.inf)
        if len(d) > 0:
            ind = d.index(min(d))
            return target_list[ind]
        else:
            return None
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


def assign_ore(name):
    if name == 'Std':  # standard asteroid with iron, nickel, platinum, and gold
        return {"Iron": rnd.randint(200, 300), "Nickel": rnd.randint(100, 200), "Platinum": rnd.randint(25, 125), "Gold": rnd.randint(0, 75)}
    if name == 'Cargo':  # shortcut to assign empty cargo to new ships
        return {"Iron": 0, "Nickel": 0, "Platinum": 0, "Gold": 0}


def check_purchase(station, target):
    for i in range(len(target.cost)):
        ore_names = list(target.cost)
        if station.cargo[ore_names[i]] < target.cost[ore_names[i]]:
            return False
    return True


def purchase(station, target):
    for i in range(len(target.cost)):
        ore_names = list(target.cost)
        station.cargo[ore_names[i]] -= target.cost[ore_names[i]]

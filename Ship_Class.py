import pygame
import math
import numpy as np
import random as rnd
import os

from Weapon_Class import Bullet, Missile
from Misc import BulletTypes, MissileTypes, ShipTypes, TurretTypes, StationTypes, Particle
from Control_Functions import FindNearest, NPControl, TurretControl
from Menus import StationMenu


class Ship(pygame.Rect):
    def __init__(self, control_module, x, y, angle, color, ship_type, bullet_type, missile_type, is_player=False):
        ShipType = ShipTypes(ship_type, color)
        Turrets = []
        for turret in ShipType.turrets:
            Turrets.append(Turret(x, y, angle, turret, is_player=False))
        super().__init__(x, y, ShipType.height, ShipType.width)
        self.ship_type = ShipType
        self.angle = angle
        # self.Velocity = ShipType.velocity
        self.velocity = ShipType.velocity
        # self.Av = ShipType.av
        self.av = ShipType.av
        # self.Acc = ShipType.acc
        self.acc = ShipType.acc
        self.fx = x
        self.fy = y
        self.cx = x
        self.cy = y
        # self.Health = ShipType.health
        self.health = ShipType.health
        # self.Energy = ShipType.energy
        self.energy = ShipType.energy
        self.vx = 0
        self.vy = 0
        self.counter = 0
        self.bulletC = 0
        self.missileC = 0
        self.target = None
        self.control_module = control_module
        self.bullet_type = BulletTypes(bullet_type)
        self.missile_type = MissileTypes(missile_type)
        self.turrets = Turrets
        # self.image = ShipType.image
        # self.imagef = ShipType.imagef
        self.forward = False
        self.boost = False
        self.is_player = is_player

    def scoot(self, bullet_list, missile_list, target_list, global_state, station_list, ally_ships):
        keys_pressed = pygame.key.get_pressed()

        commands = self.control_module(self, self.bullet_type.velocity, bullet_list, missile_list, target_list)
        self.forward = False

        """MOVEMENT- THRUSTER ACCELERATION"""

        if commands[0] == 1:  # ROTATE CCW
            self.angle += self.av
        elif commands[0] == -1:  # ROTATE CW
            self.angle -= self.av
        if commands[1] == 1:  # UP
            self.vx += self.acc * math.sin(self.angle * math.pi / 180)
            self.vy += self.acc * math.cos(self.angle * math.pi / 180)
            self.forward = True
        elif commands[1] == -1:  # DOWN
            self.vx -= self.acc * math.sin(self.angle * math.pi / 180) / 2
            self.vy -= self.acc * math.cos(self.angle * math.pi / 180) / 2
        if commands[2] == 1:  # LEFT
            self.vy -= self.acc * math.sin(self.angle * math.pi / 180) / 2
            self.vx += self.acc * math.cos(self.angle * math.pi / 180) / 2
        elif commands[2] == -1:  # RIGHT
            self.vy += self.acc * math.sin(self.angle * math.pi / 180) / 2
            self.vx -= self.acc * math.cos(self.angle * math.pi / 180) / 2

        """DON'T GOT OVER SPEED LIMIT"""
        if math.sqrt(self.vx ** 2 + self.vy ** 2) > self.velocity:
            self.vx = self.vx * self.velocity / math.sqrt(self.vx ** 2 + self.vy ** 2)
            self.vy = self.vy * self.velocity / math.sqrt(self.vx ** 2 + self.vy ** 2)

        self.fx += self.vx
        self.fy += self.vy

        self.x = round(self.fx)
        self.y = round(self.fy)

        self.cx = round(self.x + (
                    self.width - self.height * abs(math.sin(self.angle * math.pi / 180)) - self.width * abs(math.cos(self.angle * math.pi / 180))) / 2)
        self.cy = round(self.y + (
                    self.height - self.width * abs(math.sin(self.angle * math.pi / 180)) - self.height * abs(math.cos(self.angle * math.pi / 180))) / 2)

        """FIRE BULLETS and MISSILES"""
        if commands[3] == 1 and self.energy >= self.bullet_type.energy and self.bulletC == 0:  # DOWN
            self.energy -= self.bullet_type.energy
            self.bulletC = self.bullet_type.delay
            bullet = Bullet(self.x + self.width // 2 - self.bullet_type.width // 2, self.y + self.height // 2 - self.bullet_type.height // 2, self.angle, self.bullet_type)
            bullet_list.append(bullet)
        if commands[4] == 1 and self.energy >= self.missile_type.energy and self.missileC == 0 and self.target is not None:
            self.energy -= self.missile_type.energy
            self.missileC = self.missile_type.delay
            missile = Missile(self.x + self.width // 2, self.y + self.height // 2 - 2, self.angle, self.missile_type.height, self.missile_type.width, self.missile_type, self.target)
            missile_list.append(missile)
            self.missile_type.sound.play()
        if commands[5] == 1 and self.energy > 1:  # boost
            self.boost = True
            self.velocity = self.ship_type.velocity + 1
            self.acc = self.ship_type.acc * 2
            self.av = self.ship_type.av * 1.1
            self.energy -= 1
            for i in range(5):
                global_state.particle_list.append(Particle(self.centerx, self.centery, -rnd.randint(15, 30), self.angle + rnd.randint(-15, 15), 5, (255, rnd.randint(0, 255), 0)))
        else:
            self.boost = False
            self.velocity = self.ship_type.velocity
            self.acc = self.ship_type.acc
            self.av = self.ship_type.av

        if self.energy < self.ship_type.energy:
            self.energy += 0.5
        if self.health < self.ship_type.health:
            self.health += 0.01
        if self.bulletC > 0:
            self.bulletC -= 1
        if self.missileC > 0:
            self.missileC -= 1

        for turret in self.turrets:
            turret.x = self.centerx - turret.width / 2
            turret.y = self.centery - turret.height / 2
            turret.scoot(bullet_list, missile_list, target_list, global_state)

        if self.is_player:
            global_state.x = self.centerx - global_state.width / 2
            global_state.y = self.centery - global_state.height / 2
            global_state.cx = self.centerx
            global_state.cy = self.centery
            if keys_pressed[pygame.K_u] and global_state.docked is None:
                MyList = self.collidelistall(station_list)
                if len(MyList) == 1:
                    global_state.docked = station_list[MyList[0]]
                    global_state.menu = StationMenu()
                    self.center = global_state.docked.center
                    global_state.x = self.centerx - global_state.width / 2
                    global_state.y = self.centery - global_state.height / 2
                    global_state.cx = self.centerx
                    global_state.cy = self.centery
                    self.vx = 0
                    self.vy = 0
                    station_list[MyList[0]].docked_ships.append(self)
                    ally_ships.remove(self)
    def refresh(self):
        self.height = self.ship_type.height
        self.width = self.ship_type.width
        self.energy = self.ship_type.energy
        self.health = self.ship_type.health
        Turrets = []
        for turret in self.ship_type.turrets:
            Turrets.append(Turret(self.x, self.y, self.angle, turret, is_player=False))
        self.turrets = Turrets




class Turret(pygame.Rect):
    def __init__(self, x, y, angle, turret_type, is_player=False):
        TurretType = TurretTypes(turret_type)
        super().__init__(x, y, TurretType.height, TurretType.width)
        self.angle = angle
        self.av = TurretType.av
        self.fx = x
        self.fy = y
        self.cx = x
        self.cy = y
        self.Health = TurretType.health
        self.health = self.Health
        self.Energy = TurretType.energy
        self.energy = self.Energy
        self.vx = 0
        self.vy = 0
        self.counter = 0
        self.bulletC = 0
        self.missileC = 0
        self.target = None
        self.control_module = TurretControl
        self.bullet_type = BulletTypes(TurretType.bullet_type)
        if TurretType.missile_type is not None:
            self.missile_type = MissileTypes(TurretType.missile_type)
        else:
            self.missile_type = None
        self.image = TurretType.image
        self.is_player = is_player

    def scoot(self, bullet_list, missile_list, target_list, global_state):

        commands = self.control_module(self, self.bullet_type.velocity, bullet_list, missile_list, target_list)

        """MOVEMENT- ROTATION"""

        if commands[0] == 1:  # ROTATE CCW
            self.angle += self.av
        elif commands[0] == -1:  # ROTATE CW
            self.angle -= self.av

        """FIRE BULLETS and MISSILES"""
        if commands[1] == 1 and self.energy >= self.bullet_type.energy and self.bulletC == 0:
            self.energy -= self.bullet_type.energy
            self.bulletC = self.bullet_type.delay
            bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2 - 2, self.angle, self.bullet_type)
            bullet_list.append(bullet)
        if self.missile_type is not None and commands[2] == 1 and self.energy >= self.missile_type.energy and self.missileC == 0 and self.target is not None:
            self.energy -= self.missile_type.energy
            self.missileC = self.missile_type.delay
            missile = Missile(self.x + self.width // 2, self.y + self.height // 2 - 2, self.angle, 2, 10, self.missile_type, self.target)
            missile_list.append(missile)
            # self.missile_type.sound.play()
        if self.energy < self.Energy:
            self.energy += 0.5
        if self.health < self.Health:
            self.health += 0.005
        if self.bulletC > 0:
            self.bulletC -= 1
        if self.missileC > 0:
            self.missileC -= 1

        self.cx = round(self.x + (self.width - self.height * abs(math.sin(self.angle * math.pi / 180)) - self.width * abs(math.cos(self.angle * math.pi / 180))) / 2)
        self.cy = round(self.y + (self.height - self.width * abs(math.sin(self.angle * math.pi / 180)) - self.height * abs(math.cos(self.angle * math.pi / 180))) / 2)

        if self.is_player:
            global_state.x = self.centerx - global_state.width / 2
            global_state.y = self.centery - global_state.height / 2
            global_state.cx = self.centerx
            global_state.cy = self.centery



"""STATION CLASS"""

class Station(pygame.Rect):
    def __init__(self, x, y, station_type):
        StationType = StationTypes(station_type)
        Turrets = []
        for turret in StationType.turrets:
            Turrets.append(Turret(x, y, 0, turret, is_player=False))
        super().__init__(x, y, StationType.height, StationType.width)
        self.fx = x
        self.fy = y
        self.cx = x
        self.cy = y
        self.Health = StationType.health
        self.health = self.Health
        self.Energy = StationType.energy
        self.energy = self.Energy
        self.counter = 0
        self.turrets = Turrets
        self.image = StationType.image
        self.docked_ships = []

    def scoot(self, bullet_list, missile_list, target_list, ally_list, global_state):
        # keys_pressed = pygame.key.get_pressed()
        # if keys_pressed[pygame.K_i] and len(self.docked_ships) > 0:

        # elif keys_pressed[pygame.K_i] and global_state.docked is not None:
        # ally_ships.append(global_state.docked.docked_ships[0])
        # global_state.docked.docked_ships.remove(global_state.docked.docked_ships[0])
        for turret in self.turrets:
            turret.x = self.centerx - turret.width / 2
            turret.y = self.centery - turret.height / 2
            turret.scoot(bullet_list, missile_list, target_list, global_state)


"""ASTEROID CLASS"""

class Asteroid(pygame.Rect):
    def __init__(self, x, y, angle):
        super().__init__(x, y, 200, 200)
        self.image = pygame.image.load(os.path.join('Assets', f'asteroid.png'))
        self.angle = angle
        self.ore = ['gold']

    # def scoot(self, bullet_list, missile_list, target_list, ally_list, global_state):
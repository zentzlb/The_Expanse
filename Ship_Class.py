import pygame
import math
import numpy as np
import random as rnd

from Weapon_Class import Bullet, Missile
from Misc import BulletTypes, MissileTypes
from Control_Functions import FindNearest, NPControl


class Ship(pygame.Rect):
    def __init__(self, control_module, x, y, velocity, angular_velocity, acceleration, angle, height, width, bullet_type, missile_type):
        super().__init__(x, y, width, height)
        self.angle = angle
        self.velocity = velocity
        self.av = angular_velocity
        self.acc = acceleration
        self.fx = x
        self.fy = y
        self.cx = x
        self.cy = y
        self.Health = round(math.sqrt(self.height * self.width))
        self.health = self.Health
        self.Energy = round(10 * math.sqrt(self.height * self.width))
        self.energy = self.Energy
        self.vx = 0
        self.vy = 0
        self.counter = 0
        self.bulletC = 0
        self.missileC = 0
        self.target = None
        self.control_module = control_module
        self.bullet_type = BulletTypes(bullet_type)
        self.missile_type = MissileTypes(missile_type)

    def scoot(self, width, height, bullet_list, missile_list, target_list):

        commands = self.control_module(self, width, height, self.bullet_type.velocity, bullet_list, missile_list, target_list)

        """MOVEMENT"""

        if commands[0] == 1:  # LEFT
            self.angle += self.av
        elif commands[0] == -1:  # RIGHT
            self.angle -= self.av
        if commands[1] == 1:  # UP
            self.vx += self.acc * math.sin(self.angle * math.pi / 180)
            self.vy += self.acc * math.cos(self.angle * math.pi / 180)
        elif commands[1] == -1:  # DOWN
            self.vx -= self.acc * math.sin(self.angle * math.pi / 180) / 2
            self.vy -= self.acc * math.cos(self.angle * math.pi / 180) / 2
        if commands[2] == 1:  # LEFT
            self.vy -= self.acc * math.sin(self.angle * math.pi / 180) / 2
            self.vx += self.acc * math.cos(self.angle * math.pi / 180) / 2
        elif commands[2] == -1:  # RIGHT
            self.vy += self.acc * math.sin(self.angle * math.pi / 180) / 2
            self.vx -= self.acc * math.cos(self.angle * math.pi / 180) / 2

        """DONT GOT OVER SPEED LIMIT"""
        if math.sqrt(self.vx ** 2 + self.vy ** 2) > self.velocity:
            self.vx = self.vx * self.velocity / math.sqrt(self.vx ** 2 + self.vy ** 2)
            self.vy = self.vy * self.velocity / math.sqrt(self.vx ** 2 + self.vy ** 2)

        self.fx += self.vx
        self.fy += self.vy

        self.x = round(self.fx)
        self.y = round(self.fy)

        self.cx = round(self.fx + (
                    self.width - self.height * abs(math.sin(self.angle * math.pi / 180)) - self.width * abs(math.cos(self.angle * math.pi / 180))) / 2)
        self.cy = round(self.fy + (
                    self.height - self.width * abs(math.sin(self.angle * math.pi / 180)) - self.height * abs(math.cos(self.angle * math.pi / 180))) / 2)

        # bounce off edge of screen
        if self.fx < 0 or self.fx > width - self.width:
            self.fx += - self.vx
            self.vx = - self.vx  # / 4
            self.vy = self.vy  # / 4

        if self.fy < 0 or self.fy > height - self.height:
            self.fy += - self.vy
            self.vy = - self.vy  # / 4
            self.vx = self.vx  # / 4

        """BULLETS and MISSILES"""
        if commands[3] == 1 and self.energy >= self.bullet_type.energy and self.bulletC == 0:  # DOWN
            self.energy -= self.bullet_type.energy
            self.bulletC = self.bullet_type.delay
            bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2 - 2, self.angle, 2, 2, self.bullet_type)
            bullet_list.append(bullet)
        elif commands[4] == 1 and self.energy >= self.missile_type.energy and self.missileC == 0:
            self.energy -= self.missile_type.energy
            self.missileC = self.missile_type.delay
            missile = Missile(self.x + self.width // 2, self.y + self.height // 2 - 2, self.angle, 2, 10, self.missile_type)
            missile_list.append(missile)
        if self.energy < self.Energy:
            self.energy += 1
        if self.bulletC > 0:
            self.bulletC -= 1
        if self.missileC > 0:
            self.missileC -= 1


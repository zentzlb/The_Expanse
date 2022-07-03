import pygame
import math
import numpy as np
from Misc import ShipExplosion, MissileExplosion
from Misc import FindNearest, ExplosionDamage


class Bullet(pygame.Rect):
    def __init__(self, x, y, angle, height, width, bullet_type):
        super().__init__(x, y, width, height)
        self.angle = angle
        self.velocity = bullet_type.velocity
        self.damage = bullet_type.damage
        self.fx = x
        self.fy = y

    def scoot(self, bullet_list, target_list, height, width, explosion_group):
        self.fx += self.velocity * math.sin(self.angle * math.pi / 180)
        self.fy += self.velocity * math.cos(self.angle * math.pi / 180)

        self.x = round(self.fx)
        self.y = round(self.fy)

        if self.collidelist(target_list) != -1:  # bullet hits red
            dmgList = self.collidelistall(target_list)
            for i in dmgList:
                target_list[i].health -= self.damage
                if target_list[i].health <= 0:
                    explosion = ShipExplosion(target_list[i].centerx, target_list[i].centery)
                    explosion_group.add(explosion)
            bullet_list.remove(self)

            # pygame.event.post(pygame.event.Event(RED_HIT))
        elif self.x > width or self.x < 0 or self.y > height or self.y < 0:  # bullets leaves arena
            bullet_list.remove(self)


class Missile(pygame.Rect):
    def __init__(self, x, y, angle, height, width, missile_type):
        super().__init__(x, y, width, height)
        self.angle = angle
        self.velocity = missile_type.velocity
        self.damage = missile_type.damage
        self.explosion_damage = missile_type.explosion_damage
        self.av = missile_type.angular_velocity
        self.fx = x
        self.fy = y
        self.er = missile_type.explosion_radius
        self.timer = 0
        self.target = None

    def scoot(self, missile_list, target_list, explosion_group):

        if self.target is None or self.target.health >= 0 or self.timer % 60 == 0:
            self.target = FindNearest(self.centerx, self.centery, target_list)

        if self.target is None:
            explosion = MissileExplosion(self.centerx, self.centery, self.er)
            explosion_group.add(explosion)

            missile_list.remove(self)

        else:
            da = np.cross((math.sin(self.angle * math.pi / 180), math.cos(self.angle * math.pi / 180), 0),
                          (self.target.centerx - self.centerx, self.target.centery - self.centery, 0))[2]
            if da > 0:
                self.angle -= self.av
            else:
                self.angle += self.av

        self.fx += self.velocity * math.sin(self.angle * math.pi / 180)
        self.fy += self.velocity * math.cos(self.angle * math.pi / 180)

        self.x = round(self.fx)
        self.y = round(self.fy)

        if self.collidelist(target_list) != -1:  # bullet hits red
            dmgList = self.collidelistall(target_list)
            for i in dmgList:
                target_list[i].health -= 1
                explosion = MissileExplosion(self.centerx, self.centery, self.er)
                explosion_group.add(explosion)
                if target_list[i].health <= 0:
                    explosion = ShipExplosion(target_list[i].centerx, target_list[i].centery)
                    explosion_group.add(explosion)
            ExplosionDamage(self.explosion_damage, self.centerx, self.centery, self.er, target_list, explosion_group)
            missile_list.remove(self)

        elif self.timer > 500:  # missile runs out of thrust
            explosion = MissileExplosion(self.centerx, self.centery, self.er)
            explosion_group.add(explosion)
            ExplosionDamage(4, self.centerx, self.centery, self.er, target_list, explosion_group)
            missile_list.remove(self)

        self.timer += 1
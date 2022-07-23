import pygame
import math
import numpy as np
import random as rnd
from Misc import ShipExplosion, MissileExplosion
from Misc import FindNearest, ExplosionDamage

"""BULLET CLASS"""

class Bullet(pygame.Rect):
    def __init__(self, x, y, angle, bullet_type):
        if bullet_type.sound is not None:
            bullet_type.sound.play()
        super().__init__(x, y, bullet_type.width, bullet_type.height)
        self.angle = angle
        self.velocity = bullet_type.velocity
        self.range = bullet_type.range
        self.damage = bullet_type.damage
        self.pen = bullet_type.pen
        self.timer = 0
        self.fx = x
        self.fy = y
        self.image = pygame.transform.rotate(bullet_type.image, angle)

    def scoot(self, bullet_list, target_list, explosion_group, gs):
        self.fx += self.velocity * math.sin(self.angle * math.pi / 180)
        self.fy += self.velocity * math.cos(self.angle * math.pi / 180)

        self.x = round(self.fx)
        self.y = round(self.fy)

        if self.collidelist(target_list) != -1:  # bullet hits red
            dmgList = self.collidelistall(target_list)
            for i in dmgList:
                target_list[i].health -= self.damage
                if target_list[i].health <= 0:
                    explosion = ShipExplosion(target_list[i].centerx, target_list[i].centery, gs)
                    explosion_group.add(explosion)
            if not self.pen:
                bullet_list.remove(self)

            # pygame.event.post(pygame.event.Event(RED_HIT))
        elif self.timer > self.range / self.velocity:  # missile runs out of thrust
            bullet_list.remove(self)

        self.timer += 1
        # elif self.x > width or self.x < 0 or self.y > height or self.y < 0:  # bullets leaves arena
        #     bullet_list.remove(self)


"""MISSILE CLASS"""

class Missile(pygame.Rect):
    def __init__(self, x, y, angle, height, width, missile_type):
        if missile_type.sound is not None:
            missile_type.sound.play()
        super().__init__(x, y, width, height)
        self.angle = angle
        self.velocity = missile_type.velocity
        self.range = missile_type.range
        self.damage = missile_type.damage
        self.explosion_damage = missile_type.explosion_damage
        self.av = missile_type.angular_velocity
        self.fx = x
        self.fy = y
        self.er = missile_type.explosion_radius
        self.timer = 0
        self.arm = 30
        self.target = None
        self.emp = missile_type.emp
        self.image = missile_type.image

    def scoot(self, missile_list, target_list, explosion_group, gs):

        if self.target is None or self.target.health >= 0 or self.timer % 60 == 0:
            self.target = FindNearest(self.centerx, self.centery, target_list)

        if self.target is None:
            explosion = MissileExplosion(self.centerx, self.centery, gs, self.er)
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

        if self.collidelist(target_list) != -1 and self.timer > self.arm:  # missile hits target
            dmgList = self.collidelistall(target_list)
            for i in dmgList:
                target_list[i].health -= self.damage
                if self.emp:
                    target_list[i].energy = 0
                    target_list[i].bulletC += 180
                    target_list[i].missileC += 180
                    for turret in target_list[i].turrets:
                        turret.energy = 0
                        turret.angle += 360 * rnd.uniform(-1, 1) / math.pi
                        turret.bulletC += 180
                        turret.missileC += 180

                if target_list[i].health <= 0:
                    explosion = ShipExplosion(target_list[i].centerx, target_list[i].centery, gs)
                    explosion_group.add(explosion)
            explosion = MissileExplosion(self.centerx, self.centery, gs, self.er)
            explosion_group.add(explosion)
            ExplosionDamage(self.explosion_damage, self.centerx, self.centery, self.er, target_list, explosion_group, gs)
            missile_list.remove(self)

        elif self.timer > self.range / self.velocity:  # missile runs out of thrust
            explosion = MissileExplosion(self.centerx, self.centery, gs, self.er)
            explosion_group.add(explosion)
            ExplosionDamage(self.explosion_damage, self.centerx, self.centery, self.er, target_list, explosion_group, gs)
            missile_list.remove(self)

        self.timer += 1
import pygame
import math
import numpy as np
import random as rnd
import time
from Misc import ShipExplosion, MissileExplosion
from Misc import FindNearest, ExplosionDamage, Particle

"""BULLET CLASS"""

class Bullet(pygame.Rect):
    def __init__(self, x, y, angle, bullet_type, faction):
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
        self.exptype = bullet_type.exptype
        self.image = pygame.transform.rotate(bullet_type.image, angle)
        self.faction = faction


    def scoot(self, explosion_group, gs):
        self.fx += self.velocity * math.sin(self.angle * math.pi / 180)
        self.fy += self.velocity * math.cos(self.angle * math.pi / 180)

        self.x = round(self.fx)
        self.y = round(self.fy)



        if self.collidelist(gs.targets[self.faction]) != -1:  # bullet hits red
            if self.exptype is not None:
                explosion = self.exptype(self.centerx, self.centery, gs)
                explosion_group.add(explosion)
            dmgList = self.collidelistall(gs.targets[self.faction])
            for i in dmgList:
                gs.targets[self.faction][i].health -= self.damage
                if gs.targets[self.faction][i].health <= 0:
                    explosion = ShipExplosion(gs.targets[self.faction][i].centerx, gs.targets[self.faction][i].centery, gs)
                    explosion_group.add(explosion)
            if not self.pen:
                gs.bullets[self.faction].remove(self)

            # pygame.event.post(pygame.event.Event(RED_HIT))
        elif self.timer > self.range / self.velocity:  # missile runs out of thrust
            gs.bullets[self.faction].remove(self)

        self.timer += 1
        # elif self.x > width or self.x < 0 or self.y > height or self.y < 0:  # bullets leaves arena
        #     bullet_list.remove(self)


"""MISSILE CLASS"""

class Missile(pygame.Rect):
    def __init__(self, x, y, angle, height, width, missile_type, target, faction):
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
        self.arm = 60
        self.target = target
        self.emp = missile_type.emp
        self.image = missile_type.image
        self.missile_type = missile_type
        self.faction = faction
        # for i in range(len(gs.ships)):
        #     if i != faction:
        #         self.target_list.extend(gs.ships[i])

    def scoot(self, explosion_group, gs):

        for i in range(self.missile_type.par_str):
            gs.particle_list.append(Particle(self.centerx, self.centery, -rnd.randint(3, 5), self.angle + rnd.randint(-self.missile_type.par_rnd, self.missile_type.par_rnd), 5, (255, rnd.randint(0, 255), 0)))

        if self.target is None or self.target.health <= 0:
            # self.target_list = []
            # for i in range(len(gs.ships)):
            #     if i != self.faction:
            #         self.target_list.extend(gs.ships[i])

            self.target = FindNearest(self.centerx, self.centery, gs.targets[self.faction])

        if self.target is None:
            explosion = MissileExplosion(self.centerx, self.centery, gs, self.er)
            explosion_group.add(explosion)
            gs.missiles[self.faction].remove(self)

        else:
            if self.missile_type.drunk:
                da = 400 * np.cross((math.sin(self.angle * math.pi / 180), math.cos(self.angle * math.pi / 180), 0),
                              (self.target.centerx - self.centerx, self.target.centery - self.centery, 0))[2] / min([((self.target.centerx - self.centerx) ** 2 + (self.target.centery - self.centery) ** 2 + 1), (self.range / 2) ** 2]) + math.sin(self.timer / 10) + 2 * rnd.random() - 1
                # print(min([((self.target.centerx - self.centerx) ** 2 + (self.target.centery - self.centery) ** 2 + 1), self.range ** 2]))
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

        if self.collidelist(gs.targets[self.faction]) != -1 and self.timer > self.arm:  # missile hits target
            dmgList = self.collidelistall(gs.targets[self.faction])
            for i in dmgList:
                gs.targets[self.faction][i].health -= self.damage
                if self.emp:
                    gs.targets[self.faction][i].energy = 0
                    # target_list[i].bulletC += 180
                    # target_list[i].missileC += 180
                    for turret in gs.targets[self.faction][i].turrets:
                        turret.energy = 0
                        turret.angle += 360 * rnd.uniform(-1, 1) / math.pi
                        # turret.bulletC += 180
                        # turret.missileC += 180

                if gs.targets[self.faction][i].health <= 0:
                    explosion = ShipExplosion(gs.targets[self.faction][i].centerx, gs.targets[self.faction][i].centery, gs)
                    explosion_group.add(explosion)
            explosion = MissileExplosion(self.centerx, self.centery, gs, self.er)
            explosion_group.add(explosion)
            ExplosionDamage(self.explosion_damage, self.centerx, self.centery, self.er, gs.targets[self.faction], explosion_group, gs)
            gs.missiles[self.faction].remove(self)

        elif self.timer > self.range / self.velocity:  # missile runs out of thrust
            explosion = MissileExplosion(self.centerx, self.centery, gs, self.er)
            explosion_group.add(explosion)
            ExplosionDamage(self.explosion_damage, self.centerx, self.centery, self.er, gs.targets[self.faction], explosion_group, gs)
            gs.missiles[self.faction].remove(self)

        self.timer += 1

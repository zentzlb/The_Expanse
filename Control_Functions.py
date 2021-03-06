import pygame
import math
import numpy as np

from Misc import FindNearest


def NPControl(ship, width, height, bullet_velocity, bullet_list, missile_list, target_list):

    commands = []

    if ship.target is None or ship.target.health >= 0 or ship.counter == 60:
        ship.target = FindNearest(ship.centerx, ship.centery, target_list)
        ship.counter = 0
    else:
        ship.counter += 1

    if ship.target is not None:
        vx = ship.target.vx
        vy = ship.target.vy
        xo = ship.target.centerx
        yo = ship.target.centery

        a = vx ** 2 + vy ** 2 - bullet_velocity ** 2
        b = 2 * (vx * (xo - ship.centerx) + vy * (yo - ship.centery))
        c = (xo - ship.centerx) ** 2 + (yo - ship.centery) ** 2

        t = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        x = xo + vx * t
        y = yo + vy * t

        dx = x - ship.x
        dy = y - ship.y

        cos = math.cos(ship.angle * math.pi / 180)
        sin = math.sin(ship.angle * math.pi / 180)

        Q = np.array([[cos, -sin], [sin, cos]])
        V = np.array([[dx], [dy]])
        V_prime = Q.dot(V)
        angle2 = math.atan2(V_prime[0][0], V_prime[1][0])

        # print(angle2)

        if angle2 > ship.av * math.pi / 360:  # LEFT
            commands.append(1)
        elif angle2 < -ship.av * math.pi / 360:  # RIGHT
            commands.append(-1)
        else:
            commands.append(0)

        """GO FORWARD"""
        commands.append(1)

        """NO LATERAL ACCELERATION"""
        commands.append(0)

        """SHOOT"""
        if abs(angle2 * 180 / math.pi) < ship.av and ship.energy >= 30 and ship.bulletC == 0:  # SHOOT BULLET
            commands.append(1)
            commands.append(0)
        elif ship.energy >= 150 and ship.missileC == 0:
            commands.append(0)
            commands.append(1)
        else:
            commands.append(0)
            commands.append(0)
    else:
        commands = [0, 0, 0, 0, 0]

    return commands

def PlayerControl1(ship, width, height, bullet_velocity, bullet_list, missile_list, target_list):

    keys_pressed = pygame.key.get_pressed()
    commands = []

    """MOVEMENT"""
    if keys_pressed[pygame.K_q]:  # LEFT
        commands.append(1)
    elif keys_pressed[pygame.K_e]:  # RIGHT
        commands.append(-1)
    else:
        commands.append(0)

    if keys_pressed[pygame.K_w]:  # UP
        commands.append(1)
    elif keys_pressed[pygame.K_s]:  # DOWN
        commands.append(-1)
    else:
        commands.append(0)

    if keys_pressed[pygame.K_a]:  # LEFT
        commands.append(1)
    elif keys_pressed[pygame.K_d]:  # RIGHT
        commands.append(-1)
    else:
        commands.append(0)

    if keys_pressed[pygame.K_SPACE]:  # fire bullet
        commands.append(1)
        commands.append(0)
    elif keys_pressed[pygame.K_m]:  # fire missile
        commands.append(0)
        commands.append(1)
    else:
        commands.append(0)
        commands.append(0)

    return commands

import pygame
import math
import numpy as np

from Misc import FindNearest


"""NPC LOGIC"""


def NPControl(ship, bullet_velocity, bullet_list, missile_list, target_list):

    commands = []

    if ship.target is None or ship.target.health <= 0 or ship.counter >= 60:
        new_target = FindNearest(ship.centerx, ship.centery, target_list)
        ship.target = new_target
        if new_target is not None:  # don't lose lock
            ship.target = new_target
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

        dx = x - ship.centerx
        dy = y - ship.centery

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
        if abs(angle2 * 180 / math.pi) < ship.av and ship.energy >= 30 and ship.bullet_type.range > math.sqrt((xo - ship.centerx) ** 2 + (yo - ship.centery) ** 2):  # SHOOT BULLET
            commands.append(1)
        else:
            commands.append(0)
        if ship.energy >= 150 and ship.missile_type.range > math.sqrt(dx ** 2 + dy ** 2):
            commands.append(1)
        else:
            commands.append(0)

        """BOOST"""
        if ship.health < 20 and ((ship.energy > ship.bullet_type.energy and ship.boost) or ship.energy > ship.bullet_type.energy + 30):
            commands.append(1)
        else:
            commands.append(0)

    else:
        commands = [0, 0, 0, 0, 0, 0]

    return commands


"""TURRET CONTROLS"""

def TurretControl(ship, bullet_velocity, bullet_list, missile_list, target_list):

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

        dx = x - ship.centerx
        dy = y - ship.centery

        cos = math.cos(ship.angle * math.pi / 180)
        sin = math.sin(ship.angle * math.pi / 180)

        Q = np.array([[cos, -sin], [sin, cos]])
        V = np.array([[dx], [dy]])
        V_prime = Q.dot(V)
        angle2 = math.atan2(V_prime[0][0], V_prime[1][0])

        if angle2 > ship.av * math.pi / 360:  # LEFT
            commands.append(1)
        elif angle2 < -ship.av * math.pi / 360:  # RIGHT
            commands.append(-1)
        else:
            commands.append(0)

        """SHOOT"""
        if abs(angle2 * 180 / math.pi) < ship.av and ship.energy >= 30 and ship.bullet_type.range > math.sqrt((xo - ship.centerx) ** 2 + (yo - ship.centery) ** 2):  # SHOOT BULLET
            commands.append(1)
        else:
            commands.append(0)
        if ship.missile_type is not None and (ship.energy >= 150 and ship.missile_type.range > math.sqrt(dx ** 2 + dy ** 2)):
            commands.append(1)
        else:
            commands.append(0)

    else:
        commands = [0, 0, 0]



    return commands


"""PLAYER KEYBOARD CONTROLS"""


def PlayerControl1(ship, bullet_velocity, bullet_list, missile_list, target_list):

    keys_pressed = pygame.key.get_pressed()
    commands = []

    if keys_pressed[pygame.K_UP]:  # LOCK ONTO THE NEAREST TARGET
        ship.target = FindNearest(ship.centerx, ship.centery, target_list)
    elif keys_pressed[pygame.K_DOWN]:  # REMOVE TARGET LOCK
        ship.target = None

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
    else:
        commands.append(0)

    if keys_pressed[pygame.K_m]:  # fire missile
        commands.append(1)
    else:
        commands.append(0)

    if keys_pressed[pygame.K_LSHIFT]:
        commands.append(1)
    else:
        commands.append(0)

    return commands

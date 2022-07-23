import pygame
import os
import math
from Misc import TargetingComputer


def draw_window(red_ships, yellow_ships, red_bullets, yellow_bullets, red_missiles, yellow_missiles, WIN, HUD, SPACE, DUST, FONT, spaceship_height, spaceship_width, explosion_group, global_state):



    HUD.fill((0,0,0,0))
    rr = 100  # radar radius
    hbh = 30  # health bar height



    COLOR = (40, 10, 35)  # define window color
    BLACK = (0, 50, 0)  # BLACK
    RED = (255, 0, 0)  # RED
    YELLOW = (255, 255, 0)  # YELLOW
    GREEN = (0, 255, 0)  # green
    BLUE = (75, 75, 255)  # blue
    WIN.blit(SPACE, (0, 0))  # draw background

    # print([global_state.x % 2000, global_state.y % 2000])
    WIN.blit(DUST, (-2000 - global_state.x % 2000, -2000 - global_state.y % 2000))  # draw foreground

    # MISSILE_IMAGE = pygame.image.load(os.path.join('Assets', 'smallmissile1.png'))  # missile
    # BULLET_IMAGE = pygame.image.load(os.path.join('Assets', 'bullet.png'))  # bullet

    # WIN.fill(COLOR)  # fill window with color
    # pygame.draw.rect(WIN, BLACK, BORDER)

    # if len(red_ships) > 0:
    #     red_health_text = FONT.render(f"Health: {red_ships[0].health} Energy: {red_ships[0].energy}", 1, RED)
    # else:
    #     red_health_text = FONT.render(f"ALL SHIPS DESTROYED", 1, RED)
    #
    # if len(yellow_ships) > 0:
    #     yellow_health_text = FONT.render(f"Health: {yellow_ships[0].health} Energy: {yellow_ships[0].energy}", 1, YELLOW)
    # else:
    #     yellow_health_text = FONT.render(f"ALL SHIPS DESTROYED", 1, YELLOW)

    # WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))  # display red health
    # WIN.blit(yellow_health_text, (yellow_health_text.get_width() - 10, 10))  # display yellow health

    for yellow in yellow_ships:
        if yellow.health > 0:
            if yellow.forward:
                SHIP = pygame.transform.rotate(yellow.imagef, yellow.angle)  # display with thrusters active
            else:
                SHIP = pygame.transform.rotate(yellow.image, yellow.angle)  # display without thrusters
            # pygame.draw.rect(WIN, GREEN, yellow)
            WIN.blit(SHIP, (yellow.cx - global_state.x, yellow.cy - global_state.y))
            for turret in yellow.turrets:
                TURRET = pygame.transform.rotate(turret.image, turret.angle)
                WIN.blit(TURRET, (turret.cx - global_state.x, turret.cy - global_state.y))


            if not yellow.is_player:  # ship is not player controlled
                """HEALTH BAR"""
                pygame.draw.line(WIN, GREEN, (yellow.x - global_state.x, yellow.y - global_state.y), (
                yellow.x + 50 * yellow.health / yellow.Health - global_state.x, yellow.y - global_state.y), 4)

                """ENERGY BAR"""
                pygame.draw.line(WIN, BLUE, (yellow.x - global_state.x, yellow.y - 4 - global_state.y), (yellow.x + 50 * yellow.energy / yellow.Energy - global_state.x, yellow.y - 4 - global_state.y), 4)

            else:  # player controlled ship
                """DRAW HEALTH AND ENERGY BARS"""
                pygame.draw.line(HUD, (0, 255, 0, 60), (3, 2 * rr + hbh), (3 + 2 * rr * yellow.health / yellow.Health, 2 * rr + hbh), hbh)
                pygame.draw.line(HUD, (80, 100, 255, 60), (3, 2 * rr + 2 * hbh + 3), (3 + 2 * rr * yellow.energy / yellow.Energy, 2 * rr + 2 * hbh + 3), hbh)
                pygame.draw.line(WIN, (200, 200, 255), (0, 2 * rr + hbh / 2), (3 + 2 * rr + 3, 2 * rr + hbh / 2), 3)
                pygame.draw.line(WIN, (200, 200, 255), (0, 2 * rr + 3 * hbh / 2 + 2), (3 + 2 * rr + 3, 2 * rr + 3 * hbh / 2 + 2), 3)
                pygame.draw.line(WIN, (200, 200, 255), (0, 2 * rr + 5 * hbh / 2 + 5), (3 + 2 * rr + 3, 2 * rr + 5 * hbh / 2 + 5), 3)
                pygame.draw.line(WIN, (200, 200, 255), (1, 2 * rr + hbh / 2), (1, 2 * rr + 5 * hbh / 2 + 5), 3)
                pygame.draw.line(WIN, (200, 200, 255), (3 + 2 * rr + 2, 2 * rr + hbh / 2), (3 + 2 * rr + 2, 2 * rr + 5 * hbh / 2 + 5), 3)

                health_text = FONT.render(f"Shields: {100 * yellow.health / yellow.Health:0.0f}%", 1, YELLOW)
                energy_text = FONT.render(f"Energy: {100 * yellow.energy / yellow.Energy:0.0f}%", 1, YELLOW)
                HUD.blit(health_text, (7, 2 * rr + hbh / 2))  # display yellow health
                HUD.blit(energy_text, (7, 2 * rr + 3 * hbh / 2 + 3))  # display yellow energy

                if yellow.target is not None and yellow.target.health > 0:
                    MyAngle = TargetingComputer(yellow)
                    # print([90 - MyAngle * 180 / math.pi, yellow.angle, MyAngle * 180 / math.pi - yellow.angle])
                    if abs(90 - MyAngle * 180 / math.pi - yellow.angle) < yellow.av:
                        MyColor = GREEN
                    else:
                        MyColor = RED
                    pygame.draw.line(WIN, MyColor, (round(yellow.centerx - global_state.x + 25 * math.cos(MyAngle)), round(yellow.centery - global_state.y + 25 * math.sin(MyAngle))), (round(yellow.centerx - global_state.x + 50 * math.cos(MyAngle)), round(yellow.centery - global_state.y + 50 * math.sin(MyAngle))), 3)
                # pygame.draw.line(WIN, BLUE, (yellow.x - global_state.x, yellow.y - 4 - global_state.y), (
                # yellow.x + 50 * yellow.energy / yellow.Energy - global_state.x, yellow.y - 4 - global_state.y), 4)

            # pygame.draw.line(WIN, BLUE, (yellow.centerx, yellow.centery), (0, 0))

    for red in red_ships:

        if red.health > 0:
            if red.forward:
                SHIP = pygame.transform.rotate(red.imagef, red.angle)  # display with thrusters active
            else:
                SHIP = pygame.transform.rotate(red.image, red.angle)  # display ship without thrusters
            # pygame.draw.circle(WIN, YELLOW, red.center, 5)
            # pygame.draw.rect(WIN, GREEN, red)
            WIN.blit(SHIP, (red.cx - global_state.x, red.cy - global_state.y))
            pygame.draw.line(WIN, GREEN, (red.x - global_state.x, red.y - global_state.y), (red.x + 50 * red.health / red.Health - global_state.x, red.y - global_state.y), 4)
            pygame.draw.line(WIN, YELLOW, (red.x - global_state.x, red.y - 4 - global_state.y), (red.x + 50 * red.energy / red.Energy - global_state.x, red.y - 4 - global_state.y), 4)

            for turret in red.turrets:
                TURRET = pygame.transform.rotate(turret.image, turret.angle)
                WIN.blit(TURRET, (turret.cx - global_state.x, turret.cy - global_state.y))

    """DISPLAY BULLETS AND MISSILES"""
    for bullet in yellow_bullets:
        # BULLET = pygame.transform.rotate(bullet.image, bullet.angle)
        WIN.blit(bullet.image, (bullet.x - global_state.x, bullet.y - global_state.y))
    for missile in yellow_missiles:
        MISSILE = pygame.transform.rotate(missile.image, missile.angle)
        WIN.blit(MISSILE, (missile.x - global_state.x, missile.y - global_state.y))
    for bullet in red_bullets:
        # BULLET = pygame.transform.rotate(bullet.image, bullet.angle)
        WIN.blit(bullet.image, (bullet.x - global_state.x, bullet.y - global_state.y))
    for missile in red_missiles:
        MISSILE = pygame.transform.rotate(missile.image, missile.angle)
        WIN.blit(MISSILE, (missile.x - global_state.x, missile.y - global_state.y))

    explosion_group.draw(WIN)

    """RADAR"""
    pygame.draw.circle(HUD, (0, 0, 255, 50), (rr + 3, rr + 3), rr)
    pygame.draw.circle(WIN, (200, 200, 255), (rr + 3, rr + 3), rr + 3, width=3)
    WIN.blit(HUD, (0, 0))
    pygame.draw.circle(WIN, GREEN, (rr + 3, rr + 3), 6)

    for ship in yellow_ships:
        dx = ship.centerx - global_state.cx
        dy = ship.centery - global_state.cy
        d = math.sqrt(dx ** 2 + dy ** 2)
        r = 1.2 * math.log((d ** 2) / (1000 + d) + 1) ** 2
        angle = math.atan2(dy, dx)
        X = rr + r * math.cos(angle) + 3
        Y = rr + r * math.sin(angle) + 3
        pygame.draw.circle(WIN, YELLOW, (X, Y), 4)

    for ship in red_ships:
        dx = ship.centerx - global_state.cx
        dy = ship.centery - global_state.cy
        d = math.sqrt(dx ** 2 + dy ** 2)
        r = 1.2 * math.log((d ** 2) / (1000 + d) + 1) ** 2
        angle = math.atan2(dy, dx)
        X = rr + r * math.cos(angle) + 3
        Y = rr + r * math.sin(angle) + 3
        pygame.draw.circle(WIN, RED, (X, Y), 4)

    for missile in yellow_missiles:
        dx = missile.centerx - global_state.cx
        dy = missile.centery - global_state.cy
        d = math.sqrt(dx ** 2 + dy ** 2)
        r = 1.2 * math.log((d ** 2) / (1000 + d) + 1) ** 2
        angle = math.atan2(dy, dx)
        X = rr + r * math.cos(angle) + 3
        Y = rr + r * math.sin(angle) + 3
        pygame.draw.circle(HUD, YELLOW, (X, Y), 1)

    for missile in red_missiles:
        dx = missile.centerx - global_state.cx
        dy = missile.centery - global_state.cy
        d = math.sqrt(dx ** 2 + dy ** 2)
        r = 1.2 * math.log((d ** 2) / (1000 + d) + 1) ** 2
        angle = math.atan2(dy, dx)
        X = rr + r * math.cos(angle) + 3
        Y = rr + r * math.sin(angle) + 3
        pygame.draw.circle(WIN, RED, (X, Y), 1)

    WIN.blit(HUD, (0, 0))

    pygame.display.update()  # update window

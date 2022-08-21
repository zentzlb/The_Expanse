import pygame
import os
import math
import time
from Misc import TargetingComputer
from Menus import StationMenu


def draw_window(red_ships, yellow_ships, red_bullets, yellow_bullets, red_missiles, yellow_missiles, yellow_stations, asteroids, WIN, HUD, SPACE, DUST, spaceship_height, spaceship_width, explosion_group, global_state, fps, HEIGHT, WIDTH):

    keys_pressed = pygame.key.get_pressed()

    HUD.fill((0, 0, 0, 0))
    rr = 100  # radar radius
    hbh = 30  # health bar height
    bar_thickness = 3



    COLOR = (40, 10, 35)  # define window color
    BLACK = (0, 50, 0)  # BLACK
    RED = (255, 0, 0)  # RED
    YELLOW = (255, 255, 0)  # YELLOW
    GREEN = (0, 255, 0)  # green
    BLUE = (75, 75, 255)  # blue
    SILVER = (200, 200, 255)  # silver

    # t1 =time.time()
    WIN.blit(SPACE, (0, 0))  # draw background
    # t2 = time.time()
    # print(f"ship subroutine: {t2 - t1}")

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
    if keys_pressed[pygame.K_PERIOD]:
        global_state.show_bars = True
    elif keys_pressed[pygame.K_COMMA]:
        global_state.show_bars = False

    for yellow in yellow_stations:
        if (yellow.cx - global_state.x > WIDTH or yellow.cx - global_state.x + yellow.width > 0) and (yellow.cy - global_state.y > HEIGHT or yellow.cy - global_state.y + yellow.height > 0):
            WIN.blit(yellow.image, (yellow.cx - global_state.x, yellow.cy - global_state.y))
            for turret in yellow.turrets:
                TURRET = pygame.transform.rotate(turret.image, turret.angle)
                WIN.blit(TURRET, (turret.cx - global_state.x, turret.cy - global_state.y))

    for roid in asteroids:
        if (roid.x - global_state.x > WIDTH or roid.x - global_state.x + roid.width > 0) and (roid.y - global_state.y > HEIGHT or roid.y - global_state.y + roid.height > 0):
            ROID = pygame.transform.rotate(roid.image, roid.angle)
            WIN.blit(ROID, (roid.x - global_state.x, roid.y - global_state.y))


    for yellow in yellow_ships:
        if yellow.health > 0 and (yellow.cx - global_state.x > WIDTH or yellow.cx - global_state.x + yellow.width > 0) and (yellow.cy - global_state.y > HEIGHT or yellow.cy - global_state.y + yellow.height > 0):
            if yellow.forward:
                SHIP = pygame.transform.rotate(yellow.ship_type.imagef, yellow.angle)  # display with thrusters active
            else:
                SHIP = pygame.transform.rotate(yellow.ship_type.image, yellow.angle)  # display without thrusters
            # pygame.draw.rect(WIN, GREEN, yellow)
            WIN.blit(SHIP, (yellow.cx - global_state.x, yellow.cy - global_state.y))
            for turret in yellow.turrets:
                TURRET = pygame.transform.rotate(turret.image, turret.angle)
                WIN.blit(TURRET, (turret.cx - global_state.x, turret.cy - global_state.y))

            if not yellow.is_player and global_state.show_bars:  # ship is not player controlled
                """HEALTH BAR"""
                pygame.draw.line(WIN, GREEN, (yellow.x - global_state.x, yellow.y - global_state.y - 5), (
                yellow.x + 50 * yellow.health / yellow.ship_type.energy - global_state.x, yellow.y - global_state.y - 5), bar_thickness)

                """ENERGY BAR"""
                pygame.draw.line(WIN, BLUE, (yellow.x - global_state.x, yellow.y - bar_thickness - global_state.y - 5), (yellow.x + 50 * yellow.energy / yellow.ship_type.energy - global_state.x, yellow.y - bar_thickness - global_state.y - 5), bar_thickness)

            elif yellow.is_player:  # player controlled ship

                """DRAW INFO BOX"""

                # translatex = 1000
                # translatey = 25
                #
                #
                # box_tl = (1 + translatex, 2 * rr + 5 * hbh / 2 + 5 + translatey)
                # box_bl = (1 + translatex, 4 * rr + 5 * hbh / 2 + 10 + translatey)
                # box_tr = (5 + 2 * rr + translatex, 2 * rr + 5 * hbh / 2 + 5 + translatey)
                # box_br = (5 + 2 * rr + translatex, 4 * rr + 5 * hbh / 2 + 10 + translatey)
                #
                # pygame.draw.line(HUD, SILVER, box_tl, box_tr, 3)  # top line
                # pygame.draw.line(HUD, SILVER, box_tl, box_bl, 3)  # left line
                # pygame.draw.line(HUD, SILVER, box_tr, box_br, 3)  # right line
                # pygame.draw.line(HUD, SILVER, box_bl, box_br, 3)  # bottom line

                """DRAW HEALTH AND ENERGY BARS"""
                pygame.draw.line(HUD, (0, 255, 0, 60), (3, 2 * rr + hbh), (3 + 2 * rr * yellow.health / yellow.ship_type.health, 2 * rr + hbh), hbh)
                pygame.draw.line(HUD, (80, 100, 255, 60), (3, 2 * rr + 2 * hbh + 3), (3 + 2 * rr * yellow.energy / yellow.ship_type.energy, 2 * rr + 2 * hbh + 3), hbh)
                pygame.draw.line(HUD, SILVER, (0, 2 * rr + hbh / 2), (3 + 2 * rr + 3, 2 * rr + hbh / 2), 3)
                pygame.draw.line(HUD, SILVER, (0, 2 * rr + 3 * hbh / 2 + 2), (3 + 2 * rr + 3, 2 * rr + 3 * hbh / 2 + 2), 3)
                pygame.draw.line(HUD, SILVER, (0, 2 * rr + 5 * hbh / 2 + 5), (3 + 2 * rr + 3, 2 * rr + 5 * hbh / 2 + 5), 3)
                pygame.draw.line(HUD, SILVER, (1, 2 * rr + hbh / 2), (1, 2 * rr + 5 * hbh / 2 + 5), 3)
                pygame.draw.line(HUD, SILVER, (3 + 2 * rr + 2, 2 * rr + hbh / 2), (3 + 2 * rr + 2, 2 * rr + 5 * hbh / 2 + 5), 3)

                """DRAW TARGET WINDOW"""
                box_tl = (1, 2 * rr + 5 * hbh / 2 + 5)
                box_bl = (1, 4 * rr + 5 * hbh / 2 + 10)
                box_tr = (5 + 2 * rr, 2 * rr + 5 * hbh / 2 + 5)
                box_br = (5 + 2 * rr, 4 * rr + 5 * hbh / 2 + 10)
                center = ((box_tr[0] + box_tl[0] - 3) // 2, (box_bl[1] + box_tl[1] - 3) // 2)  # center of box
                pygame.draw.line(HUD, SILVER, box_tl, box_bl, 3)  # left line
                pygame.draw.line(HUD, SILVER, box_tr, box_br, 3)  # right line
                pygame.draw.line(HUD, SILVER, box_bl, box_br, 3)  # bottom line


                health_text = global_state.fonts[0].render(f"{fps} Shields: {100 * yellow.health / yellow.ship_type.health:0.0f}%", 1, YELLOW)
                energy_text = global_state.fonts[0].render(f"Energy: {100 * yellow.energy / yellow.ship_type.energy:0.0f}%", 1, YELLOW)
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

                    """DRAW TARGET"""

                    target_rect = pygame.Rect(box_tl[0] + 2, box_tl[1] + 2, box_tr[0] - box_tl[0] - 3, box_bl[1] - box_tl[1] - 3)
                    pygame.draw.rect(HUD, (255, 0, 0, 15), target_rect)

                    SHIP = pygame.transform.rotate(yellow.target.ship_type.image, yellow.target.angle)
                    adjust_x = (yellow.target.width - yellow.target.height * abs(math.sin(yellow.target.angle * math.pi / 180)) - yellow.target.width * abs(math.cos(yellow.target.angle * math.pi / 180))) / 2
                    adjust_y = (yellow.target.height - yellow.target.width * abs(math.sin(yellow.target.angle * math.pi / 180)) - yellow.target.height * abs(math.cos(yellow.target.angle * math.pi / 180))) / 2
                    HUD.blit(SHIP, (center[0] - yellow.target.width // 2 + adjust_x, center[1] - yellow.target.height // 2 + adjust_y))










                # pygame.draw.line(WIN, BLUE, (yellow.x - global_state.x, yellow.y - 4 - global_state.y), (
                # yellow.x + 50 * yellow.energy / yellow.Energy - global_state.x, yellow.y - 4 - global_state.y), 4)

            # pygame.draw.line(WIN, BLUE, (yellow.centerx, yellow.centery), (0, 0))

    for red in red_ships:

        if red.health > 0 and (red.cx - global_state.x > WIDTH or red.cx - global_state.x + red.width > 0) and (red.cy - global_state.y > HEIGHT or red.cy - global_state.y + red.height > 0):
            if red.forward:
                SHIP = pygame.transform.rotate(red.ship_type.imagef, red.angle)  # display with thrusters active
            else:
                SHIP = pygame.transform.rotate(red.ship_type.image, red.angle)  # display ship without thrusters
            # pygame.draw.circle(WIN, YELLOW, red.center, 5)
            # pygame.draw.rect(WIN, GREEN, red)
            WIN.blit(SHIP, (red.cx - global_state.x, red.cy - global_state.y))
            if global_state.show_bars:
                pygame.draw.line(WIN, GREEN, (red.x - global_state.x, red.y - global_state.y), (red.x + 50 * red.health / red.ship_type.health - global_state.x, red.y - global_state.y), 4)
                pygame.draw.line(WIN, YELLOW, (red.x - global_state.x, red.y - 4 - global_state.y), (red.x + 50 * red.energy / red.ship_type.energy - global_state.x, red.y - 4 - global_state.y), 4)

            for turret in red.turrets:
                TURRET = pygame.transform.rotate(turret.image, turret.angle)
                WIN.blit(TURRET, (turret.cx - global_state.x, turret.cy - global_state.y))

    """DISPLAY BULLETS AND MISSILES"""
    for bullet in yellow_bullets:
        if (bullet.x - global_state.x > WIDTH or bullet.x - global_state.x + bullet.width > 0) and (bullet.y - global_state.y > HEIGHT or bullet.y - global_state.y + bullet.height > 0):
            WIN.blit(bullet.image, (bullet.x - global_state.x, bullet.y - global_state.y))
    for missile in yellow_missiles:
        if (missile.x - global_state.x > WIDTH or missile.x - global_state.x + missile.width > 0) and (missile.y - global_state.y > HEIGHT or missile.y - global_state.y + missile.height > 0):
            MISSILE = pygame.transform.rotate(missile.image, missile.angle)
            WIN.blit(MISSILE, (missile.x - global_state.x, missile.y - global_state.y))
    for bullet in red_bullets:
        if (bullet.x - global_state.x > WIDTH or bullet.x - global_state.x + bullet.width > 0) and (bullet.y - global_state.y > HEIGHT or bullet.y - global_state.y + bullet.height > 0):
            WIN.blit(bullet.image, (bullet.x - global_state.x, bullet.y - global_state.y))
    for missile in red_missiles:
        if (missile.x - global_state.x > WIDTH or missile.x - global_state.x + missile.width > 0) and (missile.y - global_state.y > HEIGHT or missile.y - global_state.y + missile.height > 0):
            MISSILE = pygame.transform.rotate(missile.image, missile.angle)
            WIN.blit(MISSILE, (missile.x - global_state.x, missile.y - global_state.y))

    for i in global_state.particle_list:
        i.update()
        pygame.draw.circle(WIN, i.color, (i.x - global_state.x, i.y - global_state.y), i.radius)

    for i in global_state.particle_list:
        if i.radius <= 0:
            global_state.particle_list.remove(i)


    explosion_group.draw(WIN)

    """RADAR"""
    if global_state.menu is None:
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

        for station in yellow_stations:
            dx = station.centerx - global_state.cx
            dy = station.centery - global_state.cy
            d = math.sqrt(dx ** 2 + dy ** 2)
            r = 1.2 * math.log((d ** 2) / (1000 + d) + 1) ** 2
            angle = math.atan2(dy, dx)
            X = rr + r * math.cos(angle) + 3
            Y = rr + r * math.sin(angle) + 3
            radarRect = pygame.Rect(X-5, Y-5, 10, 10)
            pygame.draw.rect(WIN, YELLOW, radarRect)
            # pygame.draw.circle(WIN, YELLOW, (X, Y), 4)

        for roid in asteroids:
            dx = roid.centerx - global_state.cx
            dy = roid.centery - global_state.cy
            d = math.sqrt(dx ** 2 + dy ** 2)
            r = 1.2 * math.log((d ** 2) / (1000 + d) + 1) ** 2
            angle = math.atan2(dy, dx)
            X = rr + r * math.cos(angle) + 3
            Y = rr + r * math.sin(angle) + 3
            pygame.draw.circle(WIN, (255, 255, 255), (X, Y), 5)

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

    else:

        global_state.menu.draw_menu(HUD, yellow_ships, red_ships, yellow_stations, global_state)

        # pygame.draw.circle(HUD, (0, 0, 50, 80), (550, 550), 100)
        # health_text = FONT.render(f"Ship", True, (255, 0, 0, 255))
        # HUD.blit(health_text, (100, 100))  # display yellow health



    WIN.blit(HUD, (0, 0))

    pygame.display.update()  # update window

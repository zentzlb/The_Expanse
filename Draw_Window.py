import pygame
import os
import math

def draw_window(red_ships, yellow_ships, red_bullets, yellow_bullets, red_missiles, yellow_missiles, WIN, SPACE, FONT, spaceship_height, spaceship_width, explosion_group, global_state):

    rr = 100  # radar radius

    COLOR = (40, 10, 35)  # define window color
    BLACK = (0, 50, 0)  # BLACK
    RED = (255, 0, 0)  # RED
    YELLOW = (255, 255, 0)  # YELLOW
    GREEN = (0, 255, 0)
    BLUE = (75, 75, 255)
    WIN.blit(SPACE, (0, 0))

    Y_SHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'yellow_ship.png'))  # yellow spaceship
    R_SHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'red_ship.png'))  # red spaceship
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
        Y_SHIP = pygame.transform.rotate(pygame.transform.scale(Y_SHIP_IMAGE, (spaceship_height, spaceship_width)), yellow.angle)
        if yellow.health > 0:
            # pygame.draw.rect(WIN, GREEN, yellow)
            WIN.blit(Y_SHIP, (yellow.cx - global_state.x, yellow.cy - global_state.y))

            if not yellow.is_player:
                pygame.draw.line(WIN, GREEN, (yellow.x - global_state.x, yellow.y - global_state.y), (
                yellow.x + 50 * yellow.health / yellow.Health - global_state.x, yellow.y - global_state.y), 4)
                pygame.draw.line(WIN, BLUE, (yellow.x - global_state.x, yellow.y - 4 - global_state.y), (yellow.x + 50 * yellow.energy / yellow.Energy - global_state.x, yellow.y - 4 - global_state.y), 4)
            else:
                pygame.draw.line(WIN, GREEN, (1, 2 * rr + 10), (1 + 2 * rr * yellow.health / yellow.Health, 2 * rr + 10), 20)
                pygame.draw.line(WIN, BLUE, (1, 2 * rr + 30), (1 + 2 * rr * yellow.energy / yellow.Energy, 2 * rr + 30), 20)
                # pygame.draw.line(WIN, BLUE, (yellow.x - global_state.x, yellow.y - 4 - global_state.y), (
                # yellow.x + 50 * yellow.energy / yellow.Energy - global_state.x, yellow.y - 4 - global_state.y), 4)

            # pygame.draw.line(WIN, BLUE, (yellow.centerx, yellow.centery), (0, 0))


    for red in red_ships:
        R_SHIP = pygame.transform.rotate(pygame.transform.scale(R_SHIP_IMAGE, (spaceship_height, spaceship_width)), red.angle)
        if red.health > 0:
            # pygame.draw.circle(WIN, YELLOW, red.center, 5)
            # pygame.draw.rect(WIN, GREEN, red)
            WIN.blit(R_SHIP, (red.cx - global_state.x, red.cy - global_state.y))
            pygame.draw.line(WIN, GREEN, (red.x - global_state.x, red.y - global_state.y), (red.x + 50 * red.health / red.Health - global_state.x, red.y - global_state.y), 4)
            pygame.draw.line(WIN, YELLOW, (red.x - global_state.x, red.y - 4 - global_state.y), (red.x + 50 * red.energy / red.Energy - global_state.x, red.y - 4 - global_state.y), 4)


    for bullet in yellow_bullets:
        # pygame.draw.rect(WIN, YELLOW, bullet)
        BULLET = pygame.transform.rotate(pygame.transform.scale(bullet.image, (bullet.height, bullet.width)), bullet.angle)
        WIN.blit(BULLET, (bullet.x - global_state.x, bullet.y - global_state.y))
    for missile in yellow_missiles:
        MISSILE = pygame.transform.rotate(pygame.transform.scale(missile.image, (missile.height, missile.width)), missile.angle)
        WIN.blit(MISSILE, (missile.x - global_state.x, missile.y - global_state.y))
    for bullet in red_bullets:
        # pygame.draw.rect(WIN, RED, bullet)
        BULLET = pygame.transform.rotate(pygame.transform.scale(bullet.image, (bullet.height, bullet.width)), bullet.angle)
        WIN.blit(BULLET, (bullet.x - global_state.x, bullet.y - global_state.y))
    for missile in red_missiles:
        MISSILE = pygame.transform.rotate(pygame.transform.scale(missile.image, (missile.height, missile.width)), missile.angle)
        WIN.blit(MISSILE, (missile.x - global_state.x, missile.y - global_state.y))

    explosion_group.draw(WIN)

    """RADAR"""
    pygame.draw.circle(WIN, BLUE, (rr, rr), rr)
    pygame.draw.circle(WIN, GREEN, (rr, rr), 6)

    for ship in yellow_ships:
        dx = ship.centerx - global_state.cx
        dy = ship.centery - global_state.cy
        d = math.sqrt(dx ** 2 + dy ** 2)
        r = 1.2 * math.log((d ** 2) / (1000 + d) + 1) ** 2
        angle = math.atan2(dy, dx)
        X = rr + r * math.cos(angle)
        Y = rr + r * math.sin(angle)
        pygame.draw.circle(WIN, YELLOW, (X, Y), 4)

    for ship in red_ships:
        dx = ship.centerx - global_state.cx
        dy = ship.centery - global_state.cy
        d = math.sqrt(dx ** 2 + dy ** 2)
        r = 1.2 * math.log((d ** 2) / (1000 + d) + 1) ** 2
        angle = math.atan2(dy, dx)
        X = rr + r * math.cos(angle)
        Y = rr + r * math.sin(angle)
        pygame.draw.circle(WIN, RED, (X, Y), 4)

    for missile in yellow_missiles:
        dx = missile.centerx - global_state.cx
        dy = missile.centery - global_state.cy
        d = math.sqrt(dx ** 2 + dy ** 2)
        r = 1.2 * math.log((d ** 2) / (1000 + d) + 1) ** 2
        angle = math.atan2(dy, dx)
        X = rr + r * math.cos(angle)
        Y = rr + r * math.sin(angle)
        pygame.draw.circle(WIN, YELLOW, (X, Y), 1)

    for missile in red_missiles:
        dx = missile.centerx - global_state.cx
        dy = missile.centery - global_state.cy
        d = math.sqrt(dx ** 2 + dy ** 2)
        r = 1.2 * math.log((d ** 2) / (1000 + d) + 1) ** 2
        angle = math.atan2(dy, dx)
        X = rr + r * math.cos(angle)
        Y = rr + r * math.sin(angle)
        pygame.draw.circle(WIN, RED, (X, Y), 1)

    pygame.display.update()  # update window

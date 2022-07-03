import pygame


def draw_window(red_ships, yellow_ships, red_bullets, yellow_bullets, red_missiles, yellow_missiles, WIN, SPACE, FONT, WIDTH, R_SHIP_IMAGE, Y_SHIP_IMAGE, MISSILE_IMAGE, spaceship_height, spaceship_width, explosion_group):

    COLOR = (40, 10, 35)  # define window color
    BLACK = (0, 50, 0)  # BLACK
    RED = (255, 0, 0)  # RED
    YELLOW = (255, 255, 0)  # YELLOW
    GREEN = (0, 255, 0)
    BLUE = (75, 75, 255)
    WIN.blit(SPACE, (0, 0))

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
            WIN.blit(Y_SHIP, (yellow.cx, yellow.cy))
            pygame.draw.line(WIN, GREEN, (yellow.x, yellow.y), (yellow.x + 50 * yellow.health / yellow.Health, yellow.y) , 4)
            pygame.draw.line(WIN, BLUE, (yellow.x, yellow.y - 4), (yellow.x + 50 * yellow.energy / yellow.Energy, yellow.y - 4), 4)
            # pygame.draw.line(WIN, BLUE, (yellow.centerx, yellow.centery), (0, 0))


    for red in red_ships:
        R_SHIP = pygame.transform.rotate(pygame.transform.scale(R_SHIP_IMAGE, (spaceship_height, spaceship_width)), red.angle)
        if red.health > 0:
            # pygame.draw.circle(WIN, YELLOW, red.center, 26)
            # pygame.draw.rect(WIN, GREEN, red)
            WIN.blit(R_SHIP, (red.cx, red.cy))
            pygame.draw.line(WIN, GREEN, (red.x, red.y), (red.x + 50 * red.health / red.Health, red.y), 4)
            pygame.draw.line(WIN, YELLOW, (red.x, red.y - 4), (red.x + 50 * red.energy / red.Energy, red.y - 4), 4)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for missile in yellow_missiles:
        MISSILE = pygame.transform.rotate(pygame.transform.scale(MISSILE_IMAGE, (missile.height, missile.width)), missile.angle)
        WIN.blit(MISSILE, (missile.x, missile.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for missile in red_missiles:
        MISSILE = pygame.transform.rotate(pygame.transform.scale(MISSILE_IMAGE, (missile.height, missile.width)), missile.angle)
        WIN.blit(MISSILE, (missile.x, missile.y))

    explosion_group.draw(WIN)

    pygame.display.update()  # update window

"""https://github.com/techwithtim/PygameForBeginners"""

import pygame
import os
import numpy as np
import math
import random as rnd

from Draw_Window import draw_window
from Misc import ShipExplosion, GlobalState
from Weapon_Class import Bullet
from Ship_Class import Ship
from Control_Functions import NPControl, PlayerControl1

PCS = 'y'
nA = 1
nE = 2

# """ASK USER WHETHER TO SPAWN PLAYER CONTROLLED SHIP"""
# while PCS != 'y' and PCS != 'n':
#     PCS = input('Spawn Player Controlled Ship? (y/n)')
#
# """NUMBER OF ALLIES"""
# while nA is not int and (nA < 0 or nA > 5):
#     nA = int(input('Number of Allies:'))
#
# """NUMBER OF ENEMIES"""
# while nE is not int and (nE < 0 or nE > 5):
#     nE = int(input('Number of Enemies:'))

pygame.font.init()

WIDTH, HEIGHT = 1500, 800  # width and height of window

WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # create window
pygame.display.set_caption("The Expanse")  # set window title

FONT = pygame.font.SysFont('comicsans', 40)

COLOR = (40, 10, 35)  # define window color
BLACK = (0, 50, 0)  # BLACK
RED = (255, 0, 0)  # RED
YELLOW = (255, 255, 0)  # YELLOW

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space2.png')), (WIDTH, HEIGHT))
DUST = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space_dust_new.png')), (6000, 6000))
Y_SHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'yellow_ship.png'))  # yellow spaceship
R_SHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'red_ship.png'))  # red spaceship


FPS = 30  # define frame rate
VEL = 8  # ship velocity
ACC = .2  # ship acceleration

# YELLOW_HIT = pygame.USEREVENT + 1
# RED_HIT = pygame.USEREVENT + 2

AV = 2  # angular velocity

spaceship_height, spaceship_width = 50, 50
# Y_SHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'yellow_ship.png'))  # yellow spaceship
# R_SHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'red_ship.png'))  # red spaceship
# MISSILE_IMAGE = pygame.image.load(os.path.join('Assets', 'smallmissile1.png'))  # red spaceship

# music_file = os.path.join('Assets', 'music.mp3')  # path to music file

explosion_group = pygame.sprite.Group()

MyGS = GlobalState(0, 0, HEIGHT, WIDTH)


def main():

    yellow_ships = []
    red_ships = []

    red_bullets = []
    yellow_bullets = []

    yellow_missiles = []
    red_missiles = []

    """ASSIGN PLAYER CONTROL AND NPC CONTROL FUNCTIONS"""
    player_control = PlayerControl1
    npc_control = NPControl

    """SPAWN IN SPECIFIED SHIPS"""
    if PCS == 'y':
        yellow = Ship(player_control, rnd.randint(0, 100), rnd.randint(0, HEIGHT), 0, 'Fighter', 'HV', 'HE', True)
        yellow_ships.append(yellow)

    for i in range(nA):
        yellow = Ship(npc_control, rnd.randint(0, 100), rnd.randint(0, HEIGHT), rnd.randint(0, 359), 'Fighter', 'HV', 'HE')
        yellow_ships.append(yellow)

    for i in range(nE):
        red = Ship(npc_control, rnd.randint(10000, 10100), rnd.randint(0, HEIGHT), rnd.randint(0, 359), 'Fighter', 'HV', 'HE')
        red_ships.append(red)

    """Play Music"""
    # pygame.init()
    # pygame.mixer.init()
    # pygame.mixer.music.load(music_file)
    # pygame.mixer.music.play()
    # pygame.event.wait()

    run = True
    clock = pygame.time.Clock()  # game clock
    winner_text = ""

    while run:  # main loop
        clock.tick(FPS)

        # explosion_group.draw(WIN)
        explosion_group.update()

        for event in pygame.event.get():  # look for events
            if event.type == pygame.QUIT:  # check to see if user quit game
                run = False
                print('game over!')

        """Ship Movement"""
        for yellow in yellow_ships:
            if yellow.health > 0:
                yellow.scoot(yellow_bullets, yellow_missiles, red_ships, MyGS)
            else:
                yellow_ships.remove(yellow)

        for red in red_ships:
            if red.health > 0:
                red.scoot(red_bullets, red_missiles, yellow_ships, MyGS)
            else:
                red_ships.remove(red)

        """Bullet Movement"""
        for bullet in yellow_bullets:
            bullet.scoot(yellow_bullets, red_ships, explosion_group, MyGS)

        for bullet in red_bullets:
            bullet.scoot(red_bullets, yellow_ships, explosion_group, MyGS)

        for missile in yellow_missiles:
            missile.scoot(yellow_missiles, red_ships, explosion_group, MyGS)

        for missile in red_missiles:
            missile.scoot(red_missiles, yellow_ships, explosion_group, MyGS)

        """Render Window"""
        draw_window(red_ships, yellow_ships, red_bullets, yellow_bullets, red_missiles, yellow_missiles, WIN, SPACE, Y_SHIP_IMAGE, R_SHIP_IMAGE, DUST, FONT, spaceship_height, spaceship_width, explosion_group, MyGS)

    pygame.quit()  # quit game


if __name__ == "__main__":
    main()

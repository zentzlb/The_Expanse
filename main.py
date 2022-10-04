"""https://github.com/techwithtim/PygameForBeginners"""

import pygame
import os
import numpy as np
import math
import random as rnd
import time

from Draw_Window import draw_window
from Misc import ShipExplosion, GlobalState, MoveScreen
from Weapon_Class import Bullet
from Ship_Class import Ship, Station, Asteroid
from Control_Functions import NPControl, PlayerControl1

PCS = 'y'
nA = 1  # number of allied ships
nE = 1  # number of enemy ships
nR = 100  # number of asteroids

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
HUD = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # create HUD surface

pygame.display.set_caption("The Expanse")  # set window title

FONT1 = pygame.font.SysFont('Agency FB', 25)  # font type
FONT2 = pygame.font.SysFont('Agency FB', 20)  # font type

COLOR = (40, 10, 35)  # define window color
BLACK = (0, 50, 0)  # BLACK
RED = (255, 0, 0)  # RED
YELLOW = (255, 255, 0)  # YELLOW

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space2.png')), (WIDTH, HEIGHT)).convert(HUD)  # background image
DUST = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space_dust_new.png')), (6000, 6000)).convert(HUD)  # foreground image
FIELD = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'middle_ground.png')), (6000, 6000)).convert(HUD)  # middle ground image

FPS = 60  # define frame rate

# YELLOW_HIT = pygame.USEREVENT + 1
# RED_HIT = pygame.USEREVENT + 2

# music_file = os.path.join('Assets', 'music.mp3')  # path to music file
pygame.init()
pygame.mixer.init()

explosion_group = pygame.sprite.Group()  # initialize explosion group

MyGS = GlobalState(0, 0, HEIGHT, WIDTH, [FONT1, FONT2], [[], []], [[], []], [[], []], [[], []], [])  # global state object: used to keep track of global variables


def main():


    """ASSIGN PLAYER CONTROL AND NPC CONTROL FUNCTIONS"""
    player_control = PlayerControl1
    npc_control = NPControl

    """SPAWN IN SPECIFIED SHIPS"""
    if PCS == 'y':
        yellow = Ship(player_control, rnd.randint(0, 200), rnd.randint(0, 1000), 0, 'yellow', 'Frigate', 'PA', 'swarm missile', is_player=True)
        MyGS.ships[0].append(yellow)
        pygame.init()
        pygame.mixer.init()

    for i in range(nA):
        # yellow = Ship(npc_control, rnd.randint(0, 200), rnd.randint(0, 1000), rnd.randint(0, 359), 'yellow', 'Fighter', 'HV', 'HE')
        # yellow_ships.append(yellow)
        # yellow = Ship(npc_control, rnd.randint(-1000, -500), rnd.randint(0, 1000), rnd.randint(0, 359), 'yellow', 'Sprinter',
        #               'PA', 'torpedo')
        # yellow_ships.append(yellow)
        yellow = Station(rnd.randint(-2000, -200), rnd.randint(0, 1000), 'Partrid')
        yellow.image.convert(HUD)
        MyGS.stations[0].append(yellow)

    for i in range(nE):
        red = Ship(npc_control, rnd.randint(10000, 10200), rnd.randint(0, 1000), rnd.randint(0, 359), 'red', 'Fighter', 'HV', 'HE')
        MyGS.ships[1].append(red)
        # red = Ship(npc_control, rnd.randint(10000, 10200), rnd.randint(0, 1000), rnd.randint(0, 359), 'red', 'Sprinter',
        #            'PA', 'HE')
        # red_ships.append(red)

    for i in range(nR):
        roid = Asteroid(rnd.randint(0, 10000), rnd.randint(0, 10000), rnd.randint(0, 359), rnd.randint(0, 100), HUD)
        MyGS.asteroids.append(roid)

    """Play Music"""
    pygame.init()
    pygame.mixer.init()
    # pygame.mixer.music.load(music_file)
    # pygame.mixer.music.play()
    # pygame.event.wait()

    run = True
    clock = pygame.time.Clock()  # game clock
    winner_text = ""
    MyGS.update()

    while run:  # main loop
        clock.tick(FPS)
        fps = str(int(clock.get_fps()))
        explosion_group.update()  # update all explosions
        if PCS == 'n':
            MoveScreen(MyGS)

        for event in pygame.event.get():  # look for events
            if event.type == pygame.QUIT:  # check to see if user quit game
                run = False
                print('game over!')

        """Station Function"""
        for faction in range(len(MyGS.stations)):
            for station in MyGS.stations[faction]:
                station.scoot(MyGS, faction)  # update stations

        """Ship Movement"""
        for faction in range(len(MyGS.ships)):
            for ship in MyGS.ships[faction]:
                if ship.health > 0:
                    ship.scoot(MyGS, faction)  # move ships
                else:
                    MyGS.ships[faction].remove(ship)  # remove dead ships
                    MyGS.update()

        """Bullet Movement"""
        for faction in range(len(MyGS.bullets)):
            for bullet in MyGS.bullets[faction]:
                bullet.scoot(explosion_group, MyGS)  # move bullets

        for faction in range(len(MyGS.missiles)):
            for missile in MyGS.missiles[faction]:
                missile.scoot(explosion_group, MyGS)  # move missiles

        """Render Window"""
        # t1 = time.time()
        draw_window(WIN, HUD, SPACE, DUST, FIELD, explosion_group, MyGS, fps, HEIGHT, WIDTH)
        # t2 = time.time()
        # print(t2 - t1)

    pygame.quit()  # quit game


if __name__ == "__main__":
    main()

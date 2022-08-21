import pygame
from Misc import BulletTypes, MissileTypes, ShipTypes


class StationMenu:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = ['Launch', 'View Map', 'Primary Weapon', 'Secondary Weapon', 'Ships']
        self.selected = 0
        # self.launch_button = self.draw_button('Launch Ship', font, (255, 255, 0), hud, 100, 100)

    def draw_menu(self, hud, ally_list, red_ships, yellow_stations, gs):
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)

        if keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.option_list) - 1
        if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
            if self.selected == 0:
                gs.docked.docked_ships[0].refresh()
                ally_list.append(gs.docked.docked_ships[0])
                gs.docked.docked_ships.remove(gs.docked.docked_ships[0])
                gs.docked = None
                gs.menu = None
            elif self.selected == 1:
                gs.menu = MapMenu()
            elif self.selected == 2:
                gs.menu = WepMenu()
            elif self.selected == 3:
                gs.menu = WepMenu2()
            elif self.selected == 4:
                gs.menu = ShipMenu()


        self.keys_pressed = keys_pressed

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)

            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 * (i + 1))



    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


"""MAP MENU"""


class MapMenu:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = ['Back']
        self.selected = 0
        # self.launch_button = self.draw_button('Launch Ship', font, (255, 255, 0), hud, 100, 100)

    def draw_menu(self, hud, yellow_ships, red_ships, yellow_stations, gs):
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        edge2 = 150
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        mapRect = pygame.Rect(edge2, edge2, gs.width - edge2 * 2, gs.height - edge2 * 2)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (30, 70, 100, 255), mapRect)

        if keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.option_list) - 1
        if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
            if self.selected == 0:
                gs.menu = StationMenu()


        self.keys_pressed = keys_pressed

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 * (i + 1))
        # pygame.draw.circle(hud, (255, 0, 0), (500, 500), 4)

        for ship in yellow_ships:
            dx = ship.centerx - gs.cx
            dy = ship.centery - gs.cy
            X = dx // 100 + gs.width // 2
            Y = dy // 100 + gs.height // 2
            pygame.draw.circle(hud, (255, 255, 0), (X, Y), 4)

        for ship in red_ships:
            dx = ship.centerx - gs.cx
            dy = ship.centery - gs.cy
            X = dx // 100 + gs.width // 2
            Y = dy // 100 + gs.height // 2
            pygame.draw.circle(hud, (255, 0, 0), (X, Y), 4)

        for station in yellow_stations:
            dx = station.centerx - gs.cx
            dy = station.centery - gs.cy
            X = dx // 100 + gs.width // 2
            Y = dy // 100 + gs.height // 2
            radarRect = pygame.Rect(X - 5, Y - 5, 10, 10)
            pygame.draw.rect(hud, (255, 255, 0), radarRect)
        # pygame.draw.circle(WIN, YELLOW, (X, Y), 4)


    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


"""WEAPONS MENU"""


class WepMenu:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = ['HV', 'PA', 'railgun']
        self.desc_list = ['rapid fire bullet projectile', 'high damage plasma rounds', 'high velocity tungsten projectile']
        self.selected = 0
        # self.launch_button = self.draw_button('Launch Ship', font, (255, 255, 0), hud, 100, 100)

    def draw_menu(self, hud, yellow_ships, red_ships, yellow_stations, gs):
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        top_left = (300, 200)
        length = 100
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        outlineRect = pygame.Rect(top_left[0]-10, top_left[1]-10, length*10, gs.height-2*(top_left[1]-10))
        wepRect = pygame.Rect(top_left[0], top_left[1], length, length)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (50, 30, 30, 255), outlineRect)
        pygame.draw.rect(hud, (20, 20, 20, 255), wepRect)

        if keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.option_list) - 1
        if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
            gs.docked.docked_ships[0].bullet_type = BulletTypes(self.option_list[self.selected])
        if keys_pressed[pygame.K_ESCAPE] and not self.keys_pressed[pygame.K_ESCAPE]:
            gs.menu = StationMenu()


        self.keys_pressed = keys_pressed

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 * (i + 1))
        # pygame.draw.circle(hud, (255, 0, 0), (500, 500), 4)
        type = BulletTypes(self.option_list[self.selected])
        image = type.image  # pygame.transform.scale(type.image, (length - 20, length - 20))
        # imagex = top_left[0] + 10
        # imagey = top_left[1] + 10
        imagex = round(top_left[0] + length / 2 - type.width / 2)
        imagey = round(top_left[1] + length / 2 - type.height / 2)
        hud.blit(image, (imagex, imagey))

        bar_width = 20
        tranx = 75

        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 10),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 10), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 15 + bar_width), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 20 + 2 * bar_width), bar_width+4)

        pygame.draw.line(hud, (100, 0, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 10), (top_left[0] + length + 5 + 4 * type.damage + tranx, top_left[1] + 10), bar_width)
        pygame.draw.line(hud, (0, 100, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 5 + type.range // 50 + tranx, top_left[1] + 15 + bar_width), bar_width)
        pygame.draw.line(hud, (0, 0, 100), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 5 + 5000 // type.delay + tranx, top_left[1] + 20 + 2 * bar_width), bar_width)
        if True:  # keys_pressed[pygame.K_i]:
            damage_text = gs.fonts[1].render(f"DAMAGE", 1, (255, 255, 0))
            range_text = gs.fonts[1].render(f"RANGE", 1, (255, 255, 0))
            ROF_text = gs.fonts[1].render(f"RoF", 1, (255, 255, 0))
            hud.blit(damage_text, (top_left[0] + length + tranx - gs.fonts[1].size('DAMAGE')[0], top_left[1] - 1))
            hud.blit(range_text, (top_left[0] + length + tranx - gs.fonts[1].size('RANGE')[0], top_left[1] + 5 + bar_width - 1))
            hud.blit(ROF_text, (top_left[0] + length + tranx - gs.fonts[1].size('RoF')[0], top_left[1] + 2 * (5 + bar_width) - 1))

        # pygame.draw.circle(WIN, YELLOW, (X, Y), 4)


    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

class WepMenu2:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = ['HE', 'torpedo']
        self.desc_list = ['fast seeker missile', 'high damage EMP torpedo']
        self.selected = 0
        # self.launch_button = self.draw_button('Launch Ship', font, (255, 255, 0), hud, 100, 100)

    def draw_menu(self, hud, yellow_ships, red_ships, yellow_stations, gs):
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        top_left = (300, 200)
        length = 100
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        outlineRect = pygame.Rect(top_left[0]-10, top_left[1]-10, length*10, gs.height-2*(top_left[1]-10))
        wepRect = pygame.Rect(top_left[0], top_left[1], length, length)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (50, 30, 30, 255), outlineRect)
        pygame.draw.rect(hud, (20, 20, 20, 255), wepRect)

        if keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.option_list) - 1
        if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
            gs.docked.docked_ships[0].missile_type = MissileTypes(self.option_list[self.selected])
        if keys_pressed[pygame.K_ESCAPE] and not self.keys_pressed[pygame.K_ESCAPE]:
            gs.menu = StationMenu()


        self.keys_pressed = keys_pressed

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 * (i + 1))
        # pygame.draw.circle(hud, (255, 0, 0), (500, 500), 4)
        type = MissileTypes(self.option_list[self.selected])
        image = type.image  # pygame.transform.scale(type.image, (length - 20, length - 20))
        # imagex = top_left[0] + 10
        # imagey = top_left[1] + 10
        imagex = round(top_left[0] + length / 2 - type.width / 2)
        imagey = round(top_left[1] + length / 2 - type.height / 2)
        hud.blit(image, (imagex, imagey))

        bar_width = 20
        tranx = 75

        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 10),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 10), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 15 + bar_width), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 20 + 2 * bar_width), bar_width+4)

        pygame.draw.line(hud, (100, 50, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 10), (top_left[0] + length + 5 + 4 * (type.damage + type.explosion_damage) + tranx, top_left[1] + 10), bar_width)
        pygame.draw.line(hud, (100, 0, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 10), (top_left[0] + length + 5 + 4 * type.damage + tranx, top_left[1] + 10), bar_width)
        pygame.draw.line(hud, (0, 100, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 5 + type.range // 50 + tranx, top_left[1] + 15 + bar_width), bar_width)
        pygame.draw.line(hud, (0, 0, 100), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 5 + 5000 // type.delay + tranx, top_left[1] + 20 + 2 * bar_width), bar_width)
        if True:  # keys_pressed[pygame.K_i]:
            damage_text = gs.fonts[1].render(f"DAMAGE", 1, (255, 255, 0))
            range_text = gs.fonts[1].render(f"RANGE", 1, (255, 255, 0))
            ROF_text = gs.fonts[1].render(f"RoF", 1, (255, 255, 0))
            hud.blit(damage_text, (top_left[0] + length + tranx - gs.fonts[1].size('DAMAGE')[0], top_left[1] - 1))
            hud.blit(range_text, (top_left[0] + length + tranx - gs.fonts[1].size('RANGE')[0], top_left[1] + 5 + bar_width - 1))
            hud.blit(ROF_text, (top_left[0] + length + tranx - gs.fonts[1].size('RoF')[0], top_left[1] + 2 * (5 + bar_width) - 1))

        # pygame.draw.circle(WIN, YELLOW, (X, Y), 4)


    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


class ShipMenu:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = ['Sprinter', 'Fighter', 'Frigate']
        self.desc_list = ['fast', 'turn', 'big']
        self.selected = 0
        # self.launch_button = self.draw_button('Launch Ship', font, (255, 255, 0), hud, 100, 100)

    def draw_menu(self, hud, yellow_ships, red_ships, yellow_stations, gs):
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        top_left = (300, 200)
        length = 100
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        outlineRect = pygame.Rect(top_left[0]-10, top_left[1]-10, length*10, gs.height-2*(top_left[1]-10))
        wepRect = pygame.Rect(top_left[0], top_left[1], length, length)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (50, 30, 30, 255), outlineRect)
        pygame.draw.rect(hud, (20, 20, 20, 255), wepRect)

        if keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.option_list) - 1
        if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
            ShipType = ShipTypes(self.option_list[self.selected], 'yellow')
            gs.docked.docked_ships[0].ship_type = ShipType
            gs.docked.docked_ships[0].refresh()
        if keys_pressed[pygame.K_ESCAPE] and not self.keys_pressed[pygame.K_ESCAPE]:
            gs.menu = StationMenu()


        self.keys_pressed = keys_pressed

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 * (i + 1))
        # pygame.draw.circle(hud, (255, 0, 0), (500, 500), 4)
        Type = ShipTypes(self.option_list[self.selected], 'yellow')
        image = Type.image  # pygame.transform.scale(Type.image, (length - 20, length - 20))
        # imagex = top_left[0] + 10
        # imagey = top_left[1] + 10
        imagex = round(top_left[0] + length / 2 - Type.width / 2)
        imagey = round(top_left[1] + length / 2 - Type.height / 2)
        hud.blit(image, (imagex, imagey))

        bar_width = 20
        tranx = 75

        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 10),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 10), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 15 + bar_width), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 20 + 2 * bar_width), bar_width+4)

        pygame.draw.line(hud, (100, 0, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 10), (top_left[0] + length + 5 + Type.health // 3 + tranx, top_left[1] + 10), bar_width)
        pygame.draw.line(hud, (0, 100, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 5 + Type.av * 100 + tranx, top_left[1] + 15 + bar_width), bar_width)
        pygame.draw.line(hud, (0, 0, 100), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 5 + 30 * Type.velocity + tranx, top_left[1] + 20 + 2 * bar_width), bar_width)
        if True:  # keys_pressed[pygame.K_i]:
            damage_text = gs.fonts[1].render(f"HEALTH", 1, (255, 255, 0))
            range_text = gs.fonts[1].render(f"TURNING", 1, (255, 255, 0))
            ROF_text = gs.fonts[1].render(f"SPEED", 1, (255, 255, 0))
            hud.blit(damage_text, (top_left[0] + length + tranx - gs.fonts[1].size('HEALTH')[0], top_left[1] - 1))
            hud.blit(range_text, (top_left[0] + length + tranx - gs.fonts[1].size('TURNING')[0], top_left[1] + 5 + bar_width - 1))
            hud.blit(ROF_text, (top_left[0] + length + tranx - gs.fonts[1].size('SPEED')[0], top_left[1] + 2 * (5 + bar_width) - 1))

        # pygame.draw.circle(WIN, YELLOW, (X, Y), 4)


    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
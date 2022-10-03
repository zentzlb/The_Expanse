import pygame
from Misc import BulletTypes, MissileTypes, ShipTypes, check_purchase, purchase


class StationMenu:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = ['Launch', 'View Map', 'Primary Weapon', 'Secondary Weapon', 'Ships', 'Cargo Hold']
        self.selected = 0
        # self.launch_button = self.draw_button('Launch Ship', font, (255, 255, 0), hud, 100, 100)

    def draw_menu(self, hud, gs):
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
                gs.ships[0].append(gs.docked.docked_ships[0])
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
            elif self.selected == 5:
                gs.menu = CargoMenu()

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

    def draw_menu(self, hud, gs):
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
                gs.menu.selected = gs.menu.option_list.index('View Map')


        self.keys_pressed = keys_pressed

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 * (i + 1))
        # pygame.draw.circle(hud, (255, 0, 0), (500, 500), 4)

        for ship in gs.ships[0]:
            if ship.is_visible:  # only show enemy ships on station map if they're visible
                dx = ship.centerx - gs.cx
                dy = ship.centery - gs.cy
                X = dx // 100 + gs.width // 2
                Y = dy // 100 + gs.height // 2
                pygame.draw.circle(hud, (255, 255, 0), (X, Y), 4)

        for ship in gs.ships[1]:
            if ship.is_visible:  # only show enemy ships on station map if they're visible
                dx = ship.centerx - gs.cx
                dy = ship.centery - gs.cy
                X = dx // 100 + gs.width // 2
                Y = dy // 100 + gs.height // 2
                pygame.draw.circle(hud, (255, 0, 0), (X, Y), 4)

        for roid in gs.asteroids:
            dx = roid.centerx - gs.cx
            dy = roid.centery - gs.cy
            X = dx // 100 + gs.width // 2
            Y = dy // 100 + gs.height // 2
            pygame.draw.circle(hud, (255, 255, 255), (X, Y), 5)

        for station in gs.stations[0]:
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

    def draw_menu(self, hud,  gs):
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
            bullet = BulletTypes(self.option_list[self.selected])
            if gs.docked.docked_ships[0].bullet_type.name == bullet.name:
                gs.menu = PopupMenu(self, "You already have that type of bullet equipped.")
            elif check_purchase(gs.docked, bullet):
                purchase(gs.docked, bullet)
                gs.docked.docked_ships[0].bullet_type = bullet
            else:
                gs.menu = PopupMenu(self, "You don't have enough ore to purchase this item.")
        if keys_pressed[pygame.K_ESCAPE] and not self.keys_pressed[pygame.K_ESCAPE]:
            gs.menu = StationMenu()
            gs.menu.selected = gs.menu.option_list.index('Primary Weapon')


        self.keys_pressed = keys_pressed
        # self.draw_button("Ship Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 800, top_left[1])
        # cargos = list(gs.docked.docked_ships[0].cargo)
        # for i in range(len(gs.docked.docked_ships[0].cargo)):
        #     color = (255, 255, 255)
        #     self.draw_button(cargos[i], gs.fonts[0], color, hud, top_left[0] + 800, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.docked_ships[0].cargo) + 1))))
        #     self.draw_button(str(gs.docked.docked_ships[0].cargo[cargos[i]]), gs.fonts[0], color, hud, top_left[0] + 900, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.docked_ships[0].cargo) + 1))))
        self.draw_button("Station Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 500, top_left[1])
        station_cargo = list(gs.docked.cargo)
        for i in range(len(gs.docked.cargo)):
            color = (255, 255, 255)
            self.draw_button(station_cargo[i], gs.fonts[0], color, hud, top_left[0] + 500, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))
            self.draw_button(str(gs.docked.cargo[station_cargo[i]]), gs.fonts[0], color, hud, top_left[0] + 600, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))

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

        self.draw_button("Cost:", gs.fonts[0], (255, 255, 255), hud, top_left[0], top_left[1] + 150)
        ore_names = list(type.cost)
        for i in range(len(type.cost)):
            color = (255, 255, 255)
            self.draw_button(ore_names[i], gs.fonts[0], color, hud, top_left[0],
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(type.cost) + 1)))))
            self.draw_button(str(type.cost[station_cargo[i]]), gs.fonts[0], color, hud, top_left[0] + 100,
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(type.cost) + 1)))))

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

    def draw_menu(self, hud, gs):
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
            missile = MissileTypes(self.option_list[self.selected])
            if gs.docked.docked_ships[0].missile_type.name == missile.name:
                gs.menu = PopupMenu(self, "You already have that type of missile equipped.")
            elif check_purchase(gs.docked, missile):
                purchase(gs.docked, missile)
                gs.docked.docked_ships[0].missile_type = missile
            else:
                gs.menu = PopupMenu(self, "You don't have enough ore to purchase this item.")
        if keys_pressed[pygame.K_ESCAPE] and not self.keys_pressed[pygame.K_ESCAPE]:
            gs.menu = StationMenu()
            gs.menu.selected = gs.menu.option_list.index('Secondary Weapon')


        self.keys_pressed = keys_pressed
        # self.draw_button("Ship Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 800, top_left[1])
        # cargos = list(gs.docked.docked_ships[0].cargo)
        # for i in range(len(gs.docked.docked_ships[0].cargo)):
        #     color = (255, 255, 255)
        #     self.draw_button(cargos[i], gs.fonts[0], color, hud, top_left[0] + 800, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.docked_ships[0].cargo) + 1))))
        #     self.draw_button(str(gs.docked.docked_ships[0].cargo[cargos[i]]), gs.fonts[0], color, hud, top_left[0] + 900, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.docked_ships[0].cargo) + 1))))
        self.draw_button("Station Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 500, top_left[1])
        station_cargo = list(gs.docked.cargo)
        for i in range(len(gs.docked.cargo)):
            color = (255, 255, 255)
            self.draw_button(station_cargo[i], gs.fonts[0], color, hud, top_left[0] + 500, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))
            self.draw_button(str(gs.docked.cargo[station_cargo[i]]), gs.fonts[0], color, hud, top_left[0] + 600, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))

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

        self.draw_button("Cost:", gs.fonts[0], (255, 255, 255), hud, top_left[0], top_left[1] + 150)
        ore_names = list(type.cost)
        for i in range(len(type.cost)):
            color = (255, 255, 255)
            self.draw_button(ore_names[i], gs.fonts[0], color, hud, top_left[0],
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(type.cost) + 1)))))
            self.draw_button(str(type.cost[station_cargo[i]]), gs.fonts[0], color, hud, top_left[0] + 100,
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(type.cost) + 1)))))

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

    def draw_menu(self, hud, gs):
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
            ship = ShipTypes(self.option_list[self.selected], 'yellow')
            if gs.docked.docked_ships[0].ship_type.name == ship.name:
                gs.menu = PopupMenu(self, "You already have that type of ship equipped.")
            elif check_purchase(gs.docked, ship):
                purchase(gs.docked, ship)
                gs.docked.docked_ships[0].ship_type = ship
                gs.docked.docked_ships[0].refresh()
            else:
                gs.menu = PopupMenu(self, "You don't have enough ore to purchase this item.")
        if keys_pressed[pygame.K_ESCAPE] and not self.keys_pressed[pygame.K_ESCAPE]:
            gs.menu = StationMenu()
            gs.menu.selected = gs.menu.option_list.index('Ships')


        self.keys_pressed = keys_pressed
        # self.draw_button("Ship Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 800, top_left[1])
        # cargos = list(gs.docked.docked_ships[0].cargo)
        # for i in range(len(gs.docked.docked_ships[0].cargo)):
        #     color = (255, 255, 255)
        #     self.draw_button(cargos[i], gs.fonts[0], color, hud, top_left[0] + 800, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.docked_ships[0].cargo) + 1))))
        #     self.draw_button(str(gs.docked.docked_ships[0].cargo[cargos[i]]), gs.fonts[0], color, hud, top_left[0] + 900, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.docked_ships[0].cargo) + 1))))
        self.draw_button("Station Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 500, top_left[1])
        station_cargo = list(gs.docked.cargo)
        for i in range(len(gs.docked.cargo)):
            color = (255, 255, 255)
            self.draw_button(station_cargo[i], gs.fonts[0], color, hud, top_left[0] + 500, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))
            self.draw_button(str(gs.docked.cargo[station_cargo[i]]), gs.fonts[0], color, hud, top_left[0] + 600, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))

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

        self.draw_button("Cost:", gs.fonts[0], (255, 255, 255), hud, top_left[0], top_left[1] + 150)
        ore_names = list(Type.cost)
        for i in range(len(Type.cost)):
            color = (255, 255, 255)
            self.draw_button(ore_names[i], gs.fonts[0], color, hud, top_left[0],
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(Type.cost) + 1)))))
            self.draw_button(str(Type.cost[station_cargo[i]]), gs.fonts[0], color, hud, top_left[0] + 100,
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(Type.cost) + 1)))))

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


class CargoMenu:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = ['Back', 'Unload Cargo']
        self.selected = 0

    def draw_menu(self, hud, gs):
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        top_left = (300, 200)
        length = 100
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        outlineRect = pygame.Rect(top_left[0]-10, top_left[1]-10, length*10, gs.height-2*(top_left[1]-10))
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (50, 30, 30, 255), outlineRect)

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
                gs.menu.selected = gs.menu.option_list.index('Cargo Hold')
            elif self.selected == 1:
                if gs.docked.docked_ships[0].cargo_total == 0:
                    gs.menu = PopupMenu(self, "Error: You can't unload 0 cargo.")
                for i in range(len(gs.docked.docked_ships[0].cargo)):
                    ores = list(gs.docked.docked_ships[0].cargo)
                    gs.docked.cargo[ores[i]] += gs.docked.docked_ships[0].cargo[ores[i]]
                    gs.docked.docked_ships[0].cargo_total -= gs.docked.docked_ships[0].cargo[ores[i]]
                    gs.docked.docked_ships[0].cargo[ores[i]] = 0

        self.keys_pressed = keys_pressed
        self.draw_button("Ship Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0], top_left[1])
        cargos = list(gs.docked.docked_ships[0].cargo)
        for i in range(len(gs.docked.docked_ships[0].cargo)):
            color = (255, 255, 255)
            self.draw_button(cargos[i], gs.fonts[0], color, hud, top_left[0], top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.docked_ships[0].cargo) + 1))))
            self.draw_button(str(gs.docked.docked_ships[0].cargo[cargos[i]]), gs.fonts[0], color, hud, top_left[0] + 100, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.docked_ships[0].cargo) + 1))))
        self.draw_button("Station Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 400, top_left[1])
        station_cargo = list(gs.docked.cargo)
        for i in range(len(gs.docked.cargo)):
            color = (255, 255, 255)
            self.draw_button(station_cargo[i], gs.fonts[0], color, hud, top_left[0] + 400, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))
            self.draw_button(str(gs.docked.cargo[station_cargo[i]]), gs.fonts[0], color, hud, top_left[0] + 500, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))

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


"""ASTEROID MENU"""


class AsteroidMenu:

    def __init__(self, ship, asteroid):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = ['Launch', 'Harvest']  # can add options later (Build Station, Build Turret, etc)
        self.selected = 0
        self.ship = ship
        self.asteroid = asteroid

    def draw_menu(self, hud, gs):
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        menuRect = pygame.Rect(edge, edge, gs.width - edge * 2, gs.height - edge * 2)
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
                gs.ships[0].append(self.ship)
                gs.menu = None
            elif self.selected == 1:
                gs.menu = AsteroidMenu2(self.ship, self.asteroid)

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


class AsteroidMenu2:

    def __init__(self, ship, asteroid):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = ['Back']
        self.selected = 0
        self.ship = ship
        self.asteroid = asteroid
        for i in range(len(asteroid.ore)):
            self.option_list.append('Harvest All/Max')
            self.option_list.append('Harvest 10')

    def draw_menu(self, hud, gs):
        keys_pressed = pygame.key.get_pressed()
        ores = list(self.asteroid.ore)
        cargos = list(self.ship.cargo)
        edge = 50
        top_left = (300, 100)
        length = 100
        menuRect = pygame.Rect(edge, edge, gs.width - edge * 2, gs.height - edge * 2)
        outlineRect = pygame.Rect(top_left[0] - 10, top_left[1] + (menuRect.height - 100) / len(self.option_list), length * 2, (len(self.option_list) - 2) * (menuRect.height - 100) / len(self.option_list) + 25)
        playerRect = pygame.Rect(top_left[0] + 350, top_left[1] + (menuRect.height - 100) / len(self.option_list), length * 2, (len(self.option_list) - 2) * (menuRect.height - 100) / len(self.option_list) + 25)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (50, 30, 30, 225), outlineRect)
        pygame.draw.rect(hud, (50, 30, 30, 225), playerRect)

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
                gs.menu = AsteroidMenu(self.ship, self.asteroid)
            elif self.selected >= 0:
                if self.selected % 2 != 0:  # odd number = Harvest All/Max for some ore
                    ores_index = self.selected // 2
                    if self.asteroid.ore[ores[ores_index]] == 0:
                        gs.menu = PopupMenu(self, "Error: You can't harvest 0 ore.")
                    elif (self.ship.cargo_total + self.asteroid.ore[ores[ores_index]]) < self.ship.ship_type.cargo_cap:
                        added_cargo = self.asteroid.harvest_all(ores[ores_index])
                        self.ship.cargo_total += added_cargo
                        self.ship.cargo[ores[ores_index]] += added_cargo
                    elif self.ship.cargo_total < self.ship.ship_type.cargo_cap:
                        added_cargo = self.ship.ship_type.cargo_cap - self.ship.cargo_total
                        self.asteroid.harvest(ores[ores_index], added_cargo)
                        self.ship.cargo_total += added_cargo
                        self.ship.cargo[ores[ores_index]] += added_cargo
                    else:
                        gs.menu = PopupMenu(self, "Error: Harvest All/Max failed. Cargo full.")
                if self.selected % 2 == 0:  # even number = Harvest 10 for some ore
                    ores_index = int(self.selected / 2 - 1)
                    if self.asteroid.ore[ores[ores_index]] < 10:
                        gs.menu = PopupMenu(self, "Error: You can't harvest 10 of this ore.")
                    elif (self.ship.cargo_total + 10) <= self.ship.ship_type.cargo_cap:
                        self.ship.cargo_total += 10
                        self.ship.cargo[ores[ores_index]] += self.asteroid.harvest(ores[ores_index], 10)
                    else:
                        gs.menu = PopupMenu(self, "Error: Harvest 10 failed. Cargo full.")

        self.keys_pressed = keys_pressed
        self.draw_button("Ship Cargo: ", gs.fonts[0], (255, 255, 255), hud, 650, 100)

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 + (((menuRect.height - 100) * i) / len(self.option_list)))
        for i in range(len(self.asteroid.ore)):
            color = (255, 255, 255)
            self.draw_button(ores[i], gs.fonts[0], color, hud, top_left[0], 100 + (1.5 * (menuRect.height - 100) / len(self.option_list)) + ((2 * (menuRect.height - 100) * i) / len(self.option_list)))
            self.draw_button(str(self.asteroid.ore[ores[i]]), gs.fonts[0], color, hud, top_left[0] + 100, 100 + (1.5 * (menuRect.height - 100) / len(self.option_list)) + ((2 * (menuRect.height - 100) * i) / len(self.option_list)))
        for i in range(len(self.ship.cargo)):
            color = (255, 255, 255)
            self.draw_button(cargos[i], gs.fonts[0], color, hud, top_left[0] + 360, 100 + (1.5 * (menuRect.height - 100) / len(self.option_list)) + ((2 * (menuRect.height - 100) * i) / len(self.option_list)))
            self.draw_button(str(self.ship.cargo[cargos[i]]), gs.fonts[0], color, hud, top_left[0] + 460, 100 + (1.5 * (menuRect.height - 100) / len(self.option_list)) + ((2 * (menuRect.height - 100) * i) / len(self.option_list)))

    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


class PopupMenu:

    def __init__(self, menu, text):
        self.keys_pressed = pygame.key.get_pressed()
        self.menu = menu
        self.text = text

    def draw_menu(self, hud, gs):
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        color = (255, 255, 255)
        menuRect = pygame.Rect(edge, edge, gs.width - edge * 2, gs.height - edge * 2)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)

        if keys_pressed[pygame.K_p] and not self.keys_pressed[pygame.K_p]:
            gs.menu = self.menu

        self.keys_pressed = keys_pressed

        self.draw_button(self.text, gs.fonts[0], color, hud, 550, 350)
        self.draw_button("Press p to return to previous menu.", gs.fonts[0], color, hud, 550, 400)

    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

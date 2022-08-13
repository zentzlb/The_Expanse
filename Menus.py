import pygame


class StationMenu():

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = ['Launch', 'View Map']
        self.selected = 0
        # self.launch_button = self.draw_button('Launch Ship', font, (255, 255, 0), hud, 100, 100)

    def draw_menu(self, font, hud, ally_list, red_ships, yellow_stations, gs):
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)

        if keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.option_list) - 1
        if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
            if self.selected == 0:
                ally_list.append(gs.docked.docked_ships[0])
                gs.docked.docked_ships.remove(gs.docked.docked_ships[0])
                gs.docked = None
                gs.menu = None
            elif self.selected == 1:
                gs.menu = MapMenu()


        self.keys_pressed = keys_pressed

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)

            self.draw_button(self.option_list[i], font, color, hud, 100, 100 * (i + 1))



    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


"""MAP MENU"""

class MapMenu():

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = ['Back']
        self.selected = 0
        # self.launch_button = self.draw_button('Launch Ship', font, (255, 255, 0), hud, 100, 100)

    def draw_menu(self, font, hud, yellow_ships, red_ships, yellow_stations, gs):
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        edge2 = 150
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        mapRect = pygame.Rect(edge2, edge2, gs.width - edge2 * 2, gs.height - edge2 * 2)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (30, 50, 100, 255), mapRect)

        if keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
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
            self.draw_button(self.option_list[i], font, color, hud, 100, 100 * (i + 1))
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

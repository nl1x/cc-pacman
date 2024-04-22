from dont_touch_me.texture import Texture

import dont_touch_me.constants as const
import pygame


def load_surface(texture, x, y, width, height) -> pygame.Surface:
    surface = pygame.Surface([width, height])
    surface.blit(texture, (0, 0), (x * const.TILE_MAP_SIZE[0], y * const.TILE_MAP_SIZE[1], width, height))
    return surface


tile_sheet = pygame.image.load("assets/map_sheet.png")

colliders_code = [92, 44, 140]
tiles = {
    "A": load_surface(tile_sheet, 2, 5, *const.TILE_MAP_SIZE),
    "B": load_surface(tile_sheet, 3, 5, *const.TILE_MAP_SIZE),
    "C": load_surface(tile_sheet, 4, 5, *const.TILE_MAP_SIZE),
    "D": load_surface(tile_sheet, 5, 5, *const.TILE_MAP_SIZE),
    "F": load_surface(tile_sheet, 6, 5, *const.TILE_MAP_SIZE),
    "E": load_surface(tile_sheet, 7, 5, *const.TILE_MAP_SIZE),
    "I": load_surface(tile_sheet, 8, 5, *const.TILE_MAP_SIZE),
    "H": load_surface(tile_sheet, 9, 5, *const.TILE_MAP_SIZE),
    "L": load_surface(tile_sheet, 4, 4, *const.TILE_MAP_SIZE),
    "G": load_surface(tile_sheet, 15, 3, *const.TILE_MAP_SIZE),
    "P": load_surface(tile_sheet, 8, 4, *const.TILE_MAP_SIZE),
    "R": load_surface(tile_sheet, 9, 4, *const.TILE_MAP_SIZE),
    ".": load_surface(tile_sheet, 13, 5, *const.TILE_MAP_SIZE),
    "*": load_surface(tile_sheet, 14, 5, *const.TILE_MAP_SIZE),
    "/": load_surface(tile_sheet, 12, 5, *const.TILE_MAP_SIZE),
    " ": load_surface(tile_sheet, 12, 5, *const.TILE_MAP_SIZE)
}


class Tile(pygame.sprite.Sprite):

    def __init__(self,
                 code: str,
                 x: int, y: int,
                 image: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.code = code
        self.color = None
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def eat_coin(self, map_image: pygame.Surface):
        self.image.fill((0, 0, 0))
        map_image.blit(self.image, (self.x, self.y))
        if self.code == '*':
            self.code = ' '
            return 10
        elif self.code == '.':
            self.code = ' '
            return 1
        else:
            return 0

    def is_coin(self):
        return self.code == '*' or self.code == '.'

    def is_wall(self):
        return self.code in ('A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'G', 'L', 'P', 'R')

    def is_enemy_spawn(self):
        return self.code == '/'

from dont_touch_me.texture import Texture

import pygame

colliders_code = [92, 44, 140]


class Tile(pygame.sprite.Sprite):

    def __init__(self,
                 code: str,
                 x: int, y: int,
                 tile_width: int,
                 tile_height: int):
        pygame.sprite.Sprite.__init__(self)
        self.code = code
        self.color = None
        self.x = x
        self.y = y
        self.image = pygame.Surface([tile_width, tile_height])
        self.is_collider = False
        if self.code == "W":
            self.image.fill((0, 20, 108))
            self.is_collider = True
        elif self.code == ".":
            self.image.fill((0, 0, 0))
            pygame.draw.circle(self.image, (192, 195, 0), (tile_width // 2, tile_height // 2), tile_width // 5)
            self.is_collider = True
        elif self.code == "*":
            self.image.fill((0, 0, 0))
            pygame.draw.circle(self.image, (192, 195, 0), (tile_width // 2, tile_height // 2), tile_width // 3)
            self.is_collider = True
        else:
            self.image.fill((0, 0, 0))
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
        return self.code == 'W'

    def is_enemy_spawn(self):
        return self.code == '/'

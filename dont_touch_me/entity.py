from dont_touch_me.texture import Texture
from random import randint

import dont_touch_me.constants as const
import dont_touch_me.tile as tile
import pygame
import sys


def load_sprite_texture(texture: Texture, texture_index: int) -> pygame.surface.Surface:
    surface = pygame.Surface(const.SPRITE_SIZE)
    surface.blit(texture.get_image(), (0, 0),
                 ((texture_index % const.SPRITE_COLS) * const.SPRITE_SIZE[0],
                  (texture_index // const.SPRITE_COLS) * const.SPRITE_SIZE[1],
                  const.SPRITE_SIZE[0],
                  const.SPRITE_SIZE[1]))
    return surface


class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y, speed=50):
        pygame.sprite.Sprite.__init__(self)
        self.RIGHT_ANIMATION_FRAME = None
        self.LEFT_ANIMATION_FRAME = None
        self.UP_ANIMATION_FRAME = None
        self.DOWN_ANIMATION_FRAME = None
        self.x = x
        self.y = y
        self.speed = speed
        self.previous_direction = "right"
        self.direction = "right"
        self.animation_frames = []  # Liste des images d'animation
        self.current_frame_index = 0
        self.animation_speed = 0.1
        self.animation_timer = 0.0
        self.rect = pygame.rect.Rect(self.x, self.y, const.SPRITE_SIZE[0], const.SPRITE_SIZE[1])

    def set_right_animation_frame(self, frame):
        self.RIGHT_ANIMATION_FRAME = frame

    def set_left_animation_frame(self, frame):
        self.LEFT_ANIMATION_FRAME = frame

    def set_down_animation_frame(self, frame):
        self.DOWN_ANIMATION_FRAME = frame

    def set_up_animation_frame(self, frame):
        self.UP_ANIMATION_FRAME = frame

    def move_right(self):
        self.set_direction("right")

    def move_left(self):
        self.set_direction("left")

    def move_up(self):
        self.set_direction("up")

    def move_down(self):
        self.set_direction("down")

    def move(self, dt, colliders):
        if self.direction == 'up':
            self.y -= self.speed * dt
        elif self.direction == 'down':
            self.y += self.speed * dt
        elif self.direction == 'left':
            self.x -= self.speed * dt
        elif self.direction == 'right':
            self.x += self.speed * dt
        self.rect.x = self.x
        self.rect.y = self.y
        collider = pygame.sprite.spritecollideany(self, pygame.sprite.Group(colliders))
        if collider is not None:
            self.cancel_move(dt)
            return False
        return True

    def cancel_move(self, dt):
        if self.direction == 'up':
            self.y += self.speed * dt
        elif self.direction == 'down':
            self.y -= self.speed * dt
        elif self.direction == 'left':
            self.x += self.speed * dt
        elif self.direction == 'right':
            self.x -= self.speed * dt
        self.rect.x = self.x
        self.rect.y = self.y

    def animate_texture(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames)
            self.animation_timer = 0.0

    def set_direction(self, direction):
        if self.direction != direction:
            self.previous_direction = self.direction
            self.direction = direction

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

    def set_speed(self, speed):
        self.speed = speed

    def set_animation_frames(self, frames):
        self.animation_frames = frames

    def update_texture(self):
        if self.direction == 'right':
            self.animation_frames[0] = self.RIGHT_ANIMATION_FRAME
        elif self.direction == 'left':
            self.animation_frames[0] = self.LEFT_ANIMATION_FRAME
        elif self.direction == 'down':
            self.animation_frames[0] = self.DOWN_ANIMATION_FRAME
        elif self.direction == 'up':
            self.animation_frames[0] = self.UP_ANIMATION_FRAME

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.animation_frames[self.current_frame_index], (self.x, self.y))

    def get_tile_pos(self) -> tuple[int, int]:
        return self.x // const.SPRITE_SIZE[0], self.y // const.SPRITE_SIZE[1]


class Enemy(Entity):

    def __init__(self, spawn: tile.Tile):
        Entity.__init__(self, spawn.x, spawn.y)
        self.RIGHT_ANIMATION_FRAME = None
        self.LEFT_ANIMATION_FRAME = None
        self.UP_ANIMATION_FRAME = None
        self.DOWN_ANIMATION_FRAME = None
        self.load_textures()

    def load_textures(self):
        texture_sheet = Texture("assets/sprites.png")
        self.set_right_animation_frame(load_sprite_texture(texture_sheet, 56))
        self.set_left_animation_frame(load_sprite_texture(texture_sheet, 58))
        self.set_up_animation_frame(load_sprite_texture(texture_sheet, 60))
        self.set_down_animation_frame(load_sprite_texture(texture_sheet, 62))
        self.set_animation_frames([self.RIGHT_ANIMATION_FRAME])
        self.move_right()

    def update(self,
               dt, window,
               colliders: list[tile.Tile]):
        while not self.move(dt, colliders):
            self.direction = ["right", "left", "up", "down"][randint(0, 3)]
        self.animate_texture(dt)
        self.draw(window)


class Player(Entity):

    def __init__(self):
        Entity.__init__(self, 16, 16)
        self.score = 0
        self.load_textures()

    def load_textures(self):
        texture_sheet = Texture("assets/sprites.png")
        self.set_right_animation_frame(load_sprite_texture(texture_sheet, 1))
        self.set_left_animation_frame(load_sprite_texture(texture_sheet, 15))
        self.set_up_animation_frame(load_sprite_texture(texture_sheet, 29))
        self.set_down_animation_frame(load_sprite_texture(texture_sheet, 43))
        self.set_animation_frames([None, load_sprite_texture(texture_sheet, 2)])
        self.move_right()

    def update(self,
               dt, window, map_image,
               colliders: list[tile.Tile],
               coins: list[tile.Tile],
               enemies: list[Enemy]):
        if not self.move(dt, colliders):
            direction = self.direction
            self.direction = self.previous_direction
            self.move(dt, colliders)
            self.direction = direction
        else:
            self.update_texture()

        coin: tile.Tile = pygame.sprite.spritecollideany(self, coins)
        if coin is not None:
            coins.remove(coin)
            self.score += coin.eat_coin(map_image)

        enemy = pygame.sprite.spritecollideany(self, enemies)
        if enemy is not None:
            pygame.quit()
            sys.exit()

        self.animate_texture(dt)
        self.draw(window)

    def get_score(self):
        return self.score

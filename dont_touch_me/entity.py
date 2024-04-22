from dont_touch_me.texture import Texture

import dont_touch_me.constants as const
import pygame


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
        self.previous_direction = pygame.K_RIGHT
        self.direction = pygame.K_RIGHT
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
        self.set_direction(pygame.K_RIGHT)

    def move_left(self):
        self.set_direction(pygame.K_LEFT)

    def move_up(self):
        self.set_direction(pygame.K_UP)

    def move_down(self):
        self.set_direction(pygame.K_DOWN)

    def move(self, dt, colliders, window: pygame.Surface):
        if self.direction == pygame.K_UP:
            self.y -= self.speed * dt
        elif self.direction == pygame.K_DOWN:
            self.y += self.speed * dt
        elif self.direction == pygame.K_LEFT:
            self.x -= self.speed * dt
        elif self.direction == pygame.K_RIGHT:
            self.x += self.speed * dt
        self.rect.x = self.x
        self.rect.y = self.y
        collider = pygame.sprite.spritecollideany(self, pygame.sprite.Group(colliders))
        if collider is not None:
            self.cancel_move(dt)
            return False
        if self.rect.x > window.get_width():
            self.set_position(0, self.rect.y)
        if self.rect.y > window.get_height():
            self.set_position(self.rect.x, 0)
        if self.rect.left < 0:
            self.set_position(window.get_width(), self.rect.y)
        if self.rect.top < 0:
            self.set_position(self.rect.x, window.get_height())
        return True

    def cancel_move(self, dt):
        if self.direction == pygame.K_UP:
            self.y += self.speed * dt
        elif self.direction == pygame.K_DOWN:
            self.y -= self.speed * dt
        elif self.direction == pygame.K_LEFT:
            self.x += self.speed * dt
        elif self.direction == pygame.K_RIGHT:
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
        if self.direction == pygame.K_RIGHT:
            self.animation_frames[0] = self.RIGHT_ANIMATION_FRAME
        elif self.direction == pygame.K_LEFT:
            self.animation_frames[0] = self.LEFT_ANIMATION_FRAME
        elif self.direction == pygame.K_DOWN:
            self.animation_frames[0] = self.DOWN_ANIMATION_FRAME
        elif self.direction == pygame.K_UP:
            self.animation_frames[0] = self.UP_ANIMATION_FRAME

    def draw(self, surface: pygame.surface.Surface):
        surface.blit(self.animation_frames[self.current_frame_index], (self.x, self.y))

    def get_tile_pos(self) -> tuple[int, int]:
        return self.x // const.SPRITE_SIZE[0], self.y // const.SPRITE_SIZE[1]
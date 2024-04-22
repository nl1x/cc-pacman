from dont_touch_me import loader, entity, texture, tile
from random import randint

import pygame
import sys


# --- Ennemie ---
class Enemy(entity.Entity):

    def __init__(self, spawn: tile.Tile):
        entity.Entity.__init__(self, spawn.x, spawn.y)
        self.RIGHT_ANIMATION_FRAME = None
        self.LEFT_ANIMATION_FRAME = None
        self.UP_ANIMATION_FRAME = None
        self.DOWN_ANIMATION_FRAME = None
        self.movement_timer = 0.0
        self.next_movement_time = 7
        self.load_textures()
        self.set_direction([pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT][randint(0, 3)])

    def load_textures(self):
        texture_sheet = texture.Texture("assets/sprites.png")
        self.set_right_animation_frame(entity.load_sprite_texture(texture_sheet, 56))
        self.set_left_animation_frame(entity.load_sprite_texture(texture_sheet, 58))
        self.set_up_animation_frame(entity.load_sprite_texture(texture_sheet, 60))
        self.set_down_animation_frame(entity.load_sprite_texture(texture_sheet, 62))
        self.set_animation_frames([self.RIGHT_ANIMATION_FRAME])

    def update(self,
               dt, window,
               colliders: list[tile.Tile]):
        self.movement_timer += dt
        if self.movement_timer > self.next_movement_time:
            self.movement_timer = 0.0
            self.set_direction([pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT][randint(0, 3)])
        while not self.move(dt, colliders, window):
            self.set_direction([pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT][randint(0, 3)])
        self.animate_texture(dt)
        self.draw(window)


# --- Joueur ---
class Player(entity.Entity):

    def __init__(self):
        entity.Entity.__init__(self, 16, 16)
        self.score = 0
        self.next_objective = 20
        self.load_textures()

    def load_textures(self):
        texture_sheet = texture.Texture("assets/sprites.png")
        self.set_right_animation_frame(entity.load_sprite_texture(texture_sheet, 1))
        self.set_left_animation_frame(entity.load_sprite_texture(texture_sheet, 15))
        self.set_up_animation_frame(entity.load_sprite_texture(texture_sheet, 29))
        self.set_down_animation_frame(entity.load_sprite_texture(texture_sheet, 43))
        self.set_animation_frames([None, entity.load_sprite_texture(texture_sheet, 2)])
        self.move_right()

    def update(self,
               dt, window, map_image,
               colliders: list[tile.Tile],
               coins: list[tile.Tile],
               enemies: list[Enemy],
               enemies_spawns):
        if not self.move(dt, colliders, window):
            direction = self.direction
            self.direction = self.previous_direction
            self.move(dt, colliders, window)
            self.direction = direction
        else:
            self.update_texture()

        coin = pygame.sprite.spritecollideany(self, coins)
        if coin is not None:
            coins.remove(coin)
            self.score += coin.eat_coin(map_image)
            if self.score >= self.next_objective:
                self.next_objective += 20
                spawn = enemies_spawns[randint(0, len(enemies_spawns) - 1)]
                enemies.append(Enemy(spawn))

        enemy = pygame.sprite.spritecollideany(self, enemies)
        if enemy is not None or len(coins) == 0:
            pygame.quit()
            sys.exit()

        self.animate_texture(dt)
        self.draw(window)


# --- Initialisation de Pygame ---
pygame.init()

# --- Configuration des composants ---
map_image, walls, coins, enemies_spawns = loader.load_map("map")
player = Player()
enemies = []

# --- Configuration de la fenêtre ---
window = pygame.display.set_mode((map_image.get_width(), map_image.get_height()))
pygame.display.set_caption("MyPacman")
BLACK = (0, 0, 0)

for i in range(3):
    spawn = enemies_spawns[randint(0, len(enemies_spawns) - 1)]
    enemies.append(Enemy(spawn))

clock = pygame.time.Clock()

# Boucle principale
running = True
while running:
    dt = clock.tick(60) / 1000.0

    # Gestion d'event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Gérer le mouvement du joueur
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move_up()
            elif event.key == pygame.K_DOWN:
                player.move_down()
            elif event.key == pygame.K_LEFT:
                player.move_left()
            elif event.key == pygame.K_RIGHT:
                player.move_right()

    # Réinitialiser la fenêtre
    window.fill(BLACK)

    # Afficher la map
    window.blit(map_image, (0, 0))

    # Mettre à jour les ennemis
    for enemy in enemies:
        enemy.update(dt, window, walls)

    # Mettre à jour le joueur
    player.update(dt, window, map_image, walls, coins, enemies, enemies_spawns)

    # Mettre à jour la fenêtre
    pygame.display.flip()

# Fermer la fenêtre
pygame.quit()
sys.exit()

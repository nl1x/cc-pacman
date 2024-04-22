from dont_touch_me import loader, entity
from random import randint

import pygame
import sys

# --- Initialisation de Pygame ---
pygame.init()

# --- Configuration des composants ---
map_image, walls, coins, enemies_spawns = loader.load_map("map")
player = entity.Player()
enemies = []

# --- Configuration de la fenêtre ---
window = pygame.display.set_mode((map_image.get_width(), map_image.get_height()))
pygame.display.set_caption("MyPacman")
BLACK = (0, 0, 0)

for i in range(3):
    spawn = enemies_spawns[randint(0, len(enemies_spawns) - 1)]
    enemies.append(entity.Enemy(spawn))

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

import sys

import dont_touch_me.constants as const
import dont_touch_me.tile as tile


def load_map(filename) -> tuple[tile.pygame.Surface, list[tile.Tile], list[tile.Tile], list[tile.Tile]]:
    colliders = []
    coins = []
    enemies_spawn = []
    tiles: list[list[tile.Tile]] = []
    with open(filename, "r") as file:
        line = file.readline()
        y = 0
        while line:
            tiles.append([])
            for x in range(len(line.strip("\n"))):
                tile_code = line[x]
                tile_sprite = tile.Tile(
                    tile_code,
                    x * const.TILE_MAP_SIZE[0],
                    y * const.TILE_MAP_SIZE[1],
                    tile.tiles[tile_code]
                )
                tiles[y].append(tile_sprite)
                if tile_sprite.is_wall():
                    colliders.append(tile_sprite)
                elif tile_sprite.is_coin():
                    coins.append(tile_sprite)
                elif tile_sprite.is_enemy_spawn():
                    enemies_spawn.append(tile_sprite)
            y += 1
            line = file.readline()
    maze = tile.pygame.Surface((len(tiles[0]) * const.TILE_MAP_SIZE[0], len(tiles) * const.TILE_MAP_SIZE[1]))
    maze.fill((0, 0, 0))
    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            tile_sprite = tiles[i][j]
            maze.blit(tile_sprite.image, (tile_sprite.x, tile_sprite.y))
    return maze, colliders, coins, enemies_spawn

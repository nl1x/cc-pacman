import sys

import dont_touch_me.constants as const
import dont_touch_me.tile as _map


def load_map(filename) -> tuple[_map.pygame.Surface, list[_map.Tile], list[_map.Tile], list[_map.Tile]]:
    colliders = []
    coins = []
    enemies_spawn = []
    tiles: list[list[_map.Tile]] = []
    with open(filename, "r") as file:
        line = file.readline()
        y = 0
        while line:
            tiles.append([])
            for x in range(len(line.strip("\n"))):
                tile_code = line[x]
                tile = _map.Tile(
                    tile_code,
                    x * const.TILE_MAP_SIZE[0],
                    y * const.TILE_MAP_SIZE[1],
                    const.TILE_MAP_SIZE[0],
                    const.TILE_MAP_SIZE[1],
                )
                tiles[y].append(tile)
                if tile.is_wall():
                    colliders.append(tile)
                elif tile.is_coin():
                    coins.append(tile)
                elif tile.is_enemy_spawn():
                    enemies_spawn.append(tile)
            y += 1
            line = file.readline()
    maze = _map.pygame.Surface((len(tiles[0]) * const.TILE_MAP_SIZE[0], len(tiles) * const.TILE_MAP_SIZE[1]))
    maze.fill((0, 0, 0))
    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            tile = tiles[i][j]
            maze.blit(tile.image, (tile.x, tile.y))
    return maze, colliders, coins, enemies_spawn

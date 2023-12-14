from __future__ import annotations
from typing import List
from azul.simple_types import Tile, compress_tile_list, STARTING_PLAYER
from azul.interfaces import UsedTilesGiveInterface, UsedTilesTakeAllInterface


class UsedTiles(UsedTilesGiveInterface, UsedTilesTakeAllInterface):
    _tiles: List[Tile]

    def __init__(self) -> None:
        self._tiles = []

    def give(self, tiles: List[Tile]) -> None:
        if STARTING_PLAYER in tiles:
            tiles.remove(STARTING_PLAYER)
        self._tiles.extend(tiles)

    def take_all(self) -> List[Tile]:
        new_copy: List[Tile] = self._tiles.copy()
        self._tiles.clear()
        return new_copy
        
    def state(self) -> str:
        return compress_tile_list(self._tiles)
    
    def get_tiles(self) -> List[Tile]:
        return self._tiles

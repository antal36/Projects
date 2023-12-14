from __future__ import annotations
from typing import List
from azul.simple_types import Tile, RED, YELLOW, GREEN, BLACK, BLUE, compress_tile_list
from azul.interfaces import RandomInterface, UsedTilesTakeAllInterface, BagInterface

class Bag(BagInterface):
    _tiles: List[Tile]

    def __init__(self, used_tiles: UsedTilesTakeAllInterface,
                random_generator: RandomInterface) -> None:
        self._tiles = []
        for _ in range(20):
            self._tiles.extend((RED, YELLOW, GREEN, BLACK, BLUE))
        
        self.used_tiles = used_tiles
        self.random_generator = random_generator

    def take(self, count: int) -> List[Tile]:
        if count > len(self._tiles):
            self._tiles.extend(self.used_tiles.take_all())
        
        result: List[Tile] = []
        permutation: List[int] = self.random_generator.permutation(len(self._tiles))
        for i in permutation:
            result.append(self._tiles[i])
        self._tiles = [value for index, value in enumerate(self._tiles) if index not in permutation]
        return result

    def state(self) -> str:
        return compress_tile_list(self._tiles)
    
    def len(self) -> int:
        return len(self._tiles)
    
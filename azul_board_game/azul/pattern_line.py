from __future__ import annotations
from typing import List
from azul.simple_types import Tile, Points, STARTING_PLAYER, compress_tile_list_with_empty_spaces
from azul.interfaces import UsedTilesGiveInterface, FloorInterface, WallLineInterface


class PatternLine:

    _tiles: List[Tile]
    _capacity: int
    used_tiles: UsedTilesGiveInterface
    _floor: FloorInterface
    _wall_line: WallLineInterface

    def __init__(self, capacity: int, used_tiles: UsedTilesGiveInterface,
                 floor: FloorInterface, wall_line: WallLineInterface) -> None:
        self._tiles = []
        self._capacity = capacity
        self.used_tiles = used_tiles
        self._floor = floor
        self._wall_line = wall_line

    def put(self, tiles: List[Tile]) -> None:
        if self._tiles:
            if self._tiles[0] != tiles[0]:
                self._floor.put(tiles)
                return
        if STARTING_PLAYER in tiles:
            self._floor.put([STARTING_PLAYER])
            tiles.remove(STARTING_PLAYER)
            if not tiles:
                return
        if self._wall_line.can_put_tile(tiles[0]):
            j: Tile
            for j in tiles:
                if len(self._tiles) < self._capacity:
                    self._tiles.append(j)
                else:
                    self._floor.put([j])
        else:
            self._floor.put(tiles)
            raise KeyError("Tile has already been put onto the wall line")
            
    def finish_round(self) -> Points:
        if len(self._tiles) == self._capacity:
            tile: Tile = self._tiles[0]
            self.used_tiles.give(self._tiles[1:])
            self._tiles = []
            return self._wall_line.put_tile(tile)
        return Points(0)

    def state(self) -> str:
        return compress_tile_list_with_empty_spaces(self._tiles + 
                        [None for _ in range(self._capacity - len(self._tiles))])

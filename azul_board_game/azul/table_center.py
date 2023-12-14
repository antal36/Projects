from __future__ import annotations
from typing import List
from azul.simple_types import Tile, compress_tile_list, STARTING_PLAYER
from azul.interfaces import TileSource, TableCenterInterface


class TableCenter(TileSource, TableCenterInterface):
    def __init__(self) -> None:
        self._tiles = []

    def take(self, _idx: Tile) -> List[Tile]:
        _tiles = [i for i in self._tiles if i == _idx]
        if not _tiles:
            raise KeyError("Unsuccessful take")
        if STARTING_PLAYER in self._tiles and STARTING_PLAYER not in _tiles:
            _tiles.append(STARTING_PLAYER)
            self._tiles.remove(STARTING_PLAYER)

        while _idx in self._tiles:
            self._tiles.remove(_idx)
        return _tiles

    def is_empty(self) -> bool:
        if len(self.state()) == 0:
            return True
        return False

    def state(self) -> str:
        return compress_tile_list(self._tiles)    
    
    def start_new_round(self) -> None:
        self._tiles.append(STARTING_PLAYER)

    def add(self, _tiles: List[Tile])-> None:
        self._tiles.extend(_tiles)

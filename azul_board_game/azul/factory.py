from __future__ import annotations
from typing import List
from azul.simple_types import Tile, compress_tile_list
from azul.interfaces import BagInterface, TileSource, TableCenterInterface


class Factory(TileSource):
    _tiles: List[Tile]

    def __init__(self, bag: BagInterface, table_center: TableCenterInterface) -> None:
        self._tiles = []
        self.bag = bag
        self.table_center = table_center

    def take(self, idx: Tile) -> List[Tile]:
        result_list: List[Tile] = [tile for tile in self._tiles if tile == idx]
        if not result_list:
            raise KeyError("Unsuccesful take")
        while idx in self._tiles:
            self._tiles.remove(idx)
        self.table_center.add(self._tiles)
        self._tiles.clear()
        return result_list

    def is_empty(self) -> bool:
        if len(self.state()) == 0:
            return True
        return False

    def state(self) -> str:
        return compress_tile_list(self._tiles)

    def start_new_round(self) -> None:
        self._tiles.extend(self.bag.take(4))

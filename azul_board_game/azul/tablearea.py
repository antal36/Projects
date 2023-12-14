from __future__ import annotations
from typing import List
from azul.simple_types import Tile
from azul.interfaces import TileSource, BagInterface
from azul.table_center import TableCenter
from azul.factory import Factory

class TableArea():
    _tile_sources: List[TileSource]

    def __init__(self, num_of_factories: int, bag: BagInterface) -> None:
        table_center: TableCenter = TableCenter()
        self._tile_sources = []
        self._tile_sources.append(table_center)
        for _ in range(num_of_factories):
            self._tile_sources.append(Factory(bag, table_center))

    def take(self, source_idx:int, idx: Tile) -> List[Tile]:
        return self._tile_sources[source_idx].take(idx)
    
    def is_round_end(self) -> bool:
        tile_source: TileSource
        for tile_source in self._tile_sources:
            if not tile_source.is_empty():
                return False
        return True

    def start_new_round(self) -> None:
        tile_source: TileSource
        for tile_source in self._tile_sources:
            tile_source.start_new_round()

    def state(self) -> str:
        result: str = ""
        tile_source: TileSource
        for tile_source in self._tile_sources:
            result += tile_source.state() + '\n'
        return result

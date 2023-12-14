from __future__ import annotations
import unittest
from typing import List, Optional
from azul.pattern_line import PatternLine
from azul.interfaces import UsedTilesGiveInterface, FloorInterface, WallLineInterface
from azul.simple_types import Points, Tile, RED, STARTING_PLAYER, compress_tile_list

class FakeUsedTilesGive(UsedTilesGiveInterface):
    def __init__(self) -> None:
        self._tiles: List[Tile] = []

    def give(self, tiles: List[Tile]) -> None:
        self._tiles.extend(tiles)

class FakeFloor(FloorInterface):
    def __init__(self) -> None:
        self._tiles: List[Tile] = []
    
    def put(self, tiles: List[Tile]) -> None:
        self._tiles.extend(tiles)
    
    def state(self) -> str:
        return compress_tile_list(self._tiles)

class FakeWallLine(WallLineInterface):
    def __init__(self) -> None:
        self._tiles: List[Optional[Tile]] = [None] * 5
        
    def can_put_tile(self, tile: Tile) -> bool:
        if self._tiles[0] is not None:
            return False
        if self._tiles[0] is None:
            return True
        return False
    
    def get_tiles(self) -> List[Optional[Tile]]:
        return self._tiles
    
    def put_tile(self, tile: Tile) -> Points:
        self._tiles[0] = tile
        return Points(1)
    
class TestPatternLine(unittest.TestCase):
    def setUp(self) -> None:
        self.used_tiles:UsedTilesGiveInterface  = FakeUsedTilesGive()
        self.floor: FloorInterface = FakeFloor()
        self.wall_line: WallLineInterface = FakeWallLine()
    
    def test_cap1(self) -> None:
        pattern_line: PatternLine = PatternLine(1, self.used_tiles, self.floor, self.wall_line)
        pattern_line.put([STARTING_PLAYER, RED])
        self.assertEqual(self.floor.state(), "S")
        self.assertEqual(pattern_line.finish_round().value, Points(1).value)
        self.assertEqual(pattern_line.state(), "_")
        self.assertEqual(self.wall_line.can_put_tile(RED), False)
        self.assertEqual(pattern_line.state(), "_")
    
    def test_cap2(self) -> None:
        pattern_line: PatternLine = PatternLine(4, self.used_tiles, self.floor, self.wall_line)
        self.assertEqual(pattern_line.state(), "____")
        pattern_line.put([RED])
        self.assertEqual(pattern_line.state(), "R___")
        self.assertEqual(pattern_line.finish_round().value, 0)
        pattern_line.put([RED, RED, RED])
        self.assertEqual(pattern_line.state(), "RRRR")
        self.assertEqual(pattern_line.finish_round().value, 1)

    def test_cap3(self) -> None:
        pattern_line: PatternLine = PatternLine(5, self.used_tiles, self.floor, self.wall_line)
        pattern_line.put([RED, RED, RED, RED, RED, RED])
        self.assertEqual(self.floor.state(), "R")

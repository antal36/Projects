from __future__ import annotations
import unittest
from typing import List
from azul.factory import Factory
from azul.interfaces import BagInterface, TableCenterInterface
from azul.simple_types import RED, Tile

class FakeBag(BagInterface):
    def __init__(self) -> None:
        self.bag = [RED for _ in range(100)]
    
    def take(self, count: int) -> List[Tile]:
        for _ in range(count):
            self.bag.pop()
        return [RED for _ in range(count)]

class FakeTableCenter(TableCenterInterface):
    def __init__(self) -> None:
        self._tiles: List[Tile] = []
    
    def add(self, tiles: List[Tile]) -> None:
        self._tiles.extend(tiles)
    
    @property
    def tiles(self) -> List[Tile]:
        return self._tiles

class TestFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.bag: FakeBag = FakeBag()
        self.table_center: FakeTableCenter = FakeTableCenter()
        self.factory: Factory = Factory(self.bag, self.table_center)
    
    def test_start_new_round(self) -> None:
        self.assertEqual(self.factory.state(), "")
        self.factory.start_new_round()
        self.assertEqual(self.factory.state(), "RRRR")
        self.assertEqual(len(self.bag.bag), 96)
    
    def test_take(self) -> None:
        self.assertEqual(self.factory.is_empty(), True)
        self.factory.start_new_round()
        self.assertEqual(self.factory.is_empty(), False)
        self.assertEqual(self.factory.take(RED), [RED, RED, RED, RED])
        self.assertEqual(self.table_center.tiles, [])
        self.assertEqual(self.factory.is_empty(), True)
    
    
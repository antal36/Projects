from __future__ import annotations
import unittest
from typing import List
from azul.bag import Bag
from azul.simple_types import Tile, RED, GREEN, BLACK, BLUE, YELLOW
from azul.interfaces import (TestRandomInterface, 
                    FakeUsedTilesTakeAllInterface, UsedTilesTakeAllInterface, RandomInterface)

class TestBag(unittest.TestCase):
    def setUp(self) -> None:
        used_tiles: UsedTilesTakeAllInterface = FakeUsedTilesTakeAllInterface()
        random: RandomInterface = TestRandomInterface()
        self.bag: Bag = Bag(used_tiles, random)
    
    def test_is_right(self) -> None:
        right_list: List[Tile] = []
        for _ in range(20):
            right_list.extend((RED, YELLOW, GREEN, BLACK, BLUE))
        self.assertEqual(self.bag.len(), 100)
        self.assertEqual(self.bag.state(), "RYGLB"*20)
    
    def test_take_few(self) -> None:
        self.assertCountEqual(self.bag.take(4), [RED, YELLOW, GREEN, BLACK])
    
    def test_take_more(self) -> None:
        testing_list: List[Tile] = self.bag.take(4) + self.bag.take(4)
        self.assertEqual(len(testing_list), 8)
        self.assertEqual(testing_list, [RED, YELLOW, GREEN, BLACK, BLUE, RED, YELLOW, GREEN])
    
    def test_take_more_times(self) -> None:
        testing_list : List[Tile] = []
        for _ in range(5):
            testing_list.extend(self.bag.take(4))
        self.assertEqual(len(testing_list), 20)
        testing_list.extend(self.bag.take(4))
        self.assertEqual(len(testing_list), 24)
    
    def test_take_all(self) -> None:
        for _ in range(25):
            self.bag.take(4)
        self.assertEqual(self.bag.state(), "")
    
    def test_take_in_bag(self) -> None:
        for _ in range(25):
            self.bag.take(4)
        self.bag.take(4)
        self.assertEqual(self.bag.state(), "B")
    
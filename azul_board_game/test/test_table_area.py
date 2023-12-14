import unittest
from typing import List
from azul.tablearea import TableArea
from azul.interfaces import (BagInterface, UsedTilesTakeAllInterface, 
                            RandomInterface, FakeUsedTilesTakeAllInterface, TestRandomInterface)
from azul.simple_types import Tile, RED, GREEN, STARTING_PLAYER



class FakeBag(BagInterface):
    _tiles: List[Tile]

    def __init__(self, used_tiles: UsedTilesTakeAllInterface,
                random_generator: RandomInterface) -> None:
        self._tiles = [GREEN, RED] * 50
        self.used_tiles = used_tiles
        self.random_generator = random_generator
    
    def take(self, count: int) -> List[Tile]:
        return [self._tiles.pop() for _ in range(count)]
        
class TestTableArea(unittest.TestCase):
    def setUp(self) -> None:
        used_tiles: FakeUsedTilesTakeAllInterface = FakeUsedTilesTakeAllInterface()
        random: TestRandomInterface = TestRandomInterface()
        self.bag: FakeBag = FakeBag(used_tiles, random)
        self.table_area: TableArea = TableArea(5, self.bag)
    
    def test_take_one(self) -> None:
        self.assertEqual(self.table_area.state(), '\n' * 6)
        self.table_area.start_new_round()
        self.assertEqual(self.table_area.state(), 'S\nRGRG\nRGRG\nRGRG\nRGRG\nRGRG\n')
        self.assertEqual(self.table_area.take(0, STARTING_PLAYER), [STARTING_PLAYER])
        self.assertEqual(self.table_area.state(), '\nRGRG\nRGRG\nRGRG\nRGRG\nRGRG\n')   
    
    def test_take_two(self) -> None:
        self.table_area.start_new_round()
        self.assertEqual(self.table_area.state(), 'S\nRGRG\nRGRG\nRGRG\nRGRG\nRGRG\n')
        self.assertEqual(self.table_area.take(1, RED), [RED, RED])
        self.assertEqual(self.table_area.state(), 'SGG\n\nRGRG\nRGRG\nRGRG\nRGRG\n')
        self.assertEqual(self.table_area.take(2, GREEN), [GREEN, GREEN])
        self.assertEqual(self.table_area.state(), 'SGGRR\n\n\nRGRG\nRGRG\nRGRG\n')
        self.table_area.take(3, RED)
        self.table_area.take(4, GREEN)
        self.table_area.take(5, GREEN)
        self.assertEqual(self.table_area.state(), 'SGGRRGGRRRR\n\n\n\n\n\n')
    
    def test_is_end(self) -> None:
        self.table_area.start_new_round()
        self.table_area.take(1, RED)
        self.table_area.take(2, RED)
        self.table_area.take(3, RED)
        self.table_area.take(4, RED)
        self.table_area.take(5, RED)
        self.table_area.take(0, GREEN)
        self.assertEqual(self.table_area.is_round_end(), True)
        self.table_area.start_new_round()
        self.assertEqual(self.table_area.state(), 'S\nRGRG\nRGRG\nRGRG\nRGRG\nRGRG\n')

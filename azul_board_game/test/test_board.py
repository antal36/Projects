from typing import List
import unittest
from azul.board import Board
from azul.interfaces import (GameFinishedInterface,
                            FinalPointsCalculationInterface, UsedTilesGiveInterface)

from azul.simple_types import NORMAL, FinishRoundResult, Points, Tile, RED, BLUE, GREEN

class FakeGameFinished(GameFinishedInterface):
    def game_finished(self, wall: List[List[Tile | None]]) -> FinishRoundResult:
        return NORMAL

class FakeFinalPointsCalculation(FinalPointsCalculationInterface):
    def get_points(self, wall: List[List[Tile | None]]) -> Points:
        return Points(2)
    
    def add_component(self, *components: FinalPointsCalculationInterface) -> None:
        return 

class FakeUsedTilesGive(UsedTilesGiveInterface):
    _tiles: List[Tile]

    def __init__(self) -> None:
        self._tiles = []
    
    def give(self, tiles: List[Tile]) -> None:
        self._tiles.extend(tiles)

    def take_all(self) -> List[Tile]:
        return [RED, BLUE]

class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.game_finished: FakeGameFinished = FakeGameFinished()
        self.used_tiles: FakeUsedTilesGive = FakeUsedTilesGive()
        self.final_points: FakeFinalPointsCalculation = FakeFinalPointsCalculation()
        self.board: Board = Board(self.game_finished, self.final_points, self.used_tiles)
    
    def test_put(self) -> None:
        i: int
        for i in range(5):
            self.assertEqual(self.board.pattern_lines[i].state(), "_" * (i+1))
        self.board.put(0, [RED])
        self.assertEqual(self.board.pattern_lines[0].state(), "R")
        self.board.put(1, [RED, RED])
        self.assertEqual(self.board.pattern_lines[1].state(), "RR")
        self.board.put(2, [RED, RED, RED])
        self.assertEqual(self.board.pattern_lines[2].state(), "RRR")
        self.board.put(3, [RED, RED, RED, RED])
        self.assertEqual(self.board.pattern_lines[3].state(), "RRRR")
        self.board.put(4, [RED, RED, RED, RED, RED])
        self.assertEqual(self.board.pattern_lines[4].state(), "RRRRR")
    
    def test_finish_round(self) -> None:
        i: int
        for i in range(5):
            self.board.put(i, [RED] * (i+1))
        self.board.finish_round()
        j: int
        for j in range(5):
            self.assertEqual(self.board.pattern_lines[j].state(), "_" * (j+1))
    
    def test_floor(self) -> None:
        self.board.put(0, [RED, RED])
        self.assertEqual(self.board.floor.state(), "R")
        self.board.put(1, [BLUE, BLUE, BLUE])
        self.assertEqual(self.board.floor.state(), "RB")
        self.board.put(2, [GREEN] * 4)
        self.assertEqual(self.board.floor.state(), "RBG")
        self.board.put(3, [RED] * 6)
        self.assertEqual(self.board.floor.state(), "RBGRR")
    
    def test_wall_line(self) -> None:
        i: int
        for i in range(5):
            self.board.put(i, [RED] * (i+1))
        self.board.finish_round()
        self.assertEqual(self.board.wall_line[0].state(), "__R__")
        self.assertEqual(self.board.wall_line[1].state(), "___R_")
        self.assertEqual(self.board.wall_line[2].state(), "____R")
        self.assertEqual(self.board.wall_line[3].state(), "R____")
        self.assertEqual(self.board.wall_line[4].state(), "_R___")
        j: int
        for j in range(5):
            self.board.put(j, [BLUE] * (i+1))
        self.board.finish_round()
        self.assertEqual(self.board.wall_line[0].state(), "B_R__")
        self.assertEqual(self.board.wall_line[1].state(), "_B_R_")
        self.assertEqual(self.board.wall_line[2].state(), "__B_R")
        self.assertEqual(self.board.wall_line[3].state(), "R__B_")
        self.assertEqual(self.board.wall_line[4].state(), "_R__B")
        
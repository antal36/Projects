from __future__ import annotations

from typing import List, Optional
from abc import ABC, abstractmethod
from azul.simple_types import Tile, Points, FinishRoundResult, RED, BLUE, BLACK, YELLOW, GREEN


class UsedTilesGiveInterface:
    def give(self, tiles: List[Tile]) -> None:
        pass

class GameFinishedInterface(ABC):
    @abstractmethod
    def game_finished(self, wall: List[List[Optional[Tile]]]) -> FinishRoundResult:
        pass

class TileSource(ABC):
    _idx: Tile #redefined idx variable
    _tiles: list[Tile]
    
    @abstractmethod
    def take(self, _idx: Tile) -> List[Tile]:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def state(self) -> str:
        pass
    
    @abstractmethod
    def start_new_round(self) -> None:
        pass


class WallLineAdjacentLineInterface(ABC):
    @abstractmethod
    def get_tile_in_column(self, column: int) -> Optional[Tile]:
        pass
    
    @abstractmethod
    def get_line_up(self) -> Optional[WallLineAdjacentLineInterface]:
        pass
    
    @abstractmethod
    def get_line_down(self) -> Optional[WallLineAdjacentLineInterface]:
        pass


class FinalPointsCalculationInterface(ABC):
    
    @abstractmethod
    def get_points(self, wall: List[List[Optional[Tile]]]) -> Points:
        pass

    @abstractmethod
    def add_component(self, *components: FinalPointsCalculationInterface) -> None:
        pass

class UsedTilesTakeAllInterface(ABC):
    @abstractmethod
    def take_all(self) -> List[Tile]:
        pass

class BagInterface(ABC):
    @abstractmethod
    def take(self, count: int) -> List[Tile]:
        pass

class FloorInterface(ABC):

    @abstractmethod
    def put(self, tiles: List[Tile]) -> None:
        pass

    @abstractmethod
    def state(self) -> str:
        pass


class WallLineInterface(ABC):

    @abstractmethod
    def can_put_tile(self, tile: Tile) -> bool:
        pass

    @abstractmethod
    def get_tiles(self) -> List[Optional[Tile]]:
        pass

    @abstractmethod
    def put_tile(self, tile: Tile) -> Points:
        pass

class RandomInterface(ABC):
    @abstractmethod
    def permutation(self, length: int) -> List[int]:
        pass

class TableCenterInterface(ABC):
    @abstractmethod
    def add(self, tiles: List[Tile]) -> None:
        pass

class TestRandomInterface(RandomInterface):
    def permutation(self, length: int) -> List[int]:
        return [0,1,2,3]

class FakeUsedTilesTakeAllInterface(UsedTilesTakeAllInterface):
    def take_all(self) -> List[Tile]:
        return [RED, YELLOW, GREEN, BLACK, BLUE]

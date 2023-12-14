from __future__ import annotations
from typing import List, Optional
from azul.interfaces import FinalPointsCalculationInterface
from azul.simple_types import Tile, Points


class FinalPointsCalculation(FinalPointsCalculationInterface):

    def __init__(self) -> None:
        self._components: List[FinalPointsCalculationInterface] = []

    def add_component(self, *components: FinalPointsCalculationInterface) -> None:
        for component in components:
            self._components.append(component)

    def get_points(self, wall: List[List[Optional[Tile]]]) -> Points:
        return Points.sum([component.get_points(wall) for component in self._components])
    

class WallPointsCalculation(FinalPointsCalculationInterface):
    
    def __init__(self) -> None:
        self._components: List[FinalPointsCalculationInterface] = []

    def add_component(self, *components: FinalPointsCalculationInterface) -> None:
        for component in components:
            self._components.append(component)

    def get_points(self, wall: List[List[Optional[Tile]]]) -> Points:
        return Points.sum([component.get_points(wall) for component in self._components])


class HorizontalRowPointsCalculation(FinalPointsCalculationInterface):

    def get_points(self, wall: List[List[Optional[Tile]]]) -> Points:
        points = 0
        for row in wall:
            if None not in row:
                points += 2

        return Points(points)
    
    def add_component(self, *components: FinalPointsCalculationInterface) -> None:
        return


class VerticalColumnPointsCalculation(FinalPointsCalculationInterface):

    def get_points(self, wall: List[List[Optional[Tile]]]) -> Points:
        points = 0
        for column in range(5):
            if None not in [row[column] for row in wall]:
                points += 7
            
        return Points(points)
    def add_component(self, *components: FinalPointsCalculationInterface) -> None:
        return


class ColorPointsCalculation(FinalPointsCalculationInterface):
    
    def get_points(self, wall: List[List[Optional[Tile]]]) -> Points:
        points = 0
        for i in range(5):
            if None not in [row[(i + j) % 5] for j, row in enumerate(wall)]:
                points += 10

        return Points(points)
    def add_component(self, *components: FinalPointsCalculationInterface) -> None:
        return 
    
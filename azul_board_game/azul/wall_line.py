from __future__ import annotations
from typing import List, Optional
from azul.simple_types import Tile, Points, compress_tile_list_with_empty_spaces
from azul.interfaces import WallLineAdjacentLineInterface, WallLineInterface

class WallLine(WallLineAdjacentLineInterface, WallLineInterface):
    _tile_types: List[Tile]
    _tiles: List[Optional[Tile]]
    _line_up: Optional[WallLineAdjacentLineInterface]
    _line_down: Optional[WallLineAdjacentLineInterface]
    _after_put_point_counter: AfterPutPointCounter

    def __init__(self, tile_types: List[Tile]) -> None:
        self._tile_types = tile_types
        self._tiles = [None] * 5
        self._line_up = None
        self._line_down = None
        self._after_put_point_counter = AfterPutPointCounter()

    def can_put_tile(self, tile: Tile) -> bool:
        return self._tiles[self._tile_types.index(tile)] is None

    def get_tiles(self) -> List[Optional[Tile]]:
        return self._tiles

    def put_tile(self, tile: Tile) -> Points:
        col = self._tile_types.index(tile)
        self._tiles[col] = tile
                
        return self._after_put_point_counter.count_points_after_put(self._tiles, col,
                                                                    self._line_up, self._line_down)
    
    def get_tile_in_column(self, column: int) -> Optional[Tile]:
        return self._tiles[column]
    
    def state(self) -> str:
        return compress_tile_list_with_empty_spaces(self._tiles)

    def get_line_up(self) -> Optional[WallLineAdjacentLineInterface]:
        return self._line_up
    
    def put_line_up(self, line_up: Optional[WallLineAdjacentLineInterface]) -> None:
        self._line_up = line_up
    
    def get_line_down(self) -> Optional[WallLineAdjacentLineInterface]:
        return self._line_down
    
    def put_line_down(self, line_down: Optional[WallLineAdjacentLineInterface]) -> None:
        self._line_down = line_down
    
    
class AfterPutPointCounter:
    """Takes care of counting points after tile is put on WallLine"""
    
    def count_points_after_put(self, tiles: List[Optional[Tile]], col: int,
                               line_up: Optional[WallLineAdjacentLineInterface], 
                               line_down: Optional[WallLineAdjacentLineInterface]) -> Points:
        """Checks if any tile is adjacent to the put tile
        
        If not, returns Points(1), if yes, calls point counter methods for row and column
        """
        
        has_adj_row: bool = any(tile is not None for tile in self.row_adjacent_tiles(tiles, col))
        has_adj_vertical: bool = any(tile is not None for tile in 
                                     self.vertical_adjacent_tiles(line_up, line_down, col))
        
        if has_adj_row or has_adj_vertical:
            points: Points = Points(0)
            if has_adj_row:
                points = Points.sum([points, self.count_row_points(tiles, col)])
            if has_adj_vertical:
                points = Points.sum([points, self.count_column_points(line_up, line_down, col)])
                
            return points
        
        return Points(1)
    
    def row_adjacent_tiles(self, tiles: List[Optional[Tile]], col: int) -> List[Optional[Tile]]:
        """Returns two tiles adjacent horizontally to put tile, None in place of no tile"""
        return [tiles[col - 1] if col > 0 else None,
                tiles[col + 1] if col < (len(tiles) - 1) else None]
    
    def vertical_adjacent_tiles(self, line_up: Optional[WallLineAdjacentLineInterface], 
                               line_down: Optional[WallLineAdjacentLineInterface],
                               col: int) -> List[Optional[Tile]]:
        """Returns two tiles adjacent vertically to put tile, None in place of no tile"""
        return [line_up.get_tile_in_column(col) if line_up is not None else None,
                line_down.get_tile_in_column(col) if line_down is not None else None]

    
    def count_row_points(self, tiles: List[Optional[Tile]], col: int) -> Points:
        """Counts length of row of tiles, where the tile has been put"""
        empty_before: int = -1
        tile_before: Optional[Tile]
        for i, tile_before in enumerate(tiles[:col]):
            if tile_before is None:
                empty_before = i
        
        empty_after: int = len(tiles)
        tile_after: Optional[Tile]
        for i, tile_after in enumerate(tiles[col:]):
            if tile_after is None:
                empty_after = col + i
                break

        return Points(empty_after - empty_before - 1)
    
    def count_column_points(self, line_up: Optional[WallLineAdjacentLineInterface], 
                              line_down: Optional[WallLineAdjacentLineInterface],
                              col: int) -> Points:
        """Counts length of column of tiles, where the tile has been put"""
        vertical_points: Points = Points(1)
        current_wall_line: Optional[WallLineAdjacentLineInterface] = line_up
        while current_wall_line is not None:
            if current_wall_line.get_tile_in_column(col) is not None:
                vertical_points = Points.sum([vertical_points, Points(1)])
            else:
                break
            current_wall_line = current_wall_line.get_line_up()
        
        current_wall_line = line_down
        while current_wall_line is not None:
            if current_wall_line.get_tile_in_column(col) is not None:
                vertical_points = Points.sum([vertical_points, Points(1)])
            else:
                break
            current_wall_line = current_wall_line.get_line_down()
        
        return vertical_points

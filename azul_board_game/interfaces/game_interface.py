from __future__ import annotations
from abc import ABC, abstractmethod


class GameInterface(ABC):
    @abstractmethod
    def take(self, player_id: int, source_idx: int, tile_idx: int, destination_idx: int) -> bool:
        """Method for communicating between players and the game
        
        returns whether the move was successful
            whether was player on turn and whether all Idxs were valid
        
        playerId - identification of the player
        sourceIdx - from what TileSource he takes a Tile/Tiles
        tileIdx - which type of Tile he takes
        destinationIdx - on which PatternLine he places the Tile/Tiles
        """

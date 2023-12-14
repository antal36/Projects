from __future__ import annotations
from typing import List, Optional
from azul.simple_types import Tile, FinishRoundResult, NORMAL, GAME_FINISHED
from azul.interfaces import GameFinishedInterface


class GameFinished(GameFinishedInterface):
    
    def game_finished(self, wall: List[List[Optional[Tile]]]) -> FinishRoundResult:
        """Determines whether game should end
        
        Gets board wall state as a 2D list as an argument
        """
        line: List[Optional[Tile]]
        for line in wall:
            if None not in line:
                return GAME_FINISHED
        
        return NORMAL

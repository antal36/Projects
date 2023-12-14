from __future__ import annotations
from typing import List, Dict, Tuple
from azul.bag import Bag
from azul.board import Board
from azul.interfaces import TestRandomInterface
from azul.interfaces import GameFinishedInterface, FinalPointsCalculationInterface
from azul.used_tiles import UsedTiles
from azul.game_finished import GameFinished
from azul.final_points_calculation import FinalPointsCalculation
from azul.simple_types import Tile, STARTING_PLAYER, compress_tile_list, Points
from azul.tablearea import TableArea
from azul.game_observer import GameObserver
from azul.observer import Observer
from interfaces.observer_interface import ObserverInterface
from interfaces.game_observer_interface import GameObserverInterface

class Game:
    _player_ids: List[int]
    _dict_of_players: Dict[int, Board]
    _bag: Bag
    _random: TestRandomInterface
    _used_tiles: UsedTiles
    _game_finished: GameFinishedInterface
    _final_points: FinalPointsCalculationInterface
    _table_area: TableArea
    _num_of_factories: int
    _playing_order: List[int]
    _player_to_start: int
    _observer: ObserverInterface
    _game_observer: GameObserverInterface
    _end_game: bool

    def __init__(self) -> None:
        self._playing_order = []
        self._end_game = False

    def start_game(self, player_ids: List[int]) -> bool:
        if len(player_ids) < 2 or len(player_ids) > 4:
            return False
        if len(set(player_ids)) != len(player_ids):
            return False
        self._player_to_start = player_ids[0]
        self._playing_order = player_ids
        self._dict_of_players = {}
        self._random = TestRandomInterface()
        self._used_tiles = UsedTiles()
        self._game_finished = GameFinished()
        self._final_points = FinalPointsCalculation()
        self._bag = Bag(self._used_tiles, self._random)
        num_of_factories = len(self._playing_order) * 2 + 1
        self._table_area = TableArea(num_of_factories, self._bag)
        self._table_area.start_new_round()
        self._game_observer = GameObserver()
        self._end_game = True
        player: int
        for player in self._playing_order:
            _observer = Observer()
            self._game_observer.register_observer(_observer)
            self._dict_of_players[player] = Board(self._game_finished,
                                                    self._final_points, self._used_tiles)
        return True
        
    def take(self, player_id: int, destination_idx: int,
             source_idx: int, tile_idx: Tile) -> bool:
        if self._playing_order[0] != player_id:
            return False
        try:
            if not self._end_game:
                print("Game has already ended")
                return False
            tiles: List[Tile] = self._table_area.take(source_idx, tile_idx)
            self._game_observer.notify_everybody(str(player_id) + '''
                                                has taken: ''' + compress_tile_list(tiles))
            if STARTING_PLAYER in tiles:
                self._player_to_start = player_id
            self._dict_of_players[player_id].put(destination_idx, tiles)
            self._game_observer.notify_everybody(str(player_id) + '''
                                has placed tiles to pattern line number ''' + str(destination_idx))

            if self._table_area.is_round_end():
                player: Tuple[int, Board]
                condition_list: List[str] = []
                for player in self._dict_of_players.items():
                    condition_list.append(str(player[1].finish_round()))
                if "gameFinished" in condition_list:
                    for player in self._dict_of_players.items():
                        player[1].end_game()
                    self.end_game()
                else:
                    self._playing_order = [self._player_to_start] + self._playing_order[
                        self._playing_order.index(self._player_to_start)+1:]+ self._playing_order[
                             :self._playing_order.index(self._player_to_start)]
                        
                    self._table_area.start_new_round()
                    self._game_observer.notify_everybody("New round is starting")
            else:
                self._playing_order.append(self._playing_order.pop(0))
            return True
        except KeyError:
            self._game_observer.notify_everybody("Invalid move")
            return False
        
    @property
    def table_area_gettter(self) -> TableArea:
        return self._table_area
    
    def board_state(self, player_id:int) -> str:
        return self._dict_of_players[player_id].state()
    
    def end_game(self) -> None:
        self._end_game = False
        self._game_observer.notify_everybody("Game has ended")
        list_of_points: List[Points] = []
        winner: int = 0
        winner_points = Points(0)
        player: Tuple[int, Board]
        for player in self._dict_of_players.items():
            if winner_points.value <= player[1].points.value:
                winner = player[0]
            list_of_points.append(player[1].points)
        print("Game has ended")
        print(f"The winner is player with ID: {winner}")

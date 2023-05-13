from board import Board
from ai import AI


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.current_player = 1

    def update_current_player(self):
        if self.current_player == 1 and len(self.board.get_available_moves(2)) > 0:
            self.current_player = 2
        elif self.current_player == 2 and len(self.board.get_available_moves(1)) > 0:
            self.current_player = 1

    def make_move(self, coord):
        self.board.move(self.current_player, coord)
        self.update_current_player()

    def ai_move(self, heuristic=1, depth=2, pruning=True):
        self.board.move(
            self.current_player,
            self.ai.get_next_move(
                self.board, self.current_player, heuristic, depth, pruning
            )[0],
        )
        self.update_current_player()

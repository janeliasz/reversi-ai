from copy import deepcopy
from math import inf
import time

from board import Board


class AI:
    def __init__(self):
        self.common_board = Board()
        self.heuristic = 1

        self.nodes_visited = 0

    def fields_difference_heuristic(self):
        return self.common_board.get_result()

    def mobility_heuristic(self):
        own_mobility = len(self.common_board.get_available_moves(1)) - len(
            self.common_board.get_available_moves(2)
        )

        max_player_potential_mobility = sum(
            1
            for _ in filter(
                lambda coord: self.common_board.is_adjacent_to_empty_field(coord),
                self.common_board.get_player_fields(2),
            )
        )
        min_player_potential_mobility = sum(
            1
            for _ in filter(
                lambda coord: self.common_board.is_adjacent_to_empty_field(coord),
                self.common_board.get_player_fields(1),
            )
        )

        return own_mobility + (
            max_player_potential_mobility - min_player_potential_mobility
        )

    def weights_heuristic(self):
        weights = {
            (0, 0): 4,
            (0, 1): -3,
            (0, 2): 2,
            (0, 3): 2,
            (0, 4): 2,
            (0, 5): 2,
            (0, 6): -3,
            (0, 7): 4,
            (1, 0): -3,
            (1, 1): -4,
            (1, 2): -1,
            (1, 3): -1,
            (1, 4): -1,
            (1, 5): -1,
            (1, 6): -4,
            (1, 7): -3,
            (2, 0): 2,
            (2, 1): -1,
            (2, 2): 1,
            (2, 3): 0,
            (2, 4): 0,
            (2, 5): 1,
            (2, 6): -1,
            (2, 7): 2,
            (3, 0): 2,
            (3, 1): -1,
            (3, 2): 0,
            (3, 3): 1,
            (3, 4): 1,
            (3, 5): 0,
            (3, 6): -1,
            (3, 7): 2,
            (4, 0): 2,
            (4, 1): -1,
            (4, 2): 0,
            (4, 3): 1,
            (4, 4): 1,
            (4, 5): 0,
            (4, 6): -1,
            (4, 7): 2,
            (5, 0): 2,
            (5, 1): -1,
            (5, 2): 1,
            (5, 3): 0,
            (5, 4): 0,
            (5, 5): 1,
            (5, 6): -1,
            (5, 7): 2,
            (6, 0): -3,
            (6, 1): -4,
            (6, 2): -1,
            (6, 3): -1,
            (6, 4): -1,
            (6, 5): -1,
            (6, 6): -4,
            (6, 7): -3,
            (7, 0): 4,
            (7, 1): -3,
            (7, 2): 2,
            (7, 3): 2,
            (7, 4): 2,
            (7, 5): 2,
            (7, 6): -3,
            (7, 7): 4,
        }

        max_player_weighted_value = sum(
            weights[coord] for coord in self.common_board.get_player_fields(1)
        )
        min_player_weighted_value = sum(
            weights[coord] for coord in self.common_board.get_player_fields(2)
        )

        return max_player_weighted_value - min_player_weighted_value

    def eval(self):
        if self.heuristic == 2:
            return self.mobility_heuristic()
        elif self.heuristic == 3:
            return self.weights_heuristic()
        else:
            return self.fields_difference_heuristic()

    def minimax(self, fields, depth, is_maximizing):
        self.nodes_visited += 1
        self.common_board.fields = deepcopy(fields)

        if depth == 0 or self.common_board.is_game_over():
            return (self.eval(), None)

        optimal_move = None

        if is_maximizing:
            maxEval = -inf
            for move in self.common_board.get_available_moves(1):
                self.common_board.move(1, move)
                result, _ = self.minimax(
                    self.common_board.fields,
                    depth - 1,
                    False
                    if len(self.common_board.get_available_moves(2)) > 0
                    else True,
                )
                if result > maxEval:
                    maxEval = result
                    optimal_move = move
                self.common_board.fields = deepcopy(fields)
            return (maxEval, optimal_move)
        else:
            minEval = +inf
            for move in self.common_board.get_available_moves(2):
                self.common_board.move(2, move)
                result, _ = self.minimax(
                    self.common_board.fields,
                    depth - 1,
                    True
                    if len(self.common_board.get_available_moves(1)) > 0
                    else False,
                )
                if result < minEval:
                    minEval = result
                    optimal_move = move
                self.common_board.fields = deepcopy(fields)
            return (minEval, optimal_move)

    def alpha_beta(self, fields, depth, alpha, beta, is_maximizing):
        self.nodes_visited += 1
        self.common_board.fields = deepcopy(fields)

        if depth == 0 or self.common_board.is_game_over():
            return (self.eval(), None)

        optimal_move = None

        if is_maximizing:
            maxEval = -inf
            for move in self.common_board.get_available_moves(1):
                self.common_board.move(1, move)
                result, _ = self.alpha_beta(
                    self.common_board.fields,
                    depth - 1,
                    alpha,
                    beta,
                    False
                    if len(self.common_board.get_available_moves(2)) > 0
                    else True,
                )
                self.common_board.fields = deepcopy(fields)
                if result > maxEval:
                    optimal_move = move
                maxEval = max(maxEval, result)
                alpha = max(alpha, result)
                if beta <= alpha:
                    break
            return (maxEval, optimal_move)
        else:
            minEval = +inf
            for move in self.common_board.get_available_moves(2):
                self.common_board.move(2, move)
                result, _ = self.alpha_beta(
                    self.common_board.fields,
                    depth - 1,
                    alpha,
                    beta,
                    True
                    if len(self.common_board.get_available_moves(1)) > 0
                    else False,
                )
                self.common_board.fields = deepcopy(fields)
                if result < minEval:
                    optimal_move = move
                minEval = min(minEval, result)
                beta = min(beta, result)
                if beta <= alpha:
                    break
            return (minEval, optimal_move)

    def get_next_move(self, board, player, heuristic, depth, pruning):
        self.heuristic = heuristic

        self.nodes_visited = 0
        start = time.time()
        next_move = (
            self.alpha_beta(
                board.fields, depth, -inf, +inf, True if player == 1 else False
            )[1]
            if pruning == True
            else self.minimax(board.fields, depth, True if player == 1 else False)[1]
        )
        end = time.time()
        total_time = end - start
        return (next_move, total_time, self.nodes_visited)

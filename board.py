class IllegalMoveException(Exception):
    pass


directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


def add_coords(coord_1, coord_2):
    return (coord_1[0] + coord_2[0], coord_1[1] + coord_2[1])


def get_coords_between(coord_1, coord_2):
    result = []
    direction_dict = {}
    for axis in range(0, 2):
        if coord_1[axis] == coord_2[axis]:
            direction_dict[axis] = 0
        elif coord_1[axis] < coord_2[axis]:
            direction_dict[axis] = 1
        else:
            direction_dict[axis] = -1
    direction = (direction_dict[0], direction_dict[1])

    if direction not in directions:
        return []

    analyzed_coord = add_coords(coord_1, direction)
    while analyzed_coord != coord_2:
        result.append(analyzed_coord)
        analyzed_coord = add_coords(analyzed_coord, direction)

    return result


def is_in_board(coord):
    return coord[0] >= 0 and coord[0] < 8 and coord[1] >= 0 and coord[1] < 8


class Board:
    def __init__(self):
        self.fields = {}
        self.fields[(3, 3)] = 2
        self.fields[(3, 4)] = 1
        self.fields[(4, 3)] = 1
        self.fields[(4, 4)] = 2

    def get_player_fields(self, current_player):
        return [
            coord for coord, value in self.fields.items() if value == current_player
        ]

    def is_player_field(self, current_player, coord):
        return coord in self.get_player_fields(current_player)

    def is_enemy_field(self, current_player, coord):
        return self.is_player_field(2 if current_player == 1 else 1, coord)

    def is_empty_field(self, coord):
        return is_in_board(coord) and coord not in self.fields

    def is_adjacent_to_empty_field(self, coord):
        for direction in directions:
            analyzed_coord = add_coords(coord, direction)
            if self.is_empty_field(analyzed_coord):
                return True

    def get_available_moves(self, current_player):
        result = set()

        player_fields = self.get_player_fields(current_player)
        for coord in player_fields:
            for direction in directions:
                analyzed_coord = add_coords(coord, direction)
                while self.is_enemy_field(current_player, analyzed_coord):
                    analyzed_coord = add_coords(analyzed_coord, direction)
                    if self.is_empty_field(analyzed_coord):
                        result.add(analyzed_coord)

        return result

    def is_game_over(self):
        return len(self.get_available_moves(1)) == len(self.get_available_moves(2)) == 0

    def get_result(self):
        return len(self.get_player_fields(1)) - len(self.get_player_fields(2))

    def get_player_result(self, player):
        return len(self.get_player_fields(player))

    def move(self, current_player, coord):
        if coord not in self.get_available_moves(current_player):
            self.print()
            print(current_player, coord)
            raise IllegalMoveException("Illegal move!")

        self.fields[coord] = current_player

        gained_fields = []
        for direction in directions:
            analyzed_coord = add_coords(coord, direction)
            while self.is_enemy_field(current_player, analyzed_coord):
                analyzed_coord = add_coords(analyzed_coord, direction)
            if self.is_player_field(current_player, analyzed_coord):
                gained_fields += get_coords_between(coord, analyzed_coord)

        for gained_coord in gained_fields:
            self.fields[gained_coord] = current_player

    def print(self):
        for i in range(0, 8):
            print("  --- --- --- --- --- --- --- ---")
            row = ""
            for j in range(0, 8):
                row += " | " + str(self.fields[(i, j)] if (i, j) in self.fields else 0)
            row += " |"
            print(row)
        print("  --- --- --- --- --- --- --- ---")

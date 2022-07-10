import Move

PAWN_VALUE = 1
KNIGHT_VALUE = 4
BISHOP_VALUE = 3
ROOK_VALUE = 5
QUEEN_VALUE = 10
KING_VALUE = 1000


class Piece:

    def __init__(self, cell, is_white, starting_pos=None):

        self.cell = cell

        if starting_pos:
            self.starting_position = starting_pos
        else:
            self.starting_position = (cell.row, cell.column)

        self.times_moved = 0
        self.is_white = is_white
        self.value = 0
        self.active = True

        if self.is_white:
            self.name = "White " + self.__class__.__name__
        else:
            self.name = "Black " + self.__class__.__name__

    def __eq__(self, other):
        return self.starting_position == other.starting_position and self.is_white == other.is_white and self.value == other.value

    def get_name(self):
        return self.name

    def in_bounds(self, move):
        return 7 >= self.cell.row + move[0] >= 0 and 7 >= self.cell.column + move[1] >= 0

    # Checks if piece is in check after making the move (no move by default, current position) passed in function
    def in_check(self, board, move=(0, 0)):

        new_position = [self.cell.row + move[0], self.cell.column + move[1]]

        for row in range(8):
            for column in range(8):
                if board[row][column].chess_piece:
                    piece = board[row][column].chess_piece
                    if piece != self and piece.active and (piece.is_white == (not self.is_white)):

                        if type(
                                piece) == King:  # if we call re-call get king moves on the other king, will call an
                            # endless recursion loop

                            all_new_moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (-1, 1), (1, 1), (-1, -1)]
                        elif type(piece) == Pawn:

                            if piece.is_white:
                                all_new_moves = [[-1, -1], [-1, 1]]
                            else:

                                all_new_moves = [[1, 1], [1, -1]]
                        else:
                            all_new_moves = [elem.move for elem in piece.get_all_moves(board)]

                        for other_move in all_new_moves:

                            if new_position == [piece.cell.row + other_move[0], piece.cell.column + other_move[1]]:
                                # print("CHECK: " + str(c.name))
                                return True
        return False


class Pawn(Piece):

    def __init__(self, cell, is_white):
        super().__init__(cell, is_white)
        self.value = PAWN_VALUE

    def get_all_moves(self, board, last_move):

        moves = []

        if not self.is_white:

            if self.in_bounds([2, 0]) and self.cell.row == 1:  # Don't use self.times_moved == 0 in case setting up
                # board that's not in default position
                c = board[self.cell.row + 1][self.cell.column].chess_piece
                d = board[self.cell.row + 2][self.cell.column].chess_piece
                if not c or not c.active:
                    if not d or not d.active:
                        moves.append(Move.Move(self, [self.cell.row, self.cell.column], [2, 0]))

            if self.in_bounds([1, 0]):
                c = board[self.cell.row + 1][self.cell.column].chess_piece
                if not c or not c.active:

                    if self.cell.row + 1 == 7:
                        for selection in ['q', 'n', 'r', 'b']:
                            moves.append(Move.Move(self, [self.cell.row, self.cell.column], [1, 0], promoted=True,
                                                   promotion=selection))
                    else:
                        moves.append(Move.Move(self, [self.cell.row, self.cell.column], [1, 0]))

            for move in [[1, 1], [1, -1]]:
                if self.in_bounds(move):
                    piece = board[self.cell.row + move[0]][self.cell.column + move[1]].chess_piece
                    if piece and piece.is_white and piece.active:

                        if self.cell.row + 1 == 7:
                            for selection in ['q', 'n', 'r', 'b']:
                                moves.append(Move.Move(self, [self.cell.row, self.cell.column], move, promoted=True,
                                                       promotion=selection))
                        else:
                            moves.append(Move.Move(self, [self.cell.row, self.cell.column], move))

        else:

            if self.in_bounds([-2, 0]) and self.cell.row == 6:  # Don't use self.times_moved == 0 in case setting up
                # board that's not in default position
                c = board[self.cell.row - 1][self.cell.column].chess_piece
                d = board[self.cell.row - 2][self.cell.column].chess_piece
                if not c or not c.active:
                    if not d or not d.active:
                        moves.append(Move.Move(self, [self.cell.row, self.cell.column], [-2, 0]))

            if self.in_bounds([-1, 0]):
                c = board[self.cell.row - 1][self.cell.column].chess_piece

                if not c or not c.active:

                    if self.cell.row - 1 == 0:

                        for selection in ['q', 'n', 'r', 'b']:
                            moves.append(Move.Move(self, [self.cell.row, self.cell.column], [-1, 0], promoted=True,
                                                   promotion=selection))

                    else:
                        moves.append(Move.Move(self, [self.cell.row, self.cell.column], [-1, 0]))
            for move in [[-1, -1], [-1, 1]]:
                if self.in_bounds(move):
                    piece = board[self.cell.row + move[0]][self.cell.column + move[1]].chess_piece
                    if piece and not piece.is_white and piece.active:
                        if self.cell.row - 1 == 0:

                            for selection in ['q', 'n', 'r', 'b']:
                                moves.append(Move.Move(self, [self.cell.row, self.cell.column], move, promoted=True,
                                                       promotion=selection))
                        else:
                            moves.append(Move.Move(self, [self.cell.row, self.cell.column], move))

        # Check for En passant
        if last_move:
            if last_move.en_passant and last_move.piece == self:
                moves.append(last_move)


            # print(last_move.piece.name, last_move.move, last_move.new_pos)
            elif type(last_move.piece) == Pawn and (last_move.piece.is_white != self.is_white) and abs(last_move.move[0]) == 2:
                if last_move.new_pos[0] == self.cell.row:
                    if abs(last_move.new_pos[1] - self.cell.column) == 1:
                        if self.is_white:
                            inc = -1
                        else:
                            inc = 1
                        # print("En passant")

                        m = [inc, last_move.new_pos[1] - self.cell.column]
                        # print(m)
                        move = Move.Move(self, [self.cell.row, self.cell.column], m, en_passant=True)
                        move.removed_piece = last_move.piece
                        moves.append(move)

        return moves


class Rook(Piece):
    def __init__(self, cell, team_color):
        super().__init__(cell, team_color)
        self.value = ROOK_VALUE
        self.castle = True  # used when making board from FEN string

    def get_all_moves(self, board):

        moves = []
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        for direction in directions:
            for i in range(1, 8):
                move = [direction[0] * i, direction[1] * i]
                if self.in_bounds(move):
                    c = board[self.cell.row + move[0]][self.cell.column + move[1]].chess_piece
                    if c and c.active:
                        if c.is_white == (not self.is_white):
                            moves.append(Move.Move(self, [self.cell.row, self.cell.column], move))

                        break
                    moves.append(Move.Move(self, [self.cell.row, self.cell.column], move))

        return moves


class Knight(Piece):
    def __init__(self, cell, team_color):
        super().__init__(cell, team_color)
        self.value = KNIGHT_VALUE

    def get_all_moves(self, board):

        possible_moves = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2)]
        valid_moves = []
        for move in possible_moves:
            if self.in_bounds(move):
                c = board[self.cell.row + move[0]][self.cell.column + move[1]]
                if c.chess_piece and c.chess_piece.active:
                    if c.chess_piece.is_white == (not self.is_white):
                        valid_moves.append(Move.Move(self, [self.cell.row, self.cell.column], move))

                else:
                    valid_moves.append(Move.Move(self, [self.cell.row, self.cell.column], move))

        return valid_moves


class Bishop(Piece):
    def __init__(self, cell, team_color):
        super().__init__(cell, team_color)
        self.value = BISHOP_VALUE

    def get_all_moves(self, board):

        moves = []
        directions = [(1, -1), (-1, 1), (1, 1), (-1, -1)]
        for direction in directions:
            for i in range(1, 8):
                move = [direction[0] * i, direction[1] * i]
                if self.in_bounds(move):
                    c = board[self.cell.row + move[0]][self.cell.column + move[1]].chess_piece
                    if c and c.active:
                        if c.is_white == (not self.is_white):
                            moves.append(Move.Move(self, [self.cell.row, self.cell.column], move))
                        break
                    moves.append(Move.Move(self, [self.cell.row, self.cell.column], move))

        return moves


class Queen(Piece):
    def __init__(self, cell, team_color):
        super().__init__(cell, team_color)
        self.value = QUEEN_VALUE

    # Queen's move are just the combined moveset of a bishop and rook on same tile
    def get_all_moves(self, board):
        moves = Bishop.get_all_moves(self, board)
        moves.extend(Rook.get_all_moves(self, board))
        return moves


class King(Piece):
    def __init__(self, cell, team_color):
        super().__init__(cell, team_color)
        self.value = KING_VALUE
        self.castle = True  # used when making board from FEN string

    def get_all_moves(self, board):

        moves = []
        possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (-1, 1), (1, 1), (-1, -1)]
        for move in possible_moves:
            if self.in_bounds(move):
                c = board[self.cell.row + move[0]][self.cell.column + move[1]].chess_piece
                if c and c.active:
                    if c.is_white == (not self.is_white):
                        if not self.in_check(board, move):
                            moves.append(Move.Move(self, [self.cell.row, self.cell.column], move))
                else:
                    if not self.in_check(board, move):
                        moves.append(Move.Move(self, [self.cell.row, self.cell.column], move))

        # Castling moves

        l, r = self.can_castle(board)
        # print(l,r)
        if l:
            move = [0, -2]
            rook = board[self.cell.row][0].chess_piece
            moves.append(
                Move.Move(self, [self.cell.row, self.cell.column], move, castling=True, rook=rook, rook_move=[0, 3]))
        if r:
            move = [0, 2]
            rook = board[self.cell.row][7].chess_piece
            moves.append(
                Move.Move(self, [self.cell.row, self.cell.column], move, castling=True, rook=rook, rook_move=[0, -2]))

        return moves

    def can_castle(self, board):

        if self.in_check(board, [0, 0]) or self.times_moved > 0 or not self.castle:
            return False, False

        l, r = True, True

        # check left
        for i in range(1, 4):
            if board[self.cell.row][i].chess_piece and board[self.cell.row][i].chess_piece.active:
                l = False
        if board[self.cell.row][0].chess_piece:
            c = board[self.cell.row][0].chess_piece
            if not (type(c) == Rook and c.times_moved == 0 and c.castle and c.active):
                l = False
        else:
            l = False
        # check if passing through check
        moves = [[0, -i] for i in range(1, 3)]

        for move in moves:
            if self.in_check(board, move):
                l = False

        # check right

        for i in range(5, 7):
            if board[self.cell.row][i].chess_piece and board[self.cell.row][i].chess_piece.active:
                r = False
        if board[self.cell.row][7].chess_piece:
            c = board[self.cell.row][7].chess_piece
            if not (type(c) == Rook and c.times_moved == 0 and c.castle and c.active):
                r = False
        else:
            r = False

        # check if passing through check
        moves = [[0, i] for i in range(1, 3)]
        for move in moves:
            if self.in_check(board, move):
                r = False

        return l, r

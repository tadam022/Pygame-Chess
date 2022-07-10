import Cell
import Pieces
import Move

WHITE = (255, 255, 255)
GREY = (196, 196, 196)

DEFAULT_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq"


class GameState:
    WHITE_CHECK = 1
    BLACK_CHECK = 2
    STALEMATE = 3
    WHITE_WIN = 4
    BLACK_WIN = 5


class ChessBoard:

    def __init__(self, fen=None, square_side_length=80, line_thickness=0, divider_thickness=0, screen_border=0):
        self.board = create_chess_board(square_side_length, line_thickness, divider_thickness, screen_border)

        self.stalemate = False
        self.black_win = False
        self.white_win = False
        self.white_turn = True
        self.turn = 1
        self.white_king = None
        self.black_king = None

        self.chess_pieces = []
        self.read_fen(fen)

        self.en_passant_capture = None  # flag for if theres an en_passant move available on the board
        self.last_move = None

    # Creates the chessboard layout of the specified FEN string. Does not currently support en-passant specification
    def read_fen(self, fen):

        try:
            fen = fen.split(" ")

        except AttributeError:
            print("Invalid FEN string format. Using default FEN string")
            fen = DEFAULT_FEN
            fen = fen.split(" ")
        if len(fen) < 3:
            fen = DEFAULT_FEN
            fen = fen.split(" ")

        piece_string = fen[0]
        piece_string = piece_string.split("/")

        # turn
        if fen[1] == 'b':

            self.white_turn = False
        else:
            self.white_turn = True

        # Set full turn number if given
        if len(fen) == 6:
            try:
                self.turn = int(fen[5])
            except ValueError:
                pass

        # castling
        white_castle_queenside = False
        white_castle_kingside = False
        black_castle_queenside = False
        black_castle_kingside = False

        castling_string = fen[2]

        for char in castling_string:
            if char == 'K':
                white_castle_kingside = True
            elif char == 'k':
                black_castle_kingside = True
            elif char == 'Q':
                white_castle_queenside = True
            elif char == 'q':
                black_castle_queenside = True
            # if char == '-' dont have to do anything
        castling = [white_castle_queenside, white_castle_kingside, black_castle_queenside, black_castle_kingside]

        # Add chess pieces
        pieces = []
        row = 0
        col = 0
        for line in piece_string:
            for elem in line:
                if elem.isnumeric():
                    col += int(elem)
                else:
                    pieces.append(self.make_piece(elem, row, col, castling))
                    col += 1
            col = 0
            row += 1

        self.chess_pieces = pieces

    def make_piece(self, letter, row, col, castling):

        if letter == 'r':
            piece = Pieces.Rook(self.board[row][col], False)
            if row == 0 and col == 0 and not castling[2]:
                piece.castle = False

            elif row == 0 and col == 7 and not castling[3]:
                piece.castle = False

        elif letter == 'R':
            piece = Pieces.Rook(self.board[row][col], True)
            if row == 7 and col == 0 and not castling[0]:
                piece.castle = False

            elif row == 7 and col == 7 and not castling[1]:
                piece.castle = False

        elif letter == 'b':
            piece = Pieces.Bishop(self.board[row][col], False)
        elif letter == 'B':
            piece = Pieces.Bishop(self.board[row][col], True)
        elif letter == 'n':
            piece = Pieces.Knight(self.board[row][col], False)
        elif letter == 'N':
            piece = Pieces.Knight(self.board[row][col], True)
        elif letter == 'p':
            piece = Pieces.Pawn(self.board[row][col], False)
        elif letter == 'P':
            piece = Pieces.Pawn(self.board[row][col], True)
        elif letter == 'k':
            piece = Pieces.King(self.board[row][col], False)
            self.black_king = piece
            if not (row == 0 and col == 4 and (castling[2] or castling[3])):
                piece.castle = False

        elif letter == 'K':
            piece = Pieces.King(self.board[row][col], True)
            self.white_king = piece
            if not (row == 7 and col == 4 and (castling[0] or castling[1])):
                piece.castle = False

        elif letter == 'q':
            piece = Pieces.Queen(self.board[row][col], False)
        elif letter == 'Q':
            piece = Pieces.Queen(self.board[row][col], True)
        else:
            piece = None

        if piece:
            piece.cell.chess_piece = piece

        return piece

    # gets score of board
    def evaluation(self):

        white_score, black_score = 0, 0
        for piece in self.chess_pieces:
            if piece.is_white:
                white_score += piece.value
            else:
                black_score += piece.value

        return white_score - black_score

    def get_state(self):

        all_moves = []
        if self.white_turn:
            if not self.white_king.in_check(self.board, [0, 0]):
                for piece in self.chess_pieces:
                    if piece.active and piece.is_white:
                        moves = self.get_valid_moves(piece)
                        all_moves.append(moves)
                if not all_moves:
                    return GameState.STALEMATE

            else:
                if self.is_checkmate(self.white_king):
                    # print("CHECKMATE - Black Win")

                    return GameState.BLACK_WIN

        else:

            if not self.black_king.in_check(self.board, [0, 0]):
                for piece in self.chess_pieces:
                    if piece.active and not piece.is_white:
                        moves = self.get_valid_moves(piece)
                        all_moves.append(moves)
                if not all_moves:
                    return GameState.STALEMATE
            else:
                if self.is_checkmate(self.black_king):
                    # print("CHECKMATE - White Win")

                    return GameState.WHITE_WIN

        if self.white_king.in_check(self.board, [0, 0]):
            return GameState.WHITE_CHECK

        elif self.black_king.in_check(self.board, [0, 0]):

            return GameState.BLACK_CHECK

        return None

    def is_checkmate(self, king):

        for piece in self.chess_pieces:
            if piece.active and piece.is_white == king.is_white:
                moves = self.get_valid_moves(piece)
                if moves:
                    return False
        return True

    def promotion(self, move, new_cell):
        piece = move.piece
        selection = move.promotion
        if selection == 'b':
            promoted_piece = Pieces.Bishop(piece.cell, piece.is_white)
        elif selection == 'n':
            promoted_piece = Pieces.Knight(new_cell, piece.is_white)
        elif selection == 'r':
            promoted_piece = Pieces.Rook(new_cell, piece.is_white)
        else:
            promoted_piece = Pieces.Queen(new_cell, piece.is_white)

        promoted_piece.times_moved = piece.times_moved
        move.promoted_to_piece = promoted_piece

        return promoted_piece

    def move_piece(self, move, promotion_selection=None):
        piece = move.piece
        piece.cell.chess_piece = None
        new_cell = self.board[move.new_pos[0]][move.new_pos[1]]

        if move.castling:

            rook = move.rook

            if move.move == [0, 2]:  # king castling right
                # print(" castling right")
                rook_move = Move.Move(rook, [rook.cell.row, rook.cell.column], move.rook_move)
            else:  # king castling left
                rook_move = Move.Move(rook, [rook.cell.row, rook.cell.column], move.rook_move)

            self.move_piece(rook_move)
            self.white_turn = not self.white_turn

        elif new_cell.chess_piece:

            move.removed_piece = new_cell.chess_piece

        if move.removed_piece and self.chess_pieces:
            move.removed_piece.cell.chess_piece = None
            move.removed_piece.active = False

        piece.cell = new_cell
        piece.cell.chess_piece = piece
        piece.times_moved += 1

        if move.promoted:
            if promotion_selection:
                move.promotion = promotion_selection
            new_promoted_piece = self.promotion(move, new_cell)

            for i in range(len(self.chess_pieces)):
                if self.chess_pieces[i] == piece:
                    self.chess_pieces[i].cell.chess_piece = new_promoted_piece
                    self.chess_pieces[i] = new_promoted_piece

            # piece.active = False

        self.last_move = move
        self.white_turn = not self.white_turn

    def undo_move(self, move):
        last = self.last_move
        reverse = [-1 * move.move[0], -1 * move.move[1]]

        if move.promoted:

            reverse_move = Move.Move(move.promoted_to_piece, move.promoted_to_piece.cell.position, reverse)

            move.piece.times_moved += 1
        else:
            reverse_move = Move.Move(move.piece, move.piece.cell.position, reverse)

        self.move_piece(reverse_move)
        move.piece.times_moved -= 2  # undo move is only called after its been moved.

        if move.promoted:

            for i in range(len(self.chess_pieces)):
                if self.chess_pieces[i] == move.promoted_to_piece:
                    self.chess_pieces[i] = move.piece
                    move.piece.cell = move.promoted_to_piece.cell

                    move.piece.cell.chess_piece = move.piece
                    break

        elif move.castling:

            rook_move = Move.Move(move.rook, move.piece.cell.position, move.rook_move)
            self.undo_move(rook_move)
            self.white_turn = not self.white_turn

        if move.removed_piece:
            move.removed_piece.active = True
            move.removed_piece.cell.chess_piece = move.removed_piece

        self.last_move = last

    # Gets all moves that won't leave the piece's king in check
    def get_valid_moves(self, selected_piece):

        last = self.last_move
        turn = self.white_turn

        if selected_piece.is_white:  # so can see valid moves for opponent even if its not their turn
            king = self.white_king
        else:
            king = self.black_king

        if type(selected_piece) == Pieces.Pawn:

            possible_moves = selected_piece.get_all_moves(self.board, last)
        else:
            possible_moves = selected_piece.get_all_moves(self.board)

        valid_moves = []

        for move in possible_moves:

            if move.castling:  # already checked if legal when creating the castling move in get_all_moves()
                valid_moves.append(move)
                continue
            self.move_piece(move)

            if not king.in_check(self.board, [0, 0]):
                valid_moves.append(move)

            self.undo_move(move)

        # so last move and turn stays the same as before this method was called
        self.last_move = last
        self.white_turn = turn
        return valid_moves

    def color_king_check(self, gamestate):
        if gamestate == GameState.WHITE_CHECK:
            self.white_king.cell.color_check()
        elif gamestate == GameState.BLACK_CHECK:
            self.black_king.cell.color_check()

    def show_piece_moves(self, moves, player_turn):
        if moves:
            for move in moves:
                try:
                    c = self.board[move.new_pos[0]][move.new_pos[1]]
                    c.color_movable(player_turn)
                except IndexError:
                    print("INDEX ERROR")
                    print(move)

                    continue

    def check_if_cells_hovered(self):
        cell_hovered = None
        for row in self.board:
            for cell in row:
                if cell.is_hovered():
                    cell.color_hover()

                    cell_hovered = cell
                else:
                    cell.reset_color()
        return cell_hovered

    def get_piece_clicked(self):
        for row in self.board:
            for cell in row:
                if cell.is_hovered() and cell.chess_piece and cell.chess_piece.active:
                    return cell.chess_piece
        return None

    def get_clicked_cell(self):
        for row in self.board:
            for cell in row:
                if cell.is_hovered():
                    return cell

    def get_number_active_pieces(self):
        white = 0
        black = 0
        for piece in self.chess_pieces:
            if piece.active:
                if piece.is_white:

                    white += 1
                else:
                    black += 1

        return white, black


def create_chess_board(square_side_length=80, line_thickness=0, divider_thickness=0, screen_border=0):
    chess_board = [[] for _ in range(8)]
    y = divider_thickness + screen_border
    color_white = True

    for row in range(8):
        x = divider_thickness + screen_border
        color_white = not color_white
        for column in range(8):
            x_coord = x + line_thickness
            y_coord = y + line_thickness

            if color_white:
                color = WHITE
                color_white = False
            else:
                color = GREY
                color_white = True
            cell = Cell.Cell(x_coord, y_coord, row, column, color, square_side_length)
            chess_board[row].append(cell)

            x += line_thickness + square_side_length

        y += line_thickness + square_side_length

    return chess_board

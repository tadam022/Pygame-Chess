import ChessBoard
import unittest


# Perft results used in these tests are taken from: https://www.chessprogramming.org/Perft_Results

# Note that in these tests, besides Nodes, all other info acquired includes the previous depths' result for that info.
# The Nodes counted are only the leaf nodes.
# E.g. the number of checks for Position 3  at depth 4 is found to be 1959, which is the sum of 1680, 267, 10, 2 found
# at depths 4, 3, 2 and 1 respectively.


class Test(unittest.TestCase):

    def setUp(self):
        # Position 1
        self.ChessBoard_1 = ChessBoard.ChessBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 ")
        # Position 2
        self.ChessBoard_2 = ChessBoard.ChessBoard("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq")
        # Position 3
        self.ChessBoard_3 = ChessBoard.ChessBoard("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - ")
        # Position 4
        self.ChessBoard_4 = ChessBoard.ChessBoard("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1")
        # Position 4 mirrored
        self.ChessBoard_4b = ChessBoard.ChessBoard("r2q1rk1/pP1p2pp/Q4n2/bbp1p3/Np6/1B3NBn/pPPP1PPP/R3K2R b KQ - 0 1 ")
        # Position 5
        self.ChessBoard_5 = ChessBoard.ChessBoard("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
        # Position 6
        self.ChessBoard_6 = ChessBoard.ChessBoard("r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10 ")

    def test_perft_results(self):

        res_1 = move_number_test(self.ChessBoard_1, 3)
        self.assertEqual(res_1, (8902, 34, 0, 0, 0, 12, 0))

        res_2 = move_number_test(self.ChessBoard_2, 3)
        self.assertEqual(res_2, (97862, 17102+351+8, 45+1, 3162+91+2, 0, 993+3, 1))

        res_3 = move_number_test(self.ChessBoard_3, 4)
        self.assertEqual(res_3, (43238, 3348+209+14+1, 123+2, 0, 0, 1680+267+10+2, 17))

        res_4 = move_number_test(self.ChessBoard_4, 3)
        self.assertEqual(res_4, (9467, 1021+87, 4, 0+6, 120+48, 38+10, 22))

        res_4b = move_number_test(self.ChessBoard_4b, 3)
        self.assertEqual(res_4b, (9467, 1021 + 87, 4, 0 + 6, 120 + 48, 38 + 10, 22))

        res_5 = move_number_test(self.ChessBoard_5, 3)
        self.assertEqual(res_5[0], 62379)

        res_6 = move_number_test(self.ChessBoard_6, 2)
        self.assertEqual(res_6[0], 2079)

def move_number_test(chess_board, depth):

    if depth == 0:

        return 1, 0, 0, 0, 0, 0, 0

    n = 0
    checks = 0
    removed_pieces = 0
    castles = 0
    promotions = 0
    en_passant = 0
    checkmates = 0
    all_moves = []

    for piece in chess_board.chess_pieces:

        if piece.is_white == chess_board.white_turn and piece.active:

            valid_moves = chess_board.get_valid_moves(piece) # appending during promotion moves wont give accurate results

            all_moves.extend(valid_moves)

    for m in all_moves:

        chess_board.move_piece(m)
        state = chess_board.get_state()
        if state in [ChessBoard.GameState.BLACK_CHECK, ChessBoard.GameState.WHITE_CHECK]:
            checks += 1
        elif state in [ChessBoard.GameState.WHITE_WIN, ChessBoard.GameState.BLACK_WIN]:
            checks += 1
            checkmates += 1

        if m.removed_piece:

            removed_pieces += 1
            if m.en_passant:

                en_passant += 1

        if m.castling:
            castles += 1

        if m.promoted:
            promotions += 1

        result = move_number_test(chess_board, depth - 1)
        n += result[0]

        removed_pieces += result[1]
        en_passant += result[2]
        castles += result[3]
        promotions += result[4]
        checks += result[5]
        checkmates += result[6]
        chess_board.undo_move(m)

    return n, removed_pieces, en_passant, castles, promotions, checks, checkmates


def main(fen=None):

    if not fen:
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 "



    chess_board = ChessBoard.ChessBoard(fen)
    print("----------------------------------------------------------")
    print("Nodes, captures, en_passants, castles, promotions, checks, checkmates")

    print(move_number_test(chess_board, 1))

if __name__ == "__main__":
    #fen = "r5k1/1P6/8/8/8/8/1p6/2R4K"
    #main()
    unittest.main()

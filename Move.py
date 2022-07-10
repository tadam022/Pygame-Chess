class Move:
    def __init__(self, piece, start_pos, move, en_passant=False, castling=False, rook=None, rook_move=None,
                 promoted=False, promotion='q'):

        self.piece = piece

        self.en_passant = en_passant
        self.castling = castling

        self.move = move
        self.start_pos = start_pos
        self.new_pos = start_pos[0] + move[0], start_pos[1] + move[1]
        self.removed_piece = None  # Opponent's piece removed from attacking

        self.rook = rook
        self.rook_move = rook_move

        self.promoted = promoted  # Was promoted
        self.promotion = promotion  # Promotion selection
        self.promoted_to_piece = None  # Promoted piece it turned into

import sys
import pygame
import ChessBoard
import Pieces

FPS = 60

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_GREY = (96, 96, 96)
WHITE = (255, 255, 255)
TEAL = (0, 150, 255)

SQUARE_SIDE_LENGTH = 80
LINE_THICKNESS = 0
DIVIDER_THICKNESS = 0

ROWS = 8
COLUMNS = 8
SCREEN_BORDER = 0

SCREEN_HEIGHT = ((SQUARE_SIDE_LENGTH + LINE_THICKNESS) * ROWS) - (LINE_THICKNESS * 2) + (
        DIVIDER_THICKNESS * 4) + (SCREEN_BORDER * 2)
SCREEN_WIDTH = ((SQUARE_SIDE_LENGTH + LINE_THICKNESS) * COLUMNS) + LINE_THICKNESS - (LINE_THICKNESS * 2) + (
        DIVIDER_THICKNESS * 4) + (SCREEN_BORDER * 2)

pygame.init()
clock = pygame.time.Clock()
screen_display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess")

screen_rect = pygame.Rect(
    [SCREEN_BORDER, SCREEN_BORDER, SCREEN_WIDTH - (SCREEN_BORDER * 2), SCREEN_HEIGHT - (SCREEN_BORDER * 2)])
pygame.draw.rect(screen_display, BLACK, screen_rect)

white_pawn_image = pygame.image.load("pieces_images/Chess_plt60.png")

black_pawn_image = pygame.image.load("pieces_images/Chess_pdt60.png")

white_rook_image = pygame.image.load("pieces_images/Chess_rlt60.png")
black_rook_image = pygame.image.load("pieces_images/Chess_rdt60.png")

white_knight_image = pygame.image.load("pieces_images/Chess_nlt60.png")
black_knight_image = pygame.image.load("pieces_images/Chess_ndt60.png")

white_bishop_image = pygame.image.load("pieces_images/Chess_blt60.png")
black_bishop_image = pygame.image.load("pieces_images/Chess_bdt60.png")

white_queen_image = pygame.image.load("pieces_images/Chess_qlt60.png")
black_queen_image = pygame.image.load("pieces_images/Chess_qdt60.png")

white_king_image = pygame.image.load("pieces_images/Chess_klt60.png")
black_king_image = pygame.image.load("pieces_images/Chess_kdt60.png")


def draw_chess_board(chess_board):
    for row in range(ROWS):
        for column in range(COLUMNS):
            pygame.draw.rect(screen_display, chess_board[row][column].color,
                             chess_board[row][column].rect
                             )


def get_piece_image(piece):
    if type(piece) == Pieces.Pawn:
        if piece.is_white:
            return white_pawn_image
        else:
            return black_pawn_image
    elif type(piece) == Pieces.Rook:
        if piece.is_white:
            return white_rook_image
        else:
            return black_rook_image
    elif type(piece) == Pieces.Knight:
        if piece.is_white:
            return white_knight_image
        else:
            return black_knight_image
    elif type(piece) == Pieces.Bishop:
        if piece.is_white:
            return white_bishop_image
        else:
            return black_bishop_image
    elif type(piece) == Pieces.Queen:
        if piece.is_white:
            return white_queen_image
        else:
            return black_queen_image
    elif type(piece) == Pieces.King:
        if piece.is_white:
            return white_king_image
        else:
            return black_king_image


def draw_pieces(pieces, selected_piece):
    for piece in pieces:
        if piece.active:
            board_cell = piece.cell
            img = get_piece_image(piece)
            center_x = (board_cell.square_length - img.get_width()) // 2
            center_y = (board_cell.square_length - img.get_height()) // 2
            screen_display.blit(img, (board_cell.x + center_x, board_cell.y + center_y))

        if selected_piece and selected_piece.active:
            if selected_piece == piece:
                outline_rect = pygame.Rect(piece.cell.x, piece.cell.y, piece.cell.square_length,
                                           piece.cell.square_length)
                pygame.draw.rect(screen_display, RED, outline_rect, 5)


def get_game_state_message(game_state):
    if game_state == ChessBoard.GameState.WHITE_CHECK:
        message = "White in check."
    elif game_state == ChessBoard.GameState.BLACK_CHECK:
        message = "Black in check."
    elif game_state == ChessBoard.GameState.STALEMATE:
        message = "Stalemate. It's a draw."
    elif game_state == ChessBoard.GameState.WHITE_WIN:
        message = "Checkmate. White wins."
    elif game_state == ChessBoard.GameState.BLACK_WIN:
        message = "Checkmate. Black wins."
    else:
        message = None
    return message


def draw_promotion_box(surface):
    font = pygame.font.SysFont('Sans', 20, True, False)
    text = "Press q for Queen | " \
           "Press n for Knight | " \
           "Press r for Rook | " \
           "Press b for Bishop "
    text_surface = font.render(text, True, WHITE)
    rect = text_surface.get_rect()
    w = rect.w // 2
    h = rect.h // 2
    x = SCREEN_WIDTH // 2 - w
    y = SCREEN_HEIGHT // 2 - h

    spacing = 20

    # border
    pygame.draw.rect(surface, TEAL, [x - spacing, y - spacing, rect.w + spacing * 2, rect.h + spacing * 2])

    pygame.draw.rect(surface, BLACK, [x - 10, y - 10, rect.w + 20, rect.h + 20])
    surface.blit(text_surface, (x, y))


def draw_text_box(surface, game_state):
    font = pygame.font.SysFont('Sans', 50, True, False)
    text = get_game_state_message(game_state)

    if text:
        text_surface = font.render(text, True, WHITE)

        rect = text_surface.get_rect()
        w = rect.w // 2
        h = rect.h // 2
        x = SCREEN_WIDTH // 2 - w
        y = SCREEN_HEIGHT // 2 - h

        spacing = 20

        # border
        pygame.draw.rect(surface, TEAL, [x - spacing, y - spacing, rect.w + spacing * 2, rect.h + spacing * 2])

        pygame.draw.rect(surface, BLACK, [x - 10, y - 10, rect.w + 20, rect.h + 20])
        surface.blit(text_surface, (x, y))


def get_promotion_selection():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    promotion_selection = 'q'
                elif event.key == pygame.K_n:
                    promotion_selection = 'n'
                elif event.key == pygame.K_r:
                    promotion_selection = 'r'
                elif event.key == pygame.K_b:
                    promotion_selection = 'b'
                else:
                    promotion_selection = ''
                print(promotion_selection)
                if promotion_selection:
                    return promotion_selection


def main(fen=None, debug=False):
    original_fen = fen
    chess_board = ChessBoard.ChessBoard(fen)

    selected_piece = None
    moves = []
    move_stack = []

    pop_up = False
    promotion_pop_up = False
    game_state = None

    promotion_selection = ''

    while True:

        chess_board.check_if_cells_hovered()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_button = event.button

                if mouse_button == 1 and (pop_up or promotion_pop_up):

                    pop_up = False
                    promotion_pop_up = False

                    if game_state in [ChessBoard.GameState.STALEMATE, ChessBoard.GameState.WHITE_WIN,
                                      ChessBoard.GameState.BLACK_WIN]:
                        chess_board = ChessBoard.ChessBoard(original_fen)

                        selected_piece = None

                        moves = []
                        move_stack = []

                        pop_up = False  #
                        promotion_pop_up = False  #

                        game_state = None

                elif mouse_button == 1 and not selected_piece and not pop_up:

                    selected_piece = chess_board.get_piece_clicked()

                    if selected_piece:

                        moves = chess_board.get_valid_moves(selected_piece)
                        if debug:
                            print("White turn: ", chess_board.white_turn)
                            print(
                                f"{selected_piece.name},  # Moves Available: {len(moves)},  Times Moved: {selected_piece.times_moved}  ", )

                            if chess_board.last_move:
                                print("Last move:", end='')
                                print(chess_board.last_move.piece.name, chess_board.last_move.move, end=' ')

                                print("En Passant:",chess_board.last_move.en_passant)
                            else:
                                print("Last move: none")

                            print("------------------------------------------------------------------\n")

                        # print(moves)

                    else:
                        print("No piece selected")

                elif mouse_button == 1 and selected_piece and not pop_up:

                    if selected_piece.is_white and chess_board.white_turn or not selected_piece.is_white and not chess_board.white_turn:
                        cell = chess_board.get_clicked_cell()

                        if moves:
                            for move in moves:

                                if move.new_pos == cell.get_grid_position():
                                    if move.promoted and not promotion_pop_up and not promotion_selection:
                                        promotion_pop_up = True

                                    else:

                                        chess_board.move_piece(move, promotion_selection)
                                        move_stack.append(move)

                                        # chess_board.white_turn = not chess_board.white_turn
                                        chess_board.turn += 1
                                        game_state = chess_board.get_state()
                                        promotion_selection = None
                                    break

                        elif chess_board.get_state() == ChessBoard.GameState.STALEMATE:
                            pop_up = True

                    selected_piece = None
                    if game_state:

                        pop_up = True

                elif mouse_button == 3 and not selected_piece and not pop_up:
                    '''
                    remove_piece = chess_board.get_piece_clicked()
                    if remove_piece:
                        remove_piece.cell.chess_piece = None
                        remove_piece.active = False
                    '''
            elif event.type == pygame.KEYDOWN and not pop_up:

                if promotion_pop_up:

                    if event.key == pygame.K_q:
                        promotion_selection = 'q'
                    elif event.key == pygame.K_n:
                        promotion_selection = 'n'
                    elif event.key == pygame.K_r:
                        promotion_selection = 'r'
                    elif event.key == pygame.K_b:
                        promotion_selection = 'b'
                    else:
                        promotion_selection = None
                    if promotion_selection:
                        promotion_pop_up = False
                    #print(promotion_selection)

                if event.key == pygame.K_SPACE:
                    w, b = chess_board.get_number_active_pieces()
                    print(f"White Pieces: {w}   Black Pieces: {b}")

                elif event.key == pygame.K_c:  # Reset

                    chess_board = ChessBoard.ChessBoard(original_fen)

                    selected_piece = None

                    moves = []
                    move_stack = []
                    game_state = None

                    pop_up = False
                    promotion_pop_up = False

                    promotion_selection = None

                elif event.key == pygame.K_d:
                    if move_stack:
                        last_move = move_stack.pop()
                        chess_board.undo_move(last_move)

                        chess_board.turn -= 1
                        game_state = chess_board.get_state()

        if selected_piece:
            if selected_piece.is_white == chess_board.white_turn:
                chess_board.show_piece_moves(moves, True)
            else:
                chess_board.show_piece_moves(moves, False)

        chess_board.color_king_check(game_state)

        draw_chess_board(chess_board.board)
        draw_pieces(chess_board.chess_pieces, selected_piece)

        if pop_up:

            draw_text_box(screen_display, game_state)
        elif promotion_pop_up:

            draw_promotion_box(screen_display)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    #fen = "r5k1/1P6/8/8/8/8/1p6/2R4K"
    main(debug=True)

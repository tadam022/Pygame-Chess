import pygame

YELLOW = (245, 255, 10)
BLUE = (0, 0, 255)
GREEN = (0, 180, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (196, 196, 196)
DARK_GREEN = (0, 128, 0)
ORANGE = (255, 185, 0)
DARK_ORANGE = (165, 120, 0)

class Cell:
    def __init__(self, x, y, row, column, color, square_length=50):

        self.color = color
        self.original_color = color
        self.x = x  # Left-most GUI x position of cell
        self.y = y  # Top-most GUI y position of cell
        self.row = row
        self.column = column
        self.position = self.row, self.column
        self.square_length = square_length
        self.rect = pygame.Rect(self.x, self.y, square_length, square_length)
        self.chess_piece = None

    def get_position(self):
        return self.x, self.y

    def get_grid_position(self):
        return self.row, self.column

    def is_hovered(self):
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            return True
        else:
            return False

    def color_hover(self):
        if self.chess_piece:
            self.color = BLUE
        else:
            self.color = YELLOW

    def color_movable(self, player_turn):
        if player_turn:
            if self.color == WHITE:
                self.color = GREEN
            elif self.color == GREY:
                self.color = DARK_GREEN
        else:
            if self.color == WHITE:
                self.color = ORANGE
            elif self.color == GREY:
                self.color = DARK_ORANGE

    def color_check(self):
        self.color = RED

    def reset_color(self):
        self.color = self.original_color

    def change_cell_color(self, color):
        self.color = color

import pygame
import os

# importing our chesskers (number) board
from chesskers import Board

# Constants declared for Board Size
SQ_SIZE = 100
BOARD_HEIGHT = 800
BOARD_WIDTH = 800
# Board Dimensions
ROWS = 8
COLS = 8
SQSIZE = (BOARD_WIDTH) // COLS  # Size of each individual square...


class Color:  # Class for creating colors: to be used below in Theme
    def __init__(self, light, dark):
        self.light = light
        self.dark = dark
        pygame.init()


class Theme:  # Class for creating color schemes of board.
    def __init__(
        self, light_bg, dark_bg, light_trace, dark_trace, light_moves, dark_moves
    ):
        self.bg = Color(light_bg, dark_bg)
        self.trace = Color(light_trace, dark_trace)
        self.moves = Color(light_moves, dark_moves)


class Sound:  # Uses paths to assets file to create Sound objects.
    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(path)

    def play(self):
        pygame.mixer.Sound.play(self.sound)


class Config:  # Combines themes and sounds into Config objects.
    def __init__(self):
        self.themes = []
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont("monospace", 18, True)
        self.move_sound = Sound(os.path.join("assets/sounds/move.wav"))
        self.capture_sound = Sound(os.path.join("assets/sounds/capture.wav"))
        self.castling_sound = Sound(os.path.join("assets/sounds/castle.wav"))
        self.end_game_sound = Sound(os.path.join("assets/sounds/game-end.wav"))
        self.notify_sound = Sound(os.path.join("assets/sounds/notify.wav"))
        self.promotion_sound = Sound(os.path.join("assets/sounds/promote.wav"))

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]

    def _add_themes(self):
        green = Theme(
            (234, 235, 200),
            (119, 154, 88),
            (244, 247, 116),
            (172, 195, 51),
            "#C86464",
            "#C84646",
        )
        blue = Theme(
            (235, 209, 166),
            (165, 170, 80),
            (245, 234, 100),
            (209, 185, 59),
            "#C86464",
            "#C84646",
        )
        brown = Theme(
            (229, 228, 200),
            (60, 95, 135),
            (183, 187, 227),
            (43, 119, 191),
            "#C86464",
            "#C84646",
        )
        gray = Theme(
            (120, 119, 118),
            (86, 85, 84),
            (99, 126, 143),
            (82, 102, 128),
            "#C86464",
            "#C84646",
        )
        self.themes = [green, blue, brown, gray]


# Dragger objects help outline how far classes will go
# TODO: turn Dragger to have a self and square argument and NO self.piece
class Dragger:
    def __init__(self, initial, final):
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    # Primary blit method (for updating piece positions)

    def update_blit(self, surface):
        # texture
        # self.piece.set_texture(size=128)
        # texture = self.piece.texture
        # image
        # img = pygame.image.load(texture)
        # rectangle
        img_center = (self.mouseX, self.mouseY)
        # self.piece.texture_rect = img.get_rect(center=img_center)
        # update blit
        # surface.blit(img, self.piece.texture_rect)

    # Other methods (storing updated positions & actually doing the dragging)

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE


class Display:  # The main class behind this file.
    def __init__(self, surface):
        # Initializing starting board to have a board to draw...
        board = """put other data here
         r n b q k b n r
         p p p p p p p p
         . . . . . . . .
         . . . . . . . .
         . . . . . . . .
         . . . . . . . .
         P P P P P P P P
         R N B Q K B N R"""
        self.board = Board()  # Creating a board object from starting position.
        self.config = Config()
        self.squares = self.draw_squares(surface)

    # Yay
    def draw_squares(self, surface):
        def get_alphacol(col):
            ALPHACOLS = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
            return ALPHACOLS[col]

        theme = self.config.themes[0]  # green theme...
        for row in range(ROWS):
            for col in range(COLS):
                # Color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # Rect
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                # Blit

                pygame.draw.rect(surface, color, rect)
                # Row coordinates (chess notation board labels by ranks)
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(str(ROWS - row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    # blit
                    surface.blit(lbl, lbl_pos)
                # Column coordinates (chess notation board labels by files)
                if row == 7:
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # label
                    lbl = self.config.font.render(get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, BOARD_HEIGHT - 20)
                    # blit
                    surface.blit(lbl, lbl_pos)
        new_rect = (800, 0, 200, 800)
        pygame.draw.rect(surface, (255, 255, 255), new_rect)

    # TODO: Fix pieces to ensure that they reflect numberboard.
    def create_texture(
        self, color, name, size=80
    ) -> str:  # takes in string arguments of piece color and piece name,
        # returns images from assets folder.
        return os.path.join(f"assets/images/imgs-{size}px/{color}_{name}.png")

    def show_pieces(self, surface) -> None:
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.piece_at((row, col)) != 0:
                    piece = self.board.piece_at((row, col))
                    # Iterating through all the possible pieces and passing arguments through create_texture() without a huge if/else jungle
                    pieces_list = [
                        "empty",
                        "pawn",
                        "knight",
                        "bishop",
                        "rook",
                        "queen",
                        "king",
                    ]
                    texture = self.create_texture(
                        "white" if piece > 0 else "black", pieces_list[abs(piece)]
                    )
                    # Loading piece image and blitting it.
                    image = pygame.image.load(texture)
                    img_center = (
                        col * SQSIZE + SQSIZE // 2,
                        row * SQSIZE + SQSIZE // 2,
                    )
                    texture_rect = image.get_rect(center=img_center)
                    surface.blit(image, texture_rect)

    def update_board(self, surface):
        self.draw_board(surface)

    def draw_board(self, surface) -> None:
        empty = (255, 255, 255)  # The last 0 indicates 0 alpha, a transparent color
        surface.fill(empty)
        self.draw_squares(surface)
        self.show_pieces(surface)

import pygame

from chesskers import Board
from display import Display
from constants import *

pygame.init()

class Main:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((800, 800))
        self.display = Display(self.screen)
        self.board = self.display.board
        print(self.board.squares)
        self.display.draw_board(self.screen)
        self.board = Board()
        self.turns_played = 0
   
   # TODO: Refactor displaying pieces as large temporarily. 
    def __step__(self, surface, start, end): # Start and end are tuples (row, col) of board squares. 
        piece = self.board.piece_at(start)
        start_row, start_col = start
        final_row, final_col = end

        # Drawing image of piece being moved larger to show it being 
        piece.set_texture(size=128)
        img = pygame.image.load(piece.texture)
        img_center = (
            start_col * SQ_SIZE + SQ_SIZE // 2,
                            start_row * SQ_SIZE + SQ_SIZE // 2,
                        )
        piece.texture_rect = img.get_rect(center=img_center)
        surface.blit(img, piece.texture_rect)

        # Performing step on numberboard
        self.board.squares[start_row][start_col] = 0
        self.board.squares[final_row][final_col] = piece

        # Redrawing the pieces of updated numberboard. 
        self.display.show_pieces(surface)
        
    def __jump__(self, surface, start, taken, end): # Start and end are tuples (row, col) of board squares. 
        piece = self.board.piece_at(start)
        start_row, start_col = start
        final_row, final_col = end
        taken_row, taken_col = taken

        # Drawing image of piece being moved larger to show it being 
        piece.set_texture(size=128)
        img = pygame.image.load(piece.texture)
        img_center = (
                        start_col * SQ_SIZE + SQ_SIZE // 2,
                            start_row * SQ_SIZE + SQ_SIZE // 2,
                        )
        piece.texture_rect = img.get_rect(center=img_center)
        surface.blit(img, piece.texture_rect)

        # Growing and shrinking piece being taken (on square taken)
        piece.set_texture(size=128)
        img = pygame.image.load(piece.texture)
        img_center = (
                        taken_col * SQ_SIZE + SQ_SIZE // 2,
                            taken_row * SQ_SIZE + SQ_SIZE // 2,
                        )
        piece.texture_rect = img.get_rect(center=img_center)
        surface.blit(img, piece.texture_rect)

        # Performing jump on numberboard
        self.board.squares[start_row][start_col] = 0
        self.board.squares[taken_row][taken_col] = 0
        self.board.squares[final_row][final_col] = piece

        # Redrawing the pieces of updated numberboard. 
        self.display.show_pieces(surface)

    # This method needs to check and make sure 
    def __move__(self, surface):
        boardUCN = input("Enter a move please")
        # Setting up column dictionary to be able to utilize UCN properties. 
        col_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        # Using UCN properties to determine starting and ending row(s) and column(s) of the move
        # First character of UCN = letter for first column of piece as shown by col_dict above
        # Second character of UCN = number (in string form) for first row of piece 
        # Second to last character of UCN = letter for final column of piece as shown by col_dict above
        # Last character of UCN = number (in string form) for final row of piece
        start_row = HEIGHT//SQ_SIZE - int(boardUCN[1]) 
        start_col = int(col_dict[boardUCN[0]])
        final_row = HEIGHT//SQ_SIZE - int(boardUCN[len(boardUCN) - 1])
        final_col = int(col_dict[boardUCN[len(boardUCN) - 2]])
        if boardUCN.__contains__("t"):
            taken_row = HEIGHT//SQ_SIZE - int(boardUCN[3])
            taken_col = int(col_dict[boardUCN[2]])
            taken = (taken_row, taken_col)
        
        # Tuple declarations for start and end. 
        start = (start_row, start_col)
        end = (final_row, final_col)

        # Jumping or stepping depending on whether or not the UCN contains a t (t is for taking a piece in which case a jump must occur). 
        self.__jump__(surface, start, taken, end) if boardUCN.__contains__("t") else self.__step__(surface, start, end)
        
        # Incrementing the turn counter
        self.turns_played += 1

    def main_loop(self):
        pygame.init()
        while True:
            row, col = pygame.mouse.get_pos()
            row //= SQ_SIZE
            col //= SQ_SIZE

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__move__(self.screen)
            self.display.draw_board(self.screen)
            pygame.display.update()

    def pve(self, surface) -> None:
        _ = pygame.init()
        while True:
            self.display.draw_board(surface)
            move = self.board.from_UCN(input("")) 
            print(move)
            self.board.do_move(move)
            print(self.board)
            self.display.update_board(surface)
            



main = Main()
main.main_loop()
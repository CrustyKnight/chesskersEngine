import pygame

from chesskers import Board
from chesskers import Square

from display import Display
from constants import *
import re

def is_ucn(move: str) -> bool:
    return True

class Main:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.display = Display(self.screen)
        self.display.draw_board(self.screen)
        self.board = Board()
        self.display.board = self.board
        print(self.board.squares)
        self.turns_played = 0

    def __step__(self, surface, start: Square):  
        pass

    def __jump__(self, surface, start: Square):  
        pass

    # This method needs to execute the user's move on the screen. 
    def __move__(self, surface) -> None | str: # (row, col) is the start square of the move
        # Getting user input and finding the piece
        user_UCN = input("Where would you like to move this piece? Enter your move in UCN Enter 'no' if you don't want to move it.\n")
        # Checking that the user did enter UCN
        if not is_ucn(user_UCN):
            return print("Please give a valid UCN next time!")
        # col_dict to use to convert UCN purely into useful numbers 
        col_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        
        # Using UCN properties to determine starting and ending row(s) and column(s) of the move
        # First character of UCN = letter for first column of piece as shown by col_dict above
        # Second character of UCN = number (in string form) for first row of piece
        # Second to last character of UCN = letter for final column of piece as shown by col_dict above
        # Last character of UCN = number (in string form) for final row of piece
        start_row = ROWS - int(user_UCN[1])
        start_col = col_dict[user_UCN[0]]
        final_row = ROWS - int(user_UCN[len(user_UCN) - 1])
        final_col = col_dict[user_UCN[len(user_UCN) - 2]] 
        if user_UCN.__contains__("t"):
            taken_row = ROWS - int(user_UCN[4])
            taken_col = col_dict[user_UCN[3]]
            taken: Square = (taken_row, taken_col)

        # Getting squares into tuples to enter into check_valid_step and check_valid_jump methods
        start: Square = (start_row, start_col)
        final: Square = (final_row, final_col)
        piece = self.board.piece_at(start)

        if taken == None:
            is_valid_move = self.board.check_valid_step(start, final)
        else:
            self.board.squares[taken_row][taken_col] = 0
            is_valid_move = self.board.check_valid_jump(start, taken, final)

        if not is_valid_move:
            return None
        
        # Now that the move has been confirmed to be valid up to this point, the move itself is executed on the GUI board
        self.board.squares[start_row][start_col] = 0
        self.board.squares[final_row][final_col] = piece
        self.display.draw_board(surface)
        

        # Using check_valid_step() and check_valid_jump() to ensure that user has entered a valid move w/o using live move generation 
        # This is done to prevent lagging (we know live move generation and comparing every possible move with the board )
        return print("yay")

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
                    pass
                    #TODO: implement move. 
            self.display.draw_board(self.screen)
            pygame.display.update()

    def pve(self, surface) -> None:
        _ = pygame.init()
        self.display.draw_board(self.screen)
        pygame.display.update()
        while True:
            self.display.draw_board(self.screen)
            move = self.board.from_UCN(input(""))
            print(move)
            print("COLOR: white") if self.display.board.color == 1 else print("COLOR: black")
            self.display.board.push(move)
            print(self.display.board)
            self.display.draw_board(self.screen)
            pygame.display.update()

def script() -> str:
        text = input("Please enter a number between 1 and 10")
        return text

# script()
# Yay

main = Main()
main.pve()

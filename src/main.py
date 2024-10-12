import pygame

from chesskers import Board
from display import Display

pygame.init()

class Main:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((800, 800))
        self.display = Display(self.screen)
        self.board = self.display.board
        print(self.board.squares)
        self.display.draw_board(self.screen)
        self.board = Board()

    # This method needs to check and make sure 
    def __move__(self):
        move = input("Enter your move now")
        self.board.from_UCN(move)
        # Recalling the dictionary for different files (a, b, c) by converting them to row. 
        col_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        # Using move properties to discern row and col of the start and 
        start_row = col_dict[move[0]]
        start_col

    def main_loop(self):
        pygame.init()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__move__()
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
main.pve()
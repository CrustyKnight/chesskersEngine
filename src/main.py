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
    

    def __move__(self):
        move = input("Enter your move now")
        

    def mainloop(self):
        _ = pygame.init()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.display.draw_board(self.screen)
            pygame.display.update()

    def pve(self) -> None:
        _ = pygame.init()
        while True:
            move = self.board.from_UCN(input("")) 
            print(move)
            self.board.do_move(move)
            print(self.board)
            



main = Main()
main.pve()

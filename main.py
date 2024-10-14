import pygame

from display import Display
import re

pygame.init()


def is_ucn(move: str) -> bool:
    return re.search(r"([a-h][1-8]){2}|(([a-h][1-8]){2}t[a-h][1-8]\\|?)+", move) != None


class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 800))
        self.display = Display(self.screen)
        self.board = self.display.board
        print(self.board.squares)
        self.display.draw_board(self.screen)

    def main_loop(self):
        pygame.init()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.display.draw_board(self.screen)
            pygame.display.update()


main = Main()
main.main_loop()

import pygame

from display import Display

pygame.init()

class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 800))
        self.display = Display(self.screen)
        self.board = self.display.board
        print(self.board.squares)
        self.display.draw_board(self.screen)

    def __move__(self):
        move = input("Enter your move now")
        

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

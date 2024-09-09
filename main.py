import pygame

from display import Display

class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 800))
        self.display = Display(self.screen)
    
    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.display.draw_board(self.screen)

main = Main()
main.main_loop()
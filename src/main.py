import pygame
from time import sleep

from chesskers import Board
from chesskers import Square

from display import Display
from constants import *

from bot import find_best_move
from bot import alphabeta
from bot import transposition_table

import re


def is_ucn(move: str) -> bool:
    return True


class Main:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.display = Display(self.screen)
        self.display.draw_board(self.screen)
        self.board = self.display.board
        print(self.board.squares)
        self.turns_played = 0

    # This method needs to execute the user's move on the screen.
    def __move__(
        self, surface
    ) -> None | str:  # (row, col) is the start square of the move
        # Getting user input and finding the piece
        user_UCN = input(
            "Where would you like to move this piece? Enter your move in UCN Enter 'no' if you don't want to move it.\n"
        )
        move = self.display.board.from_UCN(user_UCN)
        print("MOVE: " + self.display.board.to_UCN(move))
        if move == None or (self.board.color == 1 and self.turns_played %2 == 1) or (self.board.color == 0 and self.turns_played %2 == 0):
            return "Invalid move"
        if self.board.is_jump(move):
            for m in move:
                self.display.board.do_jump(m)
                self.display.draw_board(self.screen)
                pygame.display.update()
                sleep(0.5)
        else:
            self.display.board.push(move)
            self.display.draw_board(surface)
        self.turns_played += 1
        pygame.display.update()
        return None

    def main_loop(self):
        _ = pygame.init()
        while True:
            row, col = pygame.mouse.get_pos()
            row //= SQ_SIZE
            col //= SQ_SIZE

            # 2
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__move__(self.screen)
                    # TODO: implement move.
            self.display.draw_board(self.screen)
            pygame.display.update()

    def pve(self) -> None:
        def update_display():
            self.display.draw_board(self.screen)
            pygame.display.update()

        _ = pygame.init()
        self.display.draw_board(self.screen)
        pygame.display.update()
        while True:
            self.display.draw_board(self.screen)
            prompt = input("")
            if prompt == "transtable":
                print(transposition_table)
            else:
                move = self.display.board.from_UCN(prompt)
                print("MOVE: " + self.display.board.to_UCN(move))
                self.display.board.push(move)
                update_display()

            eval = find_best_move(self.display.board, depth=2)
            bot_move, bot_score = eval

            # if self.display.board.is_jump(bot_move):
            if self.display.board.is_jump(bot_move):
                for m in bot_move:
                    self.display.board.do_jump(m)
                    update_display()
                    sleep(0.5)
                self.display.board.turns += 1
                self.display.board.color *= -1
                self.display.board.moves = self.display.board.calc_moves(
                    self.display.board.color
                )

            else:
                self.display.board.push(bot_move)
            print("BOT MOVE: " + self.display.board.to_UCN(bot_move))
            print("BOT EVALUATION: " + str(bot_score))
            update_display()
            print(self.display.board)

            if self.display.board.game_over():
                print("GAME IS OVER")
                break


def script() -> str:
    text = input("Please enter a number between 1 and 10")
    return text


# script()
# Yay

main = Main()
main.main_loop()

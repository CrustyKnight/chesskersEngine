#!/usr/bin/env python3

class Board:

# TODO: Implement moves

    def __init__(self, board, fen=False):
        if fen:
            self.squares = self.from_fen_string(board)
        else:
            self.squares = self.from_string(board)
#         self.squares = [[]]
#         self.from_string("""\
# put other data here
# r n b q k b n r
# p p p p p p p p
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# . . . . . . . .
# P P P P P P P P
# R N B Q K B N R
#         """)
        self.moves = self.calc_moves()

    def from_fen_string(self, string):
        pass

    def from_string(self, string):
        # Also want information pertaining to en passant squares, turn number, etc
        counter = 0
        d = {
            ".": 0,
            "P": 1,
            "N": 2,
            "B": 3,
            "R": 4,
            "Q": 5,
            "K": 6,
            "k": -6,
            "q": -5,
            "r": -4,
            "b": -3,
            "n": -2,
            "p": -1
        }
        data_line = string.split('\n', 1)[0]
        # data_line format wc,bc,ep,tn
        # C for can, N no castle.
        # ep is of form RCR'C' where R is a number indicating row, C is number indicating column
        #   R' and C' are the same.
        #   RC indicated square is one that can be taken over
        #   R'C' square is the one the pawn that will be removed is
        # tn is an int representing turn number (even numbers mean its blacks turn, odd means its whites)
        #   starts at 1
        string = string.split('\n', 1)[1]
        for token in string.split():
            x = counter % 8
            y = counter // 8
            self.squares[y][x] = d[token]
            counter += 1

    def __str__(self):
        d = {
            0: ".",
            1: "P",
            2: "N",
            3: "B",
            4: "R",
            5: "Q",
            6: "K",
            -6: "k",
            -5: "q",
            -4: "r",
            -3: "b",
            -2: "n",
            -1: "p"
        }

        for row in self.squares:
            for piece in row:
                print(d[piece] + " ")
            print("\n")

    def piece_at(self, row, col):
        return self.squares[row][col]

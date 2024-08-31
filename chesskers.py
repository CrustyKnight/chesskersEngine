#!/usr/bin/env python3
from bot import find_best_move


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
            "p": -1,
        }
        data_line = string.split("\n", 1)[0]
        # data_line format wc,bc,ep,tn
        # C for can, N no castle.
        # ep is of form RCR'C' where R is a number indicating row, C is number indicating column
        #   R' and C' are the same.
        #   RC indicated square is one that can be taken over
        #   R'C' square is the one the pawn that will be removed is
        # tn is an int representing turn number (even numbers mean its blacks turn, odd means its whites)
        #   starts at 1
        string = string.split("\n", 1)[1]
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
            -1: "p",
        }

        for row in self.squares:
            for piece in row:
                print(d[piece] + " ")
            print("\n")

    def piece_at(self, square):
        row, col = square
        return self.squares[row][col]

    def check_valid_step_and_jump( #This function is used to VALIDATE moves, not generate them. 
        self, start, end
    ):  # start and end are tuples of 2 elements: (row, col):
        start_row, start_col = start
        piece = self.piece_at(
            start_row, start_col
        )  # this piece will be used for jump move calculations (see jump moves below)
        final_row, final_col = end

        # In chesskers, we broke up moves into 2 types: steps and jumps.
        # steps are described as normal chess moves, which occur when pieces move from their current square to an empty square.
        # jumps are described as the 'checkers' part of chesskers, where the pieces take a piece, move an extra square in the direction they took the piece, and can ...
        # ... continue taking pieces if they are 'in range' of the piece, like how a checkers piece which takes an opponent piece becomes the only piece that can be moved...
        # ... that too only if there are pieces to take ... otherwise the 'jumping' and player's turn end.

        # Step functions
        def check_pawn_step():
            boolean = True
            if self.piece_at((start_row, start_col)) == -1: # checking for black pawn
                if(start_row == 1):
                    boolean = final_row - start_row == 2
                return boolean or final_row - start_row == 1 # Returning True if it can move 1 square or 2 squares (black moves DOWN the board)
            elif self.piece_at((start_row, start_col)) == 1: # checking for white pawn
                if start_row == 6:
                    boolean = final_row - start_row == -2
                return boolean or final_row - start_row == -1 # Returning True if it can move 1 square or 2 squares (white moves UP the board)

        def check_knight_step():
            if (
                final_row < 0 or final_col < 0 or final_row > 7 or final_col > 7
            ):  # Checks for out of bounds board error (as in a step, knights move like they would in chess)
                return False
            elif (
                self.squares[final_row][final_col] != 0
            ):  # Checks that the final square of the move is indeed empty (taking pieces is a 'jump', not a 'step')
                return False
            elif (
                (abs(final_row - start_row)) == 2 and abs(final_col - start_col) == 1
            ) or (
                (abs(final_row - start_row)) == 1 and abs(final_col - start_col) == 2
            ):
                return True  # Checks that the knight moved in an appropriate 'L' shape.
            else:
                return False

        def check_bishop_step():
            if (
                final_row < 0 or final_col < 0 or final_row > 7 or final_col > 7
            ):  # Checks for out of bounds board error (as in a step, bishops move like they would in chess)
                return False
            elif (
                self.squares[final_row][final_col] != 0
            ):  # Checks that the final square of the move is indeed empty (taking pieces is a 'jump', not a 'step')
                return False
            horizontal_distance = final_col - start_col
            vertical_distance = final_row - start_row
            if abs(vertical_distance) == abs(
                horizontal_distance
            ):  # Setting up variables to be used in iteration below, which checks for obstruction between starting and ending squares
                horizontal_increment = abs(horizontal_distance) / horizontal_distance
                vertical_increment = abs(vertical_distance) / vertical_distance
                col = start_col
                for row in range(
                    start_row + vertical_increment, final_row, vertical_increment
                ):
                    col += horizontal_increment  # Iterating through squares in between the piece's starting and destination squares to check that bishop isn't obstructed
                    if self.squares[row][col] != 0:
                        return False
                    if row == final_row - vertical_increment:
                        return True
            else:
                return False

        def check_rook_step():
            if (
                final_row < 0 or final_col < 0 or final_row > 7 or final_col > 7
            ):  # Checks for out of bounds board error (as in a step, rooks move like they would in chess)
                return False
            elif (
                self.squares[final_row][final_col] != 0
            ):  # Checks that the final square of the move is indeed empty (taking pieces is a 'jump', not a 'step')
                return False
            if (abs(final_row - start_row) > 0 and final_col - start_col == 0) or (
                abs(final_col - start_col) > 0 and final_row - start_row == 0
            ):
                if (final_col - start_col == 0) and (final_row - start_row != 0):
                    distance = final_row - start_row
                    move_start = start_row  # Setting up variables to be used in iteration below, which checks for obstruction between vertical starting and ending squares
                    move_end = final_row
                elif (final_col - start_col != 0) and (final_row - start_row == 0):
                    distance = final_col - start_col
                    move_start = start_col
                    move_end = final_col  # Setting up variables to be used in iteration below, which checks for obstruction between horizontal starting and ending squares
                increment = abs(distance) / distance
                for n in range(move_start + increment, move_end, increment):
                    if final_col - start_col == 0:
                        if self.squares[n][start_col] == 0:
                            return False  # Iterating through squares in between the piece's starting and destination squares to check that rook isn't obstructed
                    elif final_row - start_row == 0:
                        if self.squares[start_row][n] == 0:
                            return False
                    elif n == move_end - increment:
                        return True
            else:
                return False

        def check_queen_step():  # Queens are bishops and rooks in one piece, so combining both their step methods tells us the queen's possible steps
            return check_bishop_step() or check_rook_step()
        
        def check_king_step(): # Checks that the king moves 1 square in any direction, but does not stay still...
            return abs(final_col - start_col) <= 1 and abs(final_row - start_row) <= 1 and not(final_col - start_col == 0 and final_row - start_row == 0)

        # Jump functions
        def check_pawn_jump(): # pawns always jump such that they move 2 columns and 2 rows (up, left or up right relative to the direction they move)
            if abs(final_col - start_col) == 2:    
                hd = abs(final_col - start_col)/(final_col - start_col) # Horizontal direction (+-1, used to check square being 'taken' over)
                if self.piece_at(((start_row + final_row)/2, (start_col + hd))) != 0: # Checking that the pawn is indeed taking a piece
                    if self.piece_at((start_row, start_col)) == -1 : # Checking and defining movement for black pawns
                            if (final_row - start_row == 2):
                                return True
                    elif self.piece_at((start_row, start_col)) == 1: # Checking and defining movement for white pawns
                        if self.piece_at((start_row, start_col)) == 1: 
                            if(final_row - start_row == -2):
                                return True
            return False
        
        #TODO: Finish knight jump, bishop jump, rook jump, queen jump, and king jump. 
        
        def check_knight_jump(): # knight jumps either result in a 3 x 1 sqauare 'L' shape or in a 2 x 2 square 'L' shape. 
            pass

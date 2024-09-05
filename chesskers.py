#!/usr/bin/env python3
from bot import find_best_move


class Board:

    # TODO: Implement moves
    # TODO: Test and debug step and jump functions

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

    # In chesskers, we define moves as having 2 types: steps and jumps
    # A step is when a piece moves to an empty square, in which case it moves like a normal chess piece
    # A jump is defined as when a piece takes a piece, upon which it must land on a 'consecutive' empty square.
    # Jumps are like checkers piece takes: like how checker pieces must jump over the pieces they take,
    # and like how checkers pieces can only land on a certain square (which must be empty) after jumping over the taken piece.
    # If this 'consecutive' empty square is not empty, then the piece cannot be taken.
    # Jumps are illustrated and described in further detail in our planning guide pdf.

    def check_valid_step(  # This function is used to VALIDATE steps, ie non-piece-taking moves
        self, start, end
    ):  # start and end are tuples of 2 elements: (row, col):
        start_row, start_col = start
        final_row, final_col = end
        piece = self.piece_at(
            start
        )  # this piece will be checked in value to ensure it is the correct type, by looking at points.
        final_square_empty = (
            self.piece_at(end) == 0
        )  # This boolean will be used to check that none of these moves involve taking a
        # piece, since taking a piece is a jump.

        # Returning false if a piece moves off the board, since they cannot do so during a step.
        # Out of bounds error.
        if final_row < 0 or final_row > 8 or final_col < 0 or final_col > 8:
            return False

        # Returning false if piece is not moving (final row = start row && final col = start col)
        if final_row - start_row == 0 and final_col - start_col == 0:
            return False

        # Returning false if there is no piece or if a piece on the final square: that would make the move a jump, NOT a step.
        if piece == 0 or not (final_square_empty):
            return False

        # Step functions of individual pieces
        def check_pawn_step():
            if piece == 1:  # Checking for piece being white pawn
                if start_row == 6:  # White pawns move up the board.
                    return (final_row - start_row == -2) or (
                        final_row - start_row == -1
                    )  # Check if pawn can move 2 squares
                return (
                    final_row - start_row
                ) == -1  # Pawns can move 2 squares if they are on starting square
                # Else only check if the pawn is moving 1 square forward
            else:
                if start_row == 1:
                    return (final_row - start_row == 2) or (
                        final_row - start_row == 1
                    )  # Black pawns move down the board.
                return (final_row - start_row) == 1

        def check_knight_step():  # Checks that the knight is indeed moving in a 2 x 1 'L' shape.
            return (
                (abs(final_row - start_row)) == 2 and abs(final_col - start_col) == 1
            ) or ((abs(final_row - start_row)) == 1 and abs(final_col - start_col) == 2)

        def check_bishop_step():
            return abs(final_row - start_row) == abs(
                final_col - start_col
            )  # Bishops move diagnally, or the same number of rows/columns.

        def check_rook_step():  # Rooks move laterally, either only horizontal or only vertical. They don't have both forms of movement.
            return (final_row - start_row != 0 and final_col - start_col == 0) or (
                final_row - start_row == 0 and final_col - start_col != 0
            )

        def check_queen_step():
            return (
                check_bishop_step() or check_rook_step()
            )  # Queens move like bishops OR rooks

        def check_king_step():  # Checks that the king is moving 1 square in ANY diretion. Not moving has already been checked before
            # starting the step functions of individual pieces.
            return (-1 <= final_col - start_col <= 1) or (
                -1 <= final_row - start_row <= 1
            )

        # Performing functions based on what type of piece the piece is (1 = pawn, 2 = knight, 3 = bishop, 4 = rook, 5 = Queen, 6 = King)
        if abs(piece) == 1:
            check_pawn_step()
        elif abs(piece) == 2:
            check_knight_step()
        elif abs(piece) == 3:
            check_bishop_step()
        elif abs(piece) == 4:
            check_rook_step()
        elif abs(piece) == 5:
            check_queen_step()
        else:
            check_king_step()

    def check_valid_jump(  # This function is used to VALIDATE jumps, ie piece-taking moves/captures
        self, start, end, isFirstJumpOverall = True
    ):  # start and end are tuples of 2 elements: (row, col):
        start_row, start_col = start
        final_row, final_col = end
        piece = self.piece_at(
            start
        )  # this piece will be checked in value to ensure it is the correct type, by looking at points.

        # Vertical and horizontal distance travelled (used with vd and hd below to compute coordinates of square of piece being taken)
        vertical_distance = final_row - start_row
        horizontal_distance = final_col - start_col

        # Vertical and horizontal direction (+- 1) of the piece: Used to check that it can move in that direction
        vd = abs(vertical_distance) / (vertical_distance)  # Vertical direction
        hd = abs(horizontal_distance) / (horizontal_distance)  # Horizontal direction

        # Returning false if piece is not moving (final row = start row && final col = start col)
        if final_row - start_row == 0 and final_col - start_col == 0:
            return False
        
        # Returning false if end square is not empty: 
        if self.piece_at(end) != 0:
            return False
        
        # checking out of bounds: now pieces can take over the edge and teleport to the other side of the board...
        def fix_piece_location(): # We might need this function to further account for edge effects, especially if they 
                                    # have only been accounted for in imagination. Maybe we won't need it in this function. 
                                    # but we will certainly NEED THIS FUNCTION IN MOVE GENERATION
                                    # TODO: Implement this function into move generation...
            if final_col == 8:
                final_col == 0
            elif final_col == -1:
                final_col = 7
            if final_row == 8:
                final_row = 0
            elif final_row == -1:
                final_row = 7
            if not (0 <= final_row <= 7 and 0 <= final_col <= 7):
                return False

        # Jump functions of individual pieces
        def check_pawn_jump():
            if abs(vertical_distance) == abs(horizontal_distance) == 2:
                if piece == 1:  # White pawn jump
                    if (
                        vertical_distance > 0
                    ):  # White pawns travel UP the board, NOT DOWN the board.
                        return False
                else:
                    if (
                        vertical_distance < 0
                    ):  # Black pawns travel DOWN the board, NOT UP the board.
                        return False
                taken_piece = (
                    start_row + vertical_distance - vd,
                    start_col + horizontal_distance - hd,
                )  # Determining square where piece is taken.
                return (
                    self.piece_at(taken_piece) != 0
                )  # Returning True if a piece is being taken, otherwise return False.
            return False

        def check_knight_jump():
            if ( # Checking for various possible 'L' shapes.
                (abs(vertical_distance) == abs(horizontal_distance) == 2)
                or (abs(horizontal_distance) == 3 and abs(vertical_distance == 1))
                or (abs(vertical_distance) == 3 and abs(horizontal_distance == 1))
            ):  
                # Confirming that a piece is indeed taken (on a square in an otherwise step location) to do the 2 x 2 'L' jump
                return (
                    self.piece_at(
                        (
                            start_row + vertical_distance,
                            start_col + horizontal_distance - hd,
                        )
                    )
                    != 0
                    or self.piece_at(
                        (
                            start_row + vertical_distance - vd,
                            start_col + horizontal_distance,
                        )
                    )
                    != 0
                ) 
            return False

        def check_bishop_jump(isFirstJump = isFirstJumpOverall):
            if isFirstJump: # bishop has no limit on how far it can go before taking a piece
                return self.piece_at((start_row + vertical_distance - vd, start_col + horizontal_distance - hd)) != 0
            else: # Setting a square of 1 as the 'take piece' radius. Bishops move diagonally, like checkers queens. 
                if abs(horizontal_distance) == abs(vertical_distance) == 2:
                    return self.piece_at((start_row + vertical_distance - vd, start_col + horizontal_distance - hd)) != 0
            return False

        def check_rook_jump(isFirstJump = isFirstJumpOverall):
            if isFirstJump: # rook also has no limit on how far it can go before taking a piece 
                if vertical_distance == 0:
                    return self.piece_at((start_row, start_col + horizontal_distance - hd)) != 0
                elif horizontal_distance == 0:
                    return self.piece_at((start_row + vertical_distance - vd, start_col)) != 0
            else: # Sets a taking radius of 1 square on the rook: it jumps over pieces and takes laterally. 
                if abs(horizontal_distance) == 2 and vertical_distance == 0:
                    return self.piece_at(start_row, start_col + horizontal_distance - hd) != 0
                elif abs(vertical_distance) == 2 and horizontal_distance == 0:
                    return self.piece_at((start_row + vertical_distance - vd, start_col)) != 0
            return False

        def check_queen_jump(isFirstJump = isFirstJumpOverall):
            if isFirstJump: # Queen also has no limit on how far it can go before taking a piece 
                return check_rook_jump() or check_bishop_jump()
            else:# Sets a taking radius of 1 square on the queen: it jumps over pieces and takes laterally.
                return check_rook_jump(isFirstJump=False) or check_bishop_jump(isFirstJump=False)
            # TODO: implement queen's limitations if this doesn't work...queens can move like Rooks OR Bishops, not like both in 1 turn

        def check_king_jump():
            if abs(horizontal_distance) == 2 or abs(vertical_distance) == 2:
                # Checking all squares around like a rook AND Bishop in a 1 square diagonal, since kings can take in any direction when they're on a spree
                return self.piece_at((start_row + vertical_distance - vd, start_col)) != 0 or self.piece_at(start_row, start_col + horizontal_distance - hd) != 0 or self.piece_at((start_row + vertical_distance - vd, start_col + horizontal_distance - hd)) != 0 
        
        # Performing functions based on what type of piece the piece is (1 = pawn, 2 = knight, 3 = bishop, 4 = rook, 5 = Queen, 6 = King)
        if abs(piece) == 1:
            check_pawn_jump()
        elif abs(piece) == 2:
            check_knight_jump()
        elif abs(piece) == 3:
            check_bishop_jump()
        elif abs(piece) == 4:
            check_rook_jump()
        elif abs(piece) == 5:
            check_queen_jump()
        else:
            check_king_jump()

    def is_step(self, move):
        if len(move[0]) == 2:
            return True

        return False

    def is_jump(self, move):
        if len(move[0]) == 3:
            return True

        return False 

    def from_UCN(self, move):
        # move notation: e2e6te8

        if self.is_step(move):
           pass 

            

# TODO: implement actual move generation and use these functions to check. 

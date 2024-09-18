#!/usr/bin/env python3
from bot import find_best_move
from bot import val_map

from bot import val_map
# yay


class Board:

    # TODO: Implement moves
    # TODO: Test and debug step and jump functions

    def __init__(
        self,
        fen=False,
        board="""other info for the board state (en-passant, etc.)
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . . 
. . . . . . . .
P P P P P P P P
R N B Q K B N R
""",
    ):
        self.squares = [[0 for i in range(8)] for i in range(8)]
        if fen:
            self.squares = self.from_fen_string(board)
        elif board:
            self.from_string(board)
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
        # self.moves = self.calc_moves()

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

        ret = ""

        for row in self.squares:
            for piece in row:
                ret += d[piece] + " "
            ret += "\n"

        return ret

    def print(self, guides=False):
        def to_ascii(piece):
            return [".", "P", "N", "B", "R", "Q", "K", "k", "q", "r", "b", "n", "p"][
                piece
            ]

        rows = ["8", "7", "6", "5", "4", "3", "2", "1"]
        cols_header = "  a b c d e f g h\n +----------------"

        y = 0
        if guides:
            print(cols_header)
        for row in self.squares:
            if guides:
                print(rows[y], end="|")
            for piece in row:
                print(to_ascii(piece), end=" ")
            print("")
            y += 1

    def piece_at(self, square):
        (row, col) = square
        if self.squares[row][col] != 0:
            return self.squares[row][col]
        else:
            return 0

    # boolean that returns whether or not a given move is legal
    # no need for stuff like pseudo-legality because there isn't check in this game
    def legal_move(self, move):
        return True if move in self.legal_moves else False

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
        self, start, end, isFirstJumpOverall=True
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
        def fix_piece_location():  # We might need this function to further account for edge effects, especially if they
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
            if (  # Checking for various possible 'L' shapes.
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

        def check_bishop_jump(isFirstJump=isFirstJumpOverall):
            if (
                isFirstJump
            ):  # bishop has no limit on how far it can go before taking a piece
                return (
                    self.piece_at(
                        (
                            start_row + vertical_distance - vd,
                            start_col + horizontal_distance - hd,
                        )
                    )
                    != 0
                )
            else:  # Setting a square of 1 as the 'take piece' radius. Bishops move diagonally, like checkers queens.
                if abs(horizontal_distance) == abs(vertical_distance) == 2:
                    return (
                        self.piece_at(
                            (
                                start_row + vertical_distance - vd,
                                start_col + horizontal_distance - hd,
                            )
                        )
                        != 0
                    )
            return False

        def check_rook_jump(isFirstJump=isFirstJumpOverall):
            if (
                isFirstJump
            ):  # rook also has no limit on how far it can go before taking a piece
                if vertical_distance == 0:
                    return (
                        self.piece_at((start_row, start_col + horizontal_distance - hd))
                        != 0
                    )
                elif horizontal_distance == 0:
                    return (
                        self.piece_at((start_row + vertical_distance - vd, start_col))
                        != 0
                    )
            else:  # Sets a taking radius of 1 square on the rook: it jumps over pieces and takes laterally.
                if abs(horizontal_distance) == 2 and vertical_distance == 0:
                    return (
                        self.piece_at(start_row, start_col + horizontal_distance - hd)
                        != 0
                    )
                elif abs(vertical_distance) == 2 and horizontal_distance == 0:
                    return (
                        self.piece_at((start_row + vertical_distance - vd, start_col))
                        != 0
                    )
            return False

        def check_queen_jump(isFirstJump=isFirstJumpOverall):
            if (
                isFirstJump
            ):  # Queen also has no limit on how far it can go before taking a piece
                return check_rook_jump() or check_bishop_jump()
            else:  # Sets a taking radius of 1 square on the queen: it jumps over pieces and takes laterally.
                return check_rook_jump(isFirstJump=False) or check_bishop_jump(
                    isFirstJump=False
                )
            # TODO: implement queen's limitations if this doesn't work...queens can move like Rooks OR Bishops, not like both in 1 turn

        def check_king_jump():
            if abs(horizontal_distance) == 2 or abs(vertical_distance) == 2:
                # Checking all squares around like a rook AND Bishop in a 1 square diagonal, since kings can take in any direction when they're on a spree
                return (
                    self.piece_at((start_row + vertical_distance - vd, start_col)) != 0
                    or self.piece_at(start_row, start_col + horizontal_distance - hd)
                    != 0
                    or self.piece_at(
                        (
                            start_row + vertical_distance - vd,
                            start_col + horizontal_distance - hd,
                        )
                    )
                    != 0
                )

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

    # Universal Chesskers Notation
    def from_UCN(self, move):

        # for e4e5 and cases like that
        def parse_move(move):
            start = self.squares[val_map[move[0]]][int(move[1])]
            end = self.squares[val_map[move[2]]][int(move[3])]
            return [(start, end, end)]

        # move notation: e2e6te7
        #                e2e6
        #                e2e6te4|e4e5te7
        square_map = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}

        if "t" not in move:
            return parse_move(move)

        M = []
        subs = move.split("|")

        for m in subs:
            if "t" not in m:
                M.append(parse_move(m))

            else:
                # splitting in order to grab the 3 squares
                name = move.split("t")

                start = self.squares[val_map[name[0][0]]][int(name[0][1])]
                end = self.squares[val_map[name[0][2]]][int(name[0][3])]
                hop = self.squares[val_map[name[1][0]]][int(name[1][1])]

                M.append((start, end, hop))

        return M

    def calc_moves(self):
        pass

    def square_moves(self, square):
        p = self.piece_at(square)

    # Actual move generation done here for steps
    def square_steps(self, square):
        def direxp(direction):
            sqs = []
            sq = add_tuple(square, direction)
            while in_bounds(sq) and self.empty(sq):
                sqs.append(sq)
                sq = add_tuple(sq, direction)
            return sqs

        def in_bounds(square):
            r, c = square
            return 0 <= r < 8 and 0 <= c < 8

        def add_tuple(a, b):
            return (a[0] + b[0], a[1] + b[1])

        p = self.piece_at(square)

        def pawn():
            c = -1 if p < 0 else 1
            d = -c
            moves = [add_tuple(square, (d, 0))]
            # add thingy to tell if at start spot and add another move
            start_row = 6 if p == 1 else 1
            if square[0] == start_row:
                moves.append(add_tuple(square, (d * 2, 0)))
            return [mv for mv in moves if self.empty(mv) and in_bounds(mv)]

        def knight():
            moves = [
                (-1, 2),
                (-1, -2),
                (1, 2),
                (1, -2),
                (2, 1),
                (2, -1),
                (-2, 1),
                (-2, -1),
            ]
            moves = [add_tuple(square, m) for m in moves]
            moves = [m for m in moves if self.empty(m) and in_bounds(m)]
            # moves = [m for m in moves if self.check_valid_step(square, m)]
            return moves

        def bishop():
            moves = []
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            # travel in each direction until I hit a piece or the end of the board
            return [mv for d in directions for mv in direxp(d)]

        def rook():
            directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
            return [mv for d in directions for mv in direxp(d)]

        def queen():
            return bishop() + rook()

        def king():
            moves = [
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1),  # diag
                (1, 0),
                (-1, 0),
                (0, -1),
                (0, 1),
            ]  # straight
            return [m for m in moves if self.empty(m) and in_bounds(m)]

        return [lambda: [], pawn, knight, bishop, rook, queen, king][abs(p)]()

    # Actual move jump generation function.
    def square_jumps(self, square, ctx=None):
        # ctx is really just for the queen right now.
        # it will be a map { queen: ("diag"|"straight")}
        # maybe later it will just become a number (if efficiency matters super)
        def direxp(direction):
            # TODO mod this to give the location of the piece it hits, not all the squares before
            # and give nothing if it hits the edge
            sqs = []
            sq = add_tuple(square, direction)
            while in_bounds(sq) and self.empty(sq):
                sqs.append(sq)
                sq = add_tuple(sq, direction)
            return sqs

        def in_bounds(square):
            r, c = square
            return 0 <= r < 8 and 0 <= c < 8

        def add_tuple(a, b):
            return (a[0] + b[0], a[1] + b[1])

        def jump_direction(taken):
            # taken is the square of the taken piece
            def sign(num):
                return -1 if num < 0 else 0 if num == 0 else 1

            return (sign(taken[0] - square[0]), sign(taken[1] - square[1]))

        p = self.piece_at(square)

        def pawn():
            def add_dir(mv):
                return add_tuple(mv, jump_direction(mv))

            c = -1 if p < 0 else 1
            d = -c
            possible_pieces = [add_tuple(square, (d, 1)), add_tuple(square, (d, -1))]
            possible_pieces = [
                mv for mv in possible_pieces if in_bounds(mv) and not self.empty(mv)
            ]
            possible_pieces = [
                (mv, add_dir(mv))
                for mv in possible_pieces
                if in_bounds(add_dir(mv)) and self.empty(add_dir(mv))
            ]
            # TODO right now this won't allow taking around the edges. fix that
            # debangshu prob already handled something like this in the move checking. look there for inspo/stuff to can copy
            return possible_pieces

        def knight():
            def split_dir(direction):
                return [(direction[0], 0), (0, direction[1])]

            moves = [
                (-1, 2),
                (-1, -2),
                (1, 2),
                (1, -2),
                (2, 1),
                (2, -1),
                (-2, 1),
                (-2, -1),
            ]
            moves = [add_tuple(square, m) for m in moves]
            moves = [m for m in moves if in_bounds(m) and not self.empty(m)]
            new_moves = []
            for mv in moves:
                d = split_dir(jump_direction(mv))
                new_moves.append((mv, add_tuple(mv, d[0])))
                new_moves.append((mv, add_tuple(mv, d[1])))
            new_moves = [
                mv for mv in new_moves if in_bounds(mv[1]) and self.empty(mv[1])
            ]
            # taking over the edges again
            return new_moves

        if abs(p) == 1:
            return pawn()
        if abs(p) == 2:
            return knight()

    def empty(self, square):
        return 0 == self.piece_at(square)

#!/usr/bin/env python3
from bot import find_best_move
from bot import val_map


from typing import Literal, TypeAlias, override


Direction: TypeAlias = tuple[int, int]
Square: TypeAlias = tuple[int, int]
Piece: TypeAlias = Literal[0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5, -6, 6]
Step: TypeAlias = tuple[Square, Square]
Jump: TypeAlias = tuple[Square, Square, Square]
JumpMove: TypeAlias = list[Jump]
Move: TypeAlias = JumpMove | Step
QueenContext: TypeAlias = None | Literal["diag", "straight"]


# yay
# YAY


# For tracking en-passant:
# One way is to create a type of phantom piece that is created whenever a pawn moves 2 spaces, and deleted on all other moves.
# Might be a bit inefficent if you have to scan the board for the phantom piece after every full move.
# This could be alleviated by also keeping track of the position of it.
# The phantom piece just allows the jump generation to not have to worry about en-passant as an edge case.
# (It would be phantom by just having the same sprite as an empty square, or we could even visually indicate it with a litle pawn afterimage)
#  ^(afterimage) could be fun

# En-passant edge case to figure out.
# If a pawn moves 2 spaces, and then another pawn, which is not right next to them, does jumps such that it is now right next to them, can it do en-passant?
# e.g.
# r n b q k b n r |=> r n b q k b n r |=> r n b q k b n r |-> r n b q k b n r
# p . p p p p p p |=> p . . p p p p p |=> p . . p p p p p |-> p P . p p p p p
# . . . . . . . . |=> . . . . . . . . |=> . . . . . . . . |-> . . . . . . . .
# . . . . . . . . |=> . . p . . . . . |=> . . p P . . . . |-> . . . . . . . .
# . . . . p . . . |=> . . . . p . . . |=> . . . . . . . . |-> . . . . . . . .
# . . . . . P . . |=> . . . . . P . . |=> . . . . . . . . |-> . . . . . . . .
# P P P P P . P P |=> P P P P P P P P |=> P P P P P P P P |-> P P P P P P P P
# R N B Q K B N R |=> R N B Q K B N R |=> R N B Q K B N R |-> R N B Q K B N R
#
# where |=> means one full turn, and |-> means a submove


class Board:

    # TODO: Implement moves
    # TODO: Test and debug step and jump functions

    def __init__(
        self,
        fen: bool = False,
        board: str = """other info for the board state (en-passant, etc.)
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
        self.squares: list[list[Piece]]
        self.squares = [[0 for _ in range(8)] for _ in range(8)]
        if fen:
            self.squares = self.from_fen_string(board)
        elif board:
            self.from_string(board)

        self.legal_moves = self.calc_moves()
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

    def from_fen_string(self, string: str) -> list[list[Piece]]:
        pass
        # return [[0]]

    def from_string(self, string: str):
        # Also want information pertaining to en passant squares, turn number, etc
        counter = 0
        d: dict[str, Piece] = {
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

    @override
    def __str__(self):
        # TODO make sure this prints out the same format from_str takes in (right now it does not include the extra data line)
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

    def print(self, guides: bool = False):
        def to_ascii(piece: Piece) -> str:
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

    def piece_at(self, square: Square) -> Piece:
        (row, col) = square
        # Useless if statement?
        if self.squares[row][col] != 0:
            return self.squares[row][col]
        else:
            return 0

    # boolean that returns whether or not a given move is legal
    # no need for stuff like pseudo-legality because there isn't check in this game
    def legal_move(self, move: Move) -> bool:
        return True if move in self.legal_moves else False

    # In chesskers, we define moves as having 2 types: steps and jumps
    # A step is when a piece moves to an empty square, in which case it moves like a normal chess piece
    # A jump is defined as when a piece takes a piece, upon which it must land on a 'consecutive' empty square.
    # Jumps are like checkers piece takes: like how checker pieces must jump over the pieces they take,
    # and like how checkers pieces can only land on a certain square (which must be empty) after jumping over the taken piece.
    # If this 'consecutive' empty square is not empty, then the piece cannot be taken.
    # Jumps are illustrated and described in further detail in our planning guide pdf.

    def check_valid_step(  # This function is used to VALIDATE steps, ie non-piece-taking moves
        self, start: Square, end: Square
    ) -> bool:  # start and end are tuples of 2 elements: (row, col):
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
            return check_pawn_step()
        elif abs(piece) == 2:
            return check_knight_step()
        elif abs(piece) == 3:
            return check_bishop_step()
        elif abs(piece) == 4:
            return check_rook_step()
        elif abs(piece) == 5:
            return check_queen_step()
        else:
            return check_king_step()

    def check_valid_jump(  # This function is used to VALIDATE jumps, ie piece-taking moves/captures
        self, start: Square, end: Square, isFirstJumpOverall: bool = True
    ):  # start and end are tuples of 2 elements: (row, col):
        start_row, start_col = start
        final_row, final_col = end
        piece = self.piece_at(
            start
        )  # this piece will be checked in value to ensure it is the correct type, by looking at points.bindsym $mod+Shift+z

        # Vertical and horizontal distance travelled (used with vd and hd below to compute coordinates of square of piece being taken)
        vertical_distance = final_row - start_row
        horizontal_distance = final_col - start_col

        # Vertical and horizontal direction (+- 1) of the piece: Used to check that it can move in that direction
        def sign(x: int):
            return -1 if x < 0 else (0 if x == 0 else 1)

        vd = sign(vertical_distance)  # Vertical direction
        hd = sign(horizontal_distance)  # Horizontal direction
        # vd = abs(vertical_distance) / (vertical_distance)  # Vertical direction
        # hd = abs(horizontal_distance) / (horizontal_distance)  # Horizontal direction

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
                taken_piece: Square = (
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
                        self.piece_at((start_row, start_col + horizontal_distance - hd))
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
                    or self.piece_at((start_row, start_col + horizontal_distance - hd))
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

    def is_step(self, move: Move) -> bool:
        if len(move[0]) == 2:
            return True

        return False

    def is_jump(self, move: Move) -> bool:
        if len(move[0]) == 3:
            return True

        return False

    # Universal Chesskers Notation
    def from_UCN(self, move: str) -> Move:
        # This is bugged. I don't want to mess with it though.
        #   - Sam

        # Fixed hopefully
        #   - Cole

        # for e4e5 and cases like that
        def parse_step(move: str) -> Step:
            start = move[:2]
            end = move[2:] 

            s1 = square_map[start[0]]
            s2 = int(start[1])

            e1 = square_map[end[0]]
            e2 = square_map[end[0]] 
            return ((s1,s2), (e1,e2))

        def parse_jump(move: str) -> Jump:
            m = move.split("t")

            start = m[0][:2]
            s1 = square_map[start[0]]
            s2 = int(start[1])
            end = m[0][2:]
            e1 = square_map[end[0]]
            e2 = int(end[1])
            hop = m[1]
            h1 = square_map[hop[0]]
            h2 = int(hop[1])

            return ((s1,s2),(e1,e2),(h1,h2))



        # move notation: e2e6te7
        #                e2e6
        #                e2e6te4|e4e5te7
        square_map = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8}

        M = []
        if len(move) == 4:
            return parse_step(move)
        subs = move.split("|")

        for m in subs:
            M.append(parse_jump(m))
                    
        return M

    def calc_moves(self):
        pass

    def square_moves(self, square: Square) -> list[Move]:
        # TODO
        p = self.piece_at(square)
        return []

    # Actual move generation done here for steps
    def square_steps(self, square: Square) -> list[Step]:

        def direxp(direction: Direction) -> list[Square]:
            sqs: list[Square] = []
            sq = add_sq_dir(square, direction)
            while in_bounds(sq) and self.empty(sq):
                sqs.append(sq)
                sq = add_sq_dir(sq, direction)
            return sqs

        def in_bounds(square: Square) -> bool:
            r, c = square
            return 0 <= r < 8 and 0 <= c < 8

        def add_sq_dir(sq: Square, d: Direction) -> Square:
            return (sq[0] + d[0], sq[1] + d[1])

        p = self.piece_at(square)

        def pawn():
            c = -1 if p < 0 else 1
            d = -c
            moves = [add_sq_dir(square, (d, 0))]
            # add thingy to tell if at start spot and add another move
            start_row = 6 if p == 1 else 1
            if square[0] == start_row:
                moves.append(add_sq_dir(square, (d * 2, 0)))
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
            moves = [add_sq_dir(square, m) for m in moves]
            moves = [m for m in moves if self.empty(m) and in_bounds(m)]
            # moves = [m for m in moves if self.check_valid_step(square, m)]
            return moves

        def bishop():
            directions: list[Direction] = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
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
            moves = [add_sq_dir(square, m) for m in moves]
            moves = [m for m in moves if self.empty(m) and in_bounds(m)]
            return moves

        def empty() -> list[Square]:
            return []

        mv_sqs = [empty, pawn, knight, bishop, rook, queen, king][abs(p)]()
        moves: list[Step] = [(square, mv) for mv in mv_sqs]
        return moves

    # Actual move jump generation function.
    def square_jumps(self, square: Square, qctx: QueenContext = None) -> list[Jump]:
        # ctx is really just for the queen right now.
        # it will be a map { queen: ("diag"|"straight")}
        # maybe later it will just become a number (if efficiency matters super)
        def direxp(direction: Direction) -> Square:
            # TODO mod this to give the location of the piece it hits, not all the squares before
            # and give nothing if it hits the edge
            sq = add_sq_dir(square, direction)
            while in_bounds(sq) and self.empty(sq):
                sq = add_sq_dir(sq, direction)
            return sq

        def in_bounds(square: Square) -> bool:
            r, c = square
            return 0 <= r < 8 and 0 <= c < 8

        def add_sq_dir(sq: Square, d: Direction) -> Square:
            return (sq[0] + d[0], sq[1] + d[1])

        def jump_direction(taken: Square) -> Direction:
            # taken is the square of the taken piece
            def sign(num: int):
                return -1 if num < 0 else 0 if num == 0 else 1

            return (sign(taken[0] - square[0]), sign(taken[1] - square[1]))

        p = self.piece_at(square)

        def add_dir(mv: Square):
            return add_sq_dir(mv, jump_direction(mv))

        def pawn():

            c = -1 if p < 0 else 1
            d = -c
            possible_pieces = [add_sq_dir(square, (d, 1)), add_sq_dir(square, (d, -1))]
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
            def split_dir(direction: Direction) -> list[Direction]:
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
            moves = [add_sq_dir(square, m) for m in moves]
            moves = [m for m in moves if in_bounds(m) and not self.empty(m)]
            new_moves: list[tuple[Square, Square]] = []
            for mv in moves:
                d = split_dir(jump_direction(mv))
                new_moves.append((mv, add_sq_dir(mv, d[0])))
                new_moves.append((mv, add_sq_dir(mv, d[1])))
            new_moves = [
                mv for mv in new_moves if in_bounds(mv[1]) and self.empty(mv[1])
            ]
            # taking over the edges again
            return new_moves

        def bishop():
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            possible_pieces = [direxp(d) for d in directions]
            moves = [
                mv for mv in possible_pieces if in_bounds(mv) and not self.empty(mv)
            ]
            moves = [
                (mv, add_dir(mv))
                for mv in moves
                if in_bounds(add_dir(mv)) and self.empty(add_dir(mv))
            ]
            # TODO right now this won't allow taking around the edges. fix that
            # debangshu prob already handled something like this in the move checking. look there for inspo/stuff to can copy
            return moves

        def rook():
            directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
            possible_pieces = [direxp(d) for d in directions]
            moves = [
                mv for mv in possible_pieces if in_bounds(mv) and not self.empty(mv)
            ]
            moves = [
                (mv, add_dir(mv))
                for mv in moves
                if in_bounds(add_dir(mv)) and self.empty(add_dir(mv))
            ]
            # TODO right now this won't allow taking around the edges. fix that
            # debangshu prob already handled something like this in the move checking. look there for inspo/stuff to can copy
            return moves

        def queen():
            if qctx == None:
                return bishop() + rook()
            elif qctx == "diag":
                return bishop()
            else:
                return rook()

        def king():
            moves = [
                (-1, 1),
                (0, 1),
                (1, 1),
                (-1, 0),
                (1, 0),
                (-1, -1),
                (0, -1),
                (1, -1),
            ]
            moves = [add_sq_dir(square, m) for m in moves]
            moves = [m for m in moves if in_bounds(m) and not self.empty(m)]
            moves = [
                (mv, add_dir(mv))
                for mv in moves
                if in_bounds(add_dir(mv)) and self.empty(add_dir(mv))
            ]
            return moves

        def empty() -> list[tuple[Square, Square]]:
            return []

        # if abs(p) == 1:
        #    return pawn()
        # if abs(p) == 2:
        #    return knight()
        dispatch = [empty, pawn, knight, bishop, rook, queen, king]
        return [(square, jmp[0], jmp[1]) for jmp in dispatch[abs(p)]()]

    def square_jumps_recursive(
        self, square: Square, qctx: QueenContext = None
    ) -> list[JumpMove] | None:
        def new_qctx(jump: Jump) -> QueenContext:
            # Basically, see if the queen jumped, and if so, which way
            pass

        def jump_end(jump: Jump) -> Square:
            return jump[2]

        jumps: list[Jump] = self.square_jumps(square, qctx)

        # Base case is there is no more jumps possible from that square
        # One above that is the piece could make some jumps.
        # What I want this to return is a list of moves I can prepend a jump to

        if len(jumps) == 0:
            return None

        # TODO implement Board.copy() and Board.do_jump(Jump)

        def next_level(jump: Jump) -> list[JumpMove] | None:
            nb = self.copy()  # Copy board
            nb.do_jump(jump)  # Execute move
            ctx = new_qctx(jump)
            # Get the new ctx (see if queen jumped diag or straight basically)
            return nb.square_jumps_recursive(jump_end(jump), ctx)
            # Check for more jumps this piece can do (so look at where it landed)
            #

        output: list[JumpMove] = []
        for jump in jumps:
            next_jumps: list[JumpMove] | None = next_level(jump)
            if next_jumps == None:
                output.append([jump])  # [jump] is a valid JumpMove
            else:
                for next_jump in next_jumps:
                    output.append([jump] + next_jump)
        # This feels mostly complete/roughed out, but the base case feels wrong.
        # Also, what will the data type this outputs be? (/ what will the format be?)
        return output

    def empty(self, square: Square) -> bool:
        return 0 == self.piece_at(square)

    def copy(self):
        return Board(False, self.__str__())

    def do_jump(self, jump: Jump):
        # assume it is valid
        (start, take, land) = jump
        p = self.piece_at(start)
        self.put_at(0, start)
        self.put_at(0, take)
        self.put_at(p, land)

    def put_at(self, p: Piece, sq: Square):
        r, c = sq
        self.squares[r][c] = p

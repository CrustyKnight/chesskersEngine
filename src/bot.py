# I like having this as a separate file, it's still integrated in chesskers.py tho
# Welcome to the world EDWARD! - EDWARD! Doesn't Work All Right, Damn! # He actually plays well lol.
from time import sleep
from typing import TypeAlias, Callable
from chesskers import Board

board: TypeAlias = Board
blist: TypeAlias = list[list[int]]
Square: TypeAlias = tuple[int, int]
Step: TypeAlias = tuple[Square, Square]
Jump: TypeAlias = tuple[Square, Square, Square]
JumpMove: TypeAlias = list[Jump]
Move: TypeAlias = JumpMove | Step

transposition_table: dict[int, tuple[float, Move]] = {}


# for transposition table
class State:
    def __init__(
        self, board: Board, evaluation: Callable[[Board], int | float], depth: int
    ):
        self.board = board
        self.depth = depth
        self.eval = evaluation


val_map = {
    0: 0,
    1: 1,
    2: 7,
    3: 4,
    4: 5,
    5: 6,
    6: 1000,
    -6: -1000,
    -5: -6,
    -4: -5,
    -3: -4,
    -2: -7,
    -1: -1,
}


def sevaluate(board: Board) -> int:
    total = 0

    for row in board.squares:
        for piece in row:
            total += val_map[piece]

    return total


def knight_col_favors(board: Board) -> float:
    def knight(square: Square) -> float:
        row, col = square
        if col / 6 > col / 3:
            return 7 + col / 6
        else:
            return 7 + col / 3

    total = 0

    for row in range(0, 8):
        for col in range(0, 8):
            piece = board.piece_at((row, col))
            total += (
                (piece / 7) * knight((row, col))
                if abs(piece == 2)
                else total + val_map[piece]
            )
    return total


evaluate = sevaluate


def evaluate_move(move: Move, board: Board, depth: int):
    # change if needed
    tb = board.copy()
    tb.push(move)

    score = alphabeta(tb, depth)
    print("SCORE OF " + board.to_UCN(move) + ": " + str(score))
    print(tb)
    # sleep(2)
    print("\n\n")
    return score


def test_depth_2(board: Board):
    val = 0
    if board.color == 1:
        val = float("-inf")
        for move in board.moves:
            tb = board.copy()
            tb.push(move)
            min = float("inf")
            for m in tb.moves:
                tb.push(m)
                v = evaluate(tb)
                if v <= min:
                    min = v

            v = min
            if v >= val:
                val = v

    else:
        val = float("inf")
        for move in board.moves:
            tb = board.copy()
            tb.push(move)
            min = float("-inf")
            for m in tb.moves:
                tb.push(m)
                v = evaluate(tb)
                if v >= min:
                    min = v

            v = min
            if v <= val:
                val = v

    return val


def alphabeta(board: board, depth: int) -> int | float:

    def evalmove(move: Move) -> int | float:
        # change if needed
        tb = board.copy()
        tb.push(move)

        return evaluate(tb)

    # not here for now but later move ordering algorithms will use board
    def order_moves(moves: list[Move]):
        # Some heuristic ideas:
        #   "decapitate" : only evalute head of move
        #   "nFav" : knights are pushed to the front
        #   other standard move ordering heuristics
        def estimate_move(mv: Move) -> float:
            val = 0
            if board.is_step(mv):
                val += 0.85 * (evalmove(mv))
                start, end = mv
                val += 0.2 * (1 if abs(board.piece_at(start)) == 2 else 0)
            return val

        return moves
        # return sorted(moves, key=lambda x: estimate_move(x))

    def abmax(board: Board, depth: int, alpha: int, beta: int) -> int:
        print("Trying at depth: " + str(depth))
        if depth == 1:
            return evaluate(board)
        moves: list[Move] = order_moves(board.moves)
        for move in moves:
            tb = board.copy()
            tb.push(move)
            print("I'm searching board:")
            tb.print()
            val = abmin(tb, depth - 1, alpha, beta)
            print("its value is: " + str(val))
            if val >= beta:
                return beta
            if val > alpha:
                alpha = val
        return alpha

    def abmin(board: Board, depth: int, alpha: int, beta: int) -> int:
        if depth == 1:
            return evaluate(board)
        moves: list[Move] = order_moves(board.moves)
        for move in moves:
            tb = board.copy()
            tb.push(move)
            val = abmax(tb, depth - 1, alpha, beta)
            if val <= alpha:
                return alpha
            if val < beta:
                beta = val
        return beta

    if board.color == 1:
        return abmax(board, depth, float("-inf"), float("inf"))
    else:
        return abmin(board, depth, float("-inf"), float("inf"))


def find_best_move(board: Board, depth: int) -> tuple[Move, int | float]:
    # change if needed
    white = True if board.color == 1 else False

    if white:
        # return max(map(board.moves, evaluate_move, board, depth), key=lambda m: m[0])
        evals: list[int] = []
        max = float("-inf")
        bmove = board.moves[0]
        for move in board.moves:
            evals.append(alphabeta(board, depth))

        for i in range(0, len(evals)):
            eval = evals[i]
            if eval >= max:
                max = eval
                bmove = board.moves[i]
                print(board.to_UCN(bmove))
                # sleep(1)

        return (bmove, max)

    else:
        # return min(map(board.moves, evaluate_move, board, depth), key=lambda m: m[0])
        evals: list[int] = []
        max = float("inf")
        bmove = board.moves[0]
        for move in board.moves:
            evals.append(evaluate_move(move, board, depth))

        for i in range(0, len(evals)):
            eval = evals[i]
            if eval <= max:
                max = eval
                bmove = board.moves[i]

        return (bmove, max)

# I like having this as a separate file, it's still integrated in chesskers.py tho
# Welcome to the world EDWARD! - EDWARD! Doesn't Work All Right, Damn! # He actually plays well lol. 
from typing import TypeAlias
from chesskers import Board

board: TypeAlias = Board
blist: TypeAlias = list[list[int]]
Square: TypeAlias = tuple[int, int]
Step: TypeAlias = tuple[Square, Square]
Jump: TypeAlias = tuple[Square, Square, Square]
JumpMove: TypeAlias = list[Jump]
Move: TypeAlias = JumpMove | Step

def map(l, fun, board:board, depth):
    ret = []
    for L in l:
        ret.append(fun(L, board, depth))

    return ret

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


evaluate = sevaluate


def evaluate_move(move: Move, board: Board, depth:int):
    # change if needed
    tb = board.copy()
    tb.push(move)

    score = alphabeta(tb, depth)
    return [score, move]


def alphabeta(board:board, depth:int) -> int | float:

    def evalmove(move: Move) -> int | float:
        # change if needed
        tb = board.copy()
        tb.push(move)

        return evaluate(tb)

    # not here for now but later move ordering algorithms will use board
    def order_moves(moves:list[Move]):
        # Some heuristic ideas:
        #   "decapitate" : only evalute head of move
        #   "nFav" : knights are pushed to the front
        #   other standard move ordering heuristics

        #omoves = sorted(moves, key=lambda x: evalmove(x))
        omoves = [[m, 0] for m in moves]

        for mv in omoves:
            if board.is_step(mv[0]):
                mv[1] += 0.85*(evalmove(mv[1])) 
                start, end = mv[0]
                mv[1] += 0.2*(1 if abs(board.piece_at(start)) == 2 else 0) 
                mv[1] += evalmove(mv[0][0])

        return sorted(omoves, key=lambda x: x[1])

    def abmax(board: Board, depth: int, alpha: int, beta: int) -> int:
        if depth == 1:
            return evaluate(board)

        tb = board.copy()

        M = order_moves(tb.moves)
        mvs: list[Move] = []
        for m in M:
           mvs.append(m[0]) 


        for move in mvs:
            # change if needed
            tb.push(move)
            val = abmin(board, depth - 1, alpha, beta)

            if val >= beta:
                break
            if val > alpha:
                alpha = val

            # change if needed
            tb.pop()
        return alpha

    def abmin(board, depth, alpha, beta):
        if depth == 1:
            return evaluate(board)

        tb = board.copy()

        moves = order_moves(tb.moves)

        for move in moves:
            # change if needed
            tb.push(move)
            val = abmax(board, depth - 1, alpha, beta)

            if val <= alpha:
                break
            if val < beta:
                beta = val

            # change if needed
            tb.pop()
        return beta

    # change if needed
    if board.color == 1:
        return abmax(board, depth, float("-inf"), float("inf"))
    else:
        return abmin(board, depth, float("-inf"), float("inf"))


def find_best_move(board:object, depth:int) -> Move:
    # change if needed
    white = True if board.color == 1 else False

    if white:
        return max(map(board.moves, evaluate_move, board, depth), key=lambda m: m[0])[1]
    else:
        return min(map(board.moves, evaluate_move, board, depth), key=lambda m: m[0])[1]

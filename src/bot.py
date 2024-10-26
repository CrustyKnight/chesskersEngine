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

transposition_table: dict[int, list[float | Move]] = {}

# for transposition table
class State:
    def __init__(self, board: Board, eval, depth: int):
        self.board = board
        self.depth = depth
        self.eval = eval

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

def knight_col_favors(board: Board) -> float:
    def knight(square:Square) -> float:
        row, col = square
        if col/6 > col/3:
            return 7 + col/6
        else:
            return 7 + col/3

    total = 0 

    for row in range(0,8):
        for col in range(0,8):
            piece = board.piece_at((row,col))
            total+=(piece/7)*knight((row,col)) if abs(piece == 2) else total+val_map[piece] 
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

        return sorted(omoves, key=lambda x: x[1])

    def abmax(depth: int, alpha: int, beta: int) -> int:
        state = State(board, evaluate, depth)
        h = hash(state)
        if h in transposition_table:
            return transposition_table[h][0]
        else:
            update = True

        if depth == 1:
            return evaluate(board)

        tb = board.copy()

        M = order_moves(tb.moves)
        mvs: list[Move] = []
        for m in M:
           mvs.append(m[0]) 
        
        bmove: Move = mvs[0]

        for move in mvs:
            tb.push(move)
            val = abmin(depth - 1, alpha, beta)

            if val >= beta:
                break
            if val > alpha:
                alpha = val
                bmove = move

            tb.pop()

        if update:
            transposition_table.update({hash(state) : [alpha, bmove]})
        return alpha

    def abmin(depth:int, alpha:int, beta:int):
        state = State(board, evaluate, depth)
        if hash(state) in transposition_table:
            return transposition_table[hash(state)][0]
        else:
            update = True


        if depth == 1:
            return evaluate(board)

        tb = board.copy()

        mvs = order_moves(tb.moves)
        moves = []
        for m in mvs:
            moves.append(m[0])
        
        bmove = moves[0]

        for move in moves:
            tb.push(move)
            val = abmax(depth - 1, alpha, beta)

            if val <= alpha:
                break
            if val < beta:
                beta = val
                bmove = move

            tb.pop()

        if update:
            transposition_table.update({hash(state) : [beta, bmove]})

        return beta

    # change if needed
    if board.color == 1:
        return abmax(depth, float("-inf"), float("inf"))
    else:
        return abmin(depth, float("-inf"), float("inf"))


def find_best_move(board:object, depth:int) -> list[Move|int]:
    # change if needed
    white = True if board.color == 1 else False

    if white:
        return max(map(board.moves, evaluate_move, board, depth), key=lambda m: m[0])
    else:
        return min(map(board.moves, evaluate_move, board, depth), key=lambda m: m[0])

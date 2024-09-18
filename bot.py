# I like having this as a separate file, it's still integrated in chesskers.py tho
# Welcome to the world EDWARD! - EDWARD! Doesn't Work All Right, Damn!

def map(l, fun, board, depth):
    ret = []
    for L in l:
        ret.append(fun(L, board, depth))

    return ret

evaluate = sevaluate

val_map = {

    0 : 0,
    1 : 1,
    2 : 7,
    3 : 4,
    4 : 5,
    5 : 6,
    6 : 1000,
    -6 : -1000,
    -5 : -6,
    -4 : -5,
    -3 : -4,
    -2 : -7,
    -1 : -1 

}

def sevaluate(board):
    total = 0

    for row in board.squares:
        for piece in row:
            total+=val_map[piece]
    
    return total
        

def evaluate_move(move, board, depth):
    # change if needed
    tb = board.copy()
    tb.move(move)

    score = alphabeta(tb,depth)
    return [score, move]

def alphabeta(board, depth):

    def evalmove(move, board):
        # change if needed
        tb = board.copy()
        tb.move(move)

        return evaluate(tb)


    def order_moves(moves, board):
        # Some heuristic ideas:
        #   "decapitate" : only evalute head of move
        #   "nFav" : knights are pushed to the front
        #   other standard move ordering heuristics

        return sorted(moves, key=lambda x : evalmove(x[0]))
        
    def abmax(board, depth, alpha, beta):
        if depth == 1:
            return evaluate(board)
        
        tb = board.copy()

        mvs = order_moves(tb.moves, tb)

        for move in mvs:
            # change if needed
            tb.move(move)
            val = abmin(board, depth - 1, alpha, beta)

            if val >= beta:
                break
            if val > alpha:
                alpha = val

            # change if needed
            tb.unmove()
        return alpha

    def abmin(board, depth, alpha, beta):
        if depth == 1:
            return evaluate(board)

        tb = board.copy()

        moves = order_moves(tb.legal_moves, tb)

        for move in moves:
            # change if needed
            tb.move(move)
            val = abmax(board, depth - 1, alpha, beta)

            if val <= alpha:
                break
            if val < beta:
                beta = val

            # change if needed
            tb.unmove()
        return beta

    # change if needed
    if board.turn == board.white:
        return abmax(board, depth, float("-inf"), float("inf"))
    else:
        return abmin(board, depth, float("-inf"), float("inf"))

def find_best_move(board, depth):
    # change if needed
    white = True if board.turn == board.white else False 

    if white:
        return max(map(board.moves, evaluate_move, board, depth), key=lambda m : m[0])[1]
    else:
        return min(map(board.moves, evaluate_move, board, depth), key=lambda m : m[0])[1]
     

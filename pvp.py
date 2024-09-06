from chesskers import Board


def main():
    game = Board()

    move = input("enter a move")

    while True:
        # change if needed
        if Board.legal_move(move):
            Board.push(move)
        else:
            print("move isn't legal")

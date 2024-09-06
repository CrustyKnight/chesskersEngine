from chesskers import Board


def main():
    game = Board()

    move = input("enter a move")

    while True:
        # change if needed
        if game.legal_move(move):
            game.push(move)
            print(game)
        else:
            print("move isn't legal")

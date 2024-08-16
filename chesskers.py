#!/usr/bin/env python3

class Board:
    def __init__(self):
        pass
    def from_string(self, string):
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
        for token in string.split():
            x = counter % 8
            y = counter // 8
            self.squares[y][x] = d[token]
            counter += 1

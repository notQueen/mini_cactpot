from random import randrange

class obj_tile():
    def __init__(self, game, number, value):
        self.game = game
        self.number = number
        self.value = value
        self.hidden = True
        self.text = "?"

class game_mini_cactpot():
    SCOREBOARD = {
        6: 10000,
        7: 36,
        8: 720,
        9: 360,
        10: 80,
        11: 252,
        12: 108,
        13: 72,
        14: 54,
        15: 180,
        16: 72,
        17: 180,
        18: 119,
        19: 36,
        20: 306,
        21: 1080,
        22: 144,
        23: 1800,
        24: 3600
    }
    LINES = {
        1: (1, 5, 9), 2: (1, 4, 7), 3: (2, 5, 8), 4: (3, 6, 9), 5: (3, 5, 7),
        6: (1, 2, 3),
        7: (4, 5, 6),
        8: (7, 8, 9)
    }

    def __init__(self):
        solution = []
        que = list(range(1, 10))
        while len(que) > 0:
            solution.append(que.pop(randrange(0, len(que))))
        self.tiles = [obj_tile(self, num, solution[num]) for num in range(9)]

    def calculate_score(self, line):
        """give line ref, get score"""
        sum = 0
        tiles = self.LINES[line]
        for tile in tiles: sum += self.tiles[tile].value
        return self.SCOREBOARD[sum]



def main():
    gaem = game_mini_cactpot()
    for tile in gaem.tiles: print(tile.value) # simple test

if __name__ == "__main__":
    main()
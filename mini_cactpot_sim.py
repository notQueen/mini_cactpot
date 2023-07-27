from random import randint

class obj_tile():
    def __init__(self, game, number, value):
        self.game = game
        self.number = number
        self.value = value
        self.hidden = True
        self.text = "?"



class game_mini_cactpot():
    def __init__(self):
        solution = ()
        que = list(range(1, 10))
        while len(que) > 0:
            solution.append(que.pop(randint(len(que))))
        tiles = [obj_tile(self, num, solution[num]) for num in range(9)]










class grid():
    def __init__(self, game):
        """
            pass parent game
        """
        self.game = game
        self.tiles = ()
    def add_tile(self, tile):
        self.tiles.append(tile)



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
        self.buttons = {}
        """
            this should contain references to 9 buttons with the index as key. exmaple: (5, buttonReference)
        """
        self.solution = {}
        """
            this should contain a list of all numbers from 1 though 9 (inclusive) in a randomized order to serve as the solution
        """
        self.gamestate = 0
        """
            0 : initial state. expects tile choice
            1 : tile choice finished. expects line choice
            2 : game over. display results
        """
        self.attempts = 3








    def get_score_from_line(self, line):
        sum = 0
        for tile in self.LINES[line]:
            sum += self.solution[tile]
        return self.SCOREBOARD[sum]
    
    def get_tiles_from_line(self, line):
        return self.LINES[line]
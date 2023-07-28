from random import randrange
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton

class obj_window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setMinimumSize(200, 200)
        self.setMaximumSize(1000, 1000)
    def resizeEvent(self, *args, **kwargs):
        shortest_side = min(self.height(), self.width())
        self.resize(shortest_side, shortest_side)

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

    def reveal_tile(self, tile):
        self.tiles[tile].hidden = False

    def calculate_score(self, line):
        """give line ref, get score"""
        sum = 0
        tiles = self.LINES[line]
        for tile in tiles: sum += self.tiles[tile].value
        return self.SCOREBOARD[sum]

class obj_monitor():
    def __init__(self, game):
        self.game = game
        self.app = QApplication()
        self.window = obj_window()
        self.widget = QWidget()
        self.layout = QGridLayout()

        self.window.setWindowTitle("Mini-Cactpot Simulator")
        self.window.setCentralWidget(self.widget)
        self.widget.setLayout(self.layout)

        self.buttons = {tile: QPushButton() for tile in range(len(self.game.tiles))}

        row, col = 0, 0

        for key, button in self.buttons.items():
            self.layout.addWidget(button, row, col)
            button.clicked.connect(self.update)
            if key % 3 == 2: col += 1; row = 0
            else: row += 1
        
        self.update()
        self.window.show()
        self.app.exec()

    def update(self):
        for key, button in self.buttons.items():
            if self.game.tiles[key].hidden: button.setText("?")
            else: button.setText(str(self.game.tiles[key].value))

    def reveal_tile(self, tile):
        self.game.reveal_tile(tile)
        self.update()

def main():
    game = game_mini_cactpot()
    monitor = obj_monitor(game)
    #for tile in game.tiles: print(tile.value) # simple test

if __name__ == "__main__":
    main()
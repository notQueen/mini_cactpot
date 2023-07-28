from random import randrange
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QSizePolicy, QPushButton
from PySide6.QtGui import QFont

"""
from PySide6.QtCore import QEvent, QSize

class obj_window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__()
        #self.setMinimumSize(300, 300)
        #self.setMaximumSize(1000, 1000)
        self.setFixedSize(300, 300)

    def resizeEvent(self, *args, **kwargs):
        shortest_side = min(self.height(), self.width())
        self.resize(shortest_side, shortest_side)
"""

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
        self.attempts = 3
        solution = []
        que = list(range(1, 10))
        while len(que) > 0:
            solution.append(que.pop(randrange(0, len(que))))
        self.tiles = {}
        for tile in range(len(solution)):
            self.tiles[tile] = obj_tile(self, tile, solution[tile])
        
        self.reveal_tile(self.tiles[randrange(0, len(self.tiles))], bypass=True)

    def reveal_tile(self, tile, bypass=False):
        if bypass == False:
            if not self.attempts > 0 or tile.hidden == False:
                return
            self.attempts -= 1
        tile.hidden = False

    def calculate_score(self, line):
        """give line ref, get score"""
        sum = 0
        tiles = self.LINES[line]
        for tile in tiles.items(): sum += self.tiles[tile].value
        return self.SCOREBOARD[sum]

class obj_monitor():
    ARROW_SYMBOLS = ["⇘", "⇓", "⇓", "⇓", "⇙", "⇒", "⇒", "⇒"]

    def __init__(self, game):
        self.game = game
        self.app = QApplication()
        self.window = QMainWindow()
        self.widget_outer = QWidget()
        self.widget_inner = QWidget()
        self.layout_outer = QGridLayout()
        self.layout_inner = QGridLayout()
        self.font_numbers = QFont()
        self.font_arrows = QFont()
        self.font_reset = QFont()

        self.window.setWindowTitle("Mini-Cactpot Simulator")
        self.window.setFixedSize(500, 500)
        self.window.setCentralWidget(self.widget_outer)

        self.widget_outer.setFixedSize(500, 500)
        self.widget_outer.setLayout(self.layout_outer)
        self.layout_outer.addWidget(self.widget_inner, 1, 1, 3, 3)
        self.layout_inner.setContentsMargins(0, 0, 0, 0)
        self.widget_inner.setLayout(self.layout_inner)

        self.font_numbers.setPointSize(30)
        self.font_arrows.setPointSize(20)
        self.font_arrows.setBold(True)
        self.font_reset.setPointSize(20)

        self.arrow_buttons = {}
        row, col = 0, 0
        for arrow in range(len(self.ARROW_SYMBOLS)):
            button = QPushButton()
            button.setText(self.ARROW_SYMBOLS[arrow])
            button.setFont(self.font_arrows)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout_outer.addWidget(button, row, col)
            if arrow <= 3:
                row = 0
                col += 1
            else:
                row += 1
                col = 0

        self.reset_button = QPushButton()
        self.reset_button.setText("RESET")
        self.reset_button.setFont(self.font_reset)
        self.reset_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout_outer.addWidget(self.reset_button, 4, 1, 1, 3)

        row, col = 0, 0
        self.buttons = {}
        for key, tile in self.game.tiles.items():
            tile.button = QPushButton()
            tile.button.tile = tile
            tile.button.clicked.connect(lambda _=None, button=tile.button: self.click(button)) # black magic
            tile.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            tile.button.setFont(self.font_numbers)
            self.layout_inner.addWidget(tile.button, row, col)
            self.buttons[key] = tile.button
            if key % 3 == 2: col += 1; row = 0
            else: row += 1


        """
        self.buttons = {tile: QPushButton() for tile in range(len(self.game.tiles))}

        for key, button in self.buttons.items():
            self.layout_inner.addWidget(button, row, col)
            button.clicked.connect(self.update)
            if key % 3 == 2: col += 1; row = 0
            else: row += 1
        """

        self.update()
        self.window.show()
        self.app.exec()

    def click(self, button):
        self.reveal_tile(button.tile)
        self.update()

    def update(self):
        for key, button in self.buttons.items():
            if button.tile.hidden: button.setText("?"); button.setStyleSheet(f"background-color: BurlyWood; color: black;")
            else: button.setText(str(button.tile.value)); button.setStyleSheet(f"background-color: DarkOrange; color: black;")

    def reveal_tile(self, tile):
        self.game.reveal_tile(tile)
        self.update()

def main():
    game = game_mini_cactpot()
    monitor = obj_monitor(game)
    #for tile in game.tiles: print(tile.value) # simple test

if __name__ == "__main__":
    main()
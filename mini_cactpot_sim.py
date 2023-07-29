from random import randrange
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QSizePolicy, QLabel, QPushButton
from PySide6.QtGui import QFont

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
    ARROW_DOUBLE = ["⇘", "⇓", "⇓", "⇓", "⇙", "⇒", "⇒", "⇒"]
    ARROW_NORMAL = ["↘", "↓", "↓", "↓", "↙", "→", "→", "→"]

    ARROW_SYMBOLS = ARROW_NORMAL

    def __init__(self, game):
        WINDOW_TITLE: str = "Mini-Cactpot Simulator"
        FONT_SIZE_NUMBERS: int = 30
        FONT_SIZE_ARROWS: int = 30
        FONT_BOLD_ARROWS: bool = True
        FONT_SIZE_RESET: int = 20
        WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500 # type: [int, int]
        OUTER_WIDTH, OUTER_HEIGHT = WINDOW_WIDTH, WINDOW_HEIGHT

        self.game = game
        self.app = QApplication()

        self.layout_inner = QGridLayout()
        self.layout_inner.setContentsMargins(0, 0, 0, 0)

        self.widget_inner = QWidget()
        self.widget_inner.setLayout(self.layout_inner)

        self.layout_side = QGridLayout()
        self.layout_side.setContentsMargins(0, 0, 0, 0)

        self.widget_side = QWidget()
        self.widget_side.setContentsMargins(0, 0, 0, 0)
        self.widget_side.setLayout(self.layout_side)

        self.layout_outer = QGridLayout()
        self.layout_outer.addWidget(self.widget_inner, 1, 1, 3, 3)
        self.layout_outer.addWidget(self.widget_side, 1, 4, 4, 1)

        self.widget_outer = QWidget()
        self.widget_outer.setLayout(self.layout_outer)
        self.widget_outer.setFixedSize(OUTER_WIDTH, OUTER_HEIGHT)

        self.window = QMainWindow()
        self.window.setWindowTitle(WINDOW_TITLE)
        self.window.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.window.setCentralWidget(self.widget_outer)

        self.font_numbers = QFont()
        self.font_numbers.setPointSize(FONT_SIZE_NUMBERS)

        self.font_arrows = QFont()
        self.font_arrows.setPointSize(FONT_SIZE_ARROWS)
        self.font_arrows.setBold(FONT_BOLD_ARROWS)

        self.font_reset = QFont()
        self.font_reset.setPointSize(FONT_SIZE_RESET)
        
        self.arrow_buttons = {}
        self.number_buttons = {}

        row, col = 0, 0
        for i, symbol in enumerate(self.ARROW_SYMBOLS):
            button = QPushButton()
            button.clicked.connect(lambda _=None, button=button: self.click_arrow(button))
            button.setFont(self.font_arrows)
            button.setText(symbol)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding,)
            self.layout_outer.addWidget(button, row, col)
            if i < 4: col += 1
            else: col = 0; row += 1

        self.reset_button = QPushButton()
        self.reset_button.setText("RESET")
        self.reset_button.clicked.connect(self.reset)
        self.reset_button.setFont(self.font_reset)
        self.reset_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout_outer.addWidget(self.reset_button, 4, 0)
        
        """

        for key, (sum, score) in enumerate(self.game.SCOREBOARD.items()):
            print(f"Current key: {key % len(self.game.SCOREBOARD) / 2}")
            label_sum = QLabel()
            label_sum.setText("test")
            #label_sum.setFont(score_font)
            label_score = QLabel()
            label_score.setText("score")
            #label_score.setFont(score_font)
            layout_pair = QGridLayout()
            layout_pair.addWidget(label_sum, 0, 0)
            layout_pair.addWidget(label_score, 0, 1)
            widget_pair = QWidget()
            widget_pair.setLayout(layout_pair)
            self.layout_side.addWidget(widget_pair, key % len(self.game.SCOREBOARD) / 2, 0)
        """
        
        score_font = QFont()
        score_font.setPointSize(7)
        for key, (sum, score) in enumerate(self.game.SCOREBOARD.items()):
            label_sum = QLabel()
            label_sum.setStyleSheet("background-color: yellow;")
            label_sum.setAlignment(Qt.AlignRight)
            label_sum.setFont(score_font)
            label_sum.setText(f"{sum}:")
            label_score = QLabel()
            label_score.setStyleSheet("background-color: yellow;")
            label_score.setAlignment(Qt.AlignLeft)
            label_score.setFont(score_font)
            label_score.setText(f"{score}")
            layout_pair = QGridLayout()
            layout_pair.setContentsMargins(0, 0, 0, 0)
            layout_pair.addWidget(label_sum, 0, 0)
            layout_pair.addWidget(label_score, 0, 1)
            widget_pair = QWidget()
            widget_pair.setLayout(layout_pair)
            self.layout_side.addWidget(widget_pair, key, 0)
        
        """
        self.label_text = ""
        for sum, score in self.game.SCOREBOARD.items():
            self.label_text += f"{sum}: {score}\n"
        temp_font = QFont()
        temp_font.setPointSize(8)
        self.label_side = QLabel()
        self.label_side.setText(self.label_text)
        self.label_side.setFont(temp_font)
        self.layout_side.addWidget(self.label_side, 1, 4, 3, 1)
        """
        
        # TRY GRID OF LABELS WITH SCORES
        # they can light up to indicate scores and stuff it'll be cute trust me

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

        self.update()
        self.window.show()
        self.app.exec()

    def click(self, caller):
        self.reveal_tile(caller.tile)
        self.update()
    
    def click_arrow(self, caller):
        pass

    def reset():
        pass

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

if __name__ == "__main__":
    main()
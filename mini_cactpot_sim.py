from random import randrange
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QSizePolicy, QLabel, QPushButton

class my_game():
    
    LINES = [(1, 5, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9),
             (3, 5, 7), (1, 2, 3), (4, 5, 6), (7, 8, 9)]
    
    SCOREBOARD = {6: 10000, 7: 36, 8: 720, 9: 360, 10: 80, 11: 252, 12: 108, 13: 72, 14: 54, 15: 180,
                  16: 72, 17: 180, 18: 119, 19: 36, 20: 306, 21: 1080, 22: 144, 23: 1800, 24: 3600}

    def __init__(self) -> None:
        self.tiles = [my_tile() for _ in range(9)]
        self.lines = self.LINES
        self.reset()
    
    def reset(self):
        self.attempts = 3
        que = list(range(1, 10))
        for tile in self.tiles:
            tile.set(que.pop(randrange(len(que))))
        
    def check_tile(self, tile_index):
        tile = self.tiles[tile_index]
        if tile.is_open() or self.attempts > 1: return 0
        self.attempts -= 1
        return tile.check()
    
    def check_line(self, line_index):
        line = self.lines[line_index]; sum = 0
        for tile in line:
            sum += self.tiles[tile].fetch()
        self.reset(); return sum


class my_tile():
    def __init__(self):
        self.set()
    
    def fetch(self) -> int:
        self.open = True
        return self.value
    
    def set(self, value=None) -> None:
        self.open = False
        self.value = value
        
    def is_open(self) -> bool:
        return self.open




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
        self.layout_side.setSpacing(0)
        self.layout_side.setContentsMargins(0, 0, 0, 0)

        self.widget_side = QWidget()
        self.widget_side.setContentsMargins(0, 0, 0, 0)
        self.widget_side.setLayout(self.layout_side)

        self.layout_outer = QGridLayout()
        self.layout_outer.addWidget(self.widget_inner, 1, 1, 3, 3)
        self.layout_outer.addWidget(self.widget_side, 1, 4, 3, 1)

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
        score_font.setPointSize(8)
        for key, (sum, score) in enumerate(self.game.SCOREBOARD.items()):
            label_sum = QLabel()
            #label_sum.setStyleSheet("background-color: yellow;")
            label_sum.setAlignment(Qt.AlignRight)
            label_sum.setFont(score_font)
            label_sum.setText(f"{sum}")
            label_divisor = QLabel()
            #label_divisor.setStyleSheet("background-color: LightBlue;")
            label_divisor.setFixedWidth(8)
            label_divisor.setAlignment(Qt.AlignCenter)
            label_divisor.setFont(score_font)
            label_divisor.setText(":")
            label_score = QLabel()
            #label_score.setStyleSheet("background-color: yellow;")
            label_score.setAlignment(Qt.AlignLeft)
            label_score.setFont(score_font)
            label_score.setText(f"{score}")
            layout_pair = QGridLayout()
            layout_pair.setSpacing(0)
            layout_pair.setContentsMargins(0, 0, 0, 0)
            layout_pair.addWidget(label_sum, 0, 0)
            layout_pair.addWidget(label_divisor, 0, 1)
            layout_pair.addWidget(label_score, 0, 2)
            widget_pair = QWidget()
            #widget_pair.setStyleSheet("background-color: rgb(100, 200, 100);")
            widget_pair.setLayout(layout_pair)
            self.layout_side.addWidget(widget_pair, key, 0)
        
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

class display_button():
    def __init__(self, index, *args, **kwargs):
        self.index = index
        self.reset()
        self.main(*args, **kwargs)
        
    def reset(self):
        self.highlight(0)
    
    def enable(self):
        self.Q.setEnabled()
    
    def disable(self):
        self.Q.setDisabled()
    
    def highlight(self, heat: int):
        if heat == 0:
            pass
        if heat == 1:
            pass
        if heat == 2:
            pass

class display_tile(display_button):
    def main():
        new = QPushButton()
        
    def reset(self):
        self.hide()
        self.enable()
        super().reset()
    
    def reveal(self, value: int):
        self.Q.setText(f"{value}")
    
    def hide(self):
        self.Q.setText("?")

class display_arrow(display_button):
    def main():
        new = QPushButton()
    
    def reset(self):
        self.disable()
        super().reset()
    
class display_scoreboard():
    def __init__(self) -> None:
        new = QWidget

class display_manager():
    def __init__(self, game):
        self.game = game
        self.grid = {}
        self.arrows = {}
        
        for tile in game.tiles: # if this isn't 9 then something is very wrong
            new = display_tile()
            self.grid.append(new)
        
        for arrow in game.arrows: # if this isn't 9 then something is very wrong
            new = display_arrow()
            self.arrows.append(new)
        
        self.scoreboard = display_scoreboard()

        new = QPushButton
        new.setText("Reset")
        new.clicked.connect(self.reset)
        self.reset = new
    
    def get_state():
        pass
    
    def grid_enabled(self, switch: bool):
        for tile in self.grid:
            if switch:
                tile.enable()
            else:
                tile.disable()
    
    def arrows_enabled(self, switch: bool):
        for arrow in self.arrows:
            if switch:
                arrow.enable()
            else:
                arrow.disable()
                
    def reset(self): # each tile should have their own reset.
        self.game.reset()
        for tile in self.grid:
            tile.enable()
            tile.hide()
            tile.highlight(0)
        for arrow in self.arrows:
            arrow.disable()
            arrow.highlight(0)
            
    def on_grid_click(self, tile):
        if reply := self.game.activate(tile.index) == 0: return
        tile.reveal(reply)
    
    def on_arrow_click(self, arrow):
        if reply := self.game.arrow(arrow.index) == 0: return
        self.present_score(reply)
    


    
# what methods does a manager need?
    # get state
    # hide / reveal values
    # highlight / unhighlight buttons
    # disable / enable keypad
    # disable / enable arrows
    # reset everything
    # check a given line
    # communicate score





def main():
    game = game_mini_cactpot()
    monitor = obj_monitor(game)

if __name__ == "__main__":
    main()
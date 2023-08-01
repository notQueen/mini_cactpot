from random import randrange
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QSizePolicy, QLabel, QPushButton

####################################################################################################
# GAME

class core_game():
    
    LINES = [(0, 4, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
             (2, 4, 6), (0, 1, 2), (3, 4, 5), (6, 7, 8)]
    
    SCOREBOARD = {6: 10000, 7: 36, 8: 720, 9: 360, 10: 80, 11: 252, 12: 108, 13: 72, 14: 54, 15: 180,
                  16: 72, 17: 180, 18: 119, 19: 36, 20: 306, 21: 1080, 22: 144, 23: 1800, 24: 3600}

    def __init__(self) -> None:
        self.tiles = [core_tile(n) for n in range(9)]
        self.lines = self.LINES
        self.listeners = []
        self.reset()
        return
    
    def play(self, move = -1, reset = False):
        if reset:
            self.reset()
        if self.state == 1 and move in range(len(self.tiles)):
            tile = self.tiles[move]
            if not tile.open and self.attempts > 0:
                self.attempts -= 1
                if not self.attempts:
                    self.state = 2
                tile.open = True
                self.preach()
                return
        elif self.state == 2 and move in range(len(self.lines)):
            self.state = 3
            for tile in self.tiles:
                tile.open = True
            line = self.lines[move]
            total = sum([self.tiles[ref].value for ref in line])
            self.score = self.SCOREBOARD[total]
            self.preach()
            return
        return
    
    def reset(self) -> None:
        # reset state
        self.state = 1
        self.attempts = 3
        self.score = 0
        # make new solution
        que = list(range(1, 10))
        for tile in self.tiles:
            tile.value = que.pop(randrange(len(que)))
            tile.open = False
        self.tiles[randrange(len(self.tiles))].open = True
        self.preach()
        return None
    
    def register_listener(self, listener):
        self.listeners.append(listener)
        self.preach()
        return
    
    def preach(self): # brute force preach everything initially. implement selective preach at a later time maybe.
        audience = self.listeners
        state_of_the_board = [tile.get_value() for tile in self.tiles]
        for dude in audience:
            dude.listen(self.state, state_of_the_board, self.score)
        return
    
####################################################################################################
# GAME COMPONENTS

class core_tile():
    def __init__(self, value) -> None:
        self.open: bool
        self.value: int
        self.set(value)
        return
    
    def get_value(self) -> int:
        if self.open: return self.value
        return 0
    
    def set(self, value) -> None:
        self.open = False
        self.value = value
        return
    
####################################################################################################
# DISPLAY

class custom_QPushButton(QPushButton):
    def resizeEvent(self, event):
        new_size = event.size()
        shortest_side = min(new_size.width(), new_size.height())
        self.resize(shortest_side, shortest_side)
        super().resizeEvent(event)

class monitor_frame():
    def __init__(self):
        widget = self.widget = QWidget()
        layout = self.layout = QGridLayout(widget)

class monitor_button():
    def __init__(self):
        button = self.button = custom_QPushButton()
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.setFixedSize(50, 50)
    
class monitor_tile(monitor_button):
    def __init__(self):
        super().__init__()
        return
    
    def display(self, payload):
        if payload == 0:
            self.button.setText("?")
        else:
            self.button.setText(str(payload))

class monitor_arrow(monitor_button):
    def __init__(self, symbol):
        super().__init__()
        self.button.setText(symbol)

class core_monitor():

    # ARROWS = ["⇘", "⇓", "⇓", "⇓", "⇙", "⇒", "⇒", "⇒"]
    ARROWS = ["↘", "↓", "↓", "↓", "↙", "→", "→", "→"]
    
    def __init__(self, game):
        self.game = game
        self.tiles = []
        self.arrows= []
        app = QApplication()
        window = QMainWindow()
        window.setWindowTitle("Mini-Cactpot Sim")
        
        main_wrapper = monitor_frame()
        window.setCentralWidget(main_wrapper.widget)
        
        reset_button = self.reset_button = monitor_button()
        reset_button.button.setText("Reset")
        reset_button.button.clicked.connect(self.on_reset_click)
        main_wrapper.layout.addWidget(reset_button.button, 3, 4)
        
        for key, arrow_symbol in enumerate(self.ARROWS):
            new_arrow = monitor_arrow(arrow_symbol)
            main_wrapper.layout.addWidget(new_arrow.button, (key - 4) * (key > 4), key * (key <= 4))
            new_arrow.button.clicked.connect(lambda _ = None, payload = key: self.on_arrow_click(payload))
            self.arrows.append(new_arrow)
        
        for key, _ in enumerate(game.tiles):
            new_tile = monitor_tile()
            main_wrapper.layout.addWidget(new_tile.button, 1 + (int(key / 3)), 1 + (key % 3))
            new_tile.button.clicked.connect(lambda _ = None, payload = key: self.on_tile_click(payload))
            self.tiles.append(new_tile)
        
        scoreboard = self.scoreboard = monitor_frame()
        scoreboard.label = QLabel()
        scoreboard.layout.addWidget(scoreboard.label)
        main_wrapper.layout.addWidget(scoreboard.widget, 1, 4, 2, 1)
        
        game.register_listener(self)
        window.show()
        app.exec()
        return
    
    def listen(self, game_state, board_state, score):
        if not score: score = "?"
        self.scoreboard.label.setText(f"Score:\n{score}")
        [tile.display(message) for tile, message in zip(self.tiles, board_state)]
        if game_state == 1:
            self.disable_tiles(False)
            self.disable_arrows(True)
        if game_state == 2:
            self.disable_tiles(True)
            self.disable_arrows(False)
        if game_state == 3:
            self.disable_tiles(True)
            self.disable_arrows(True)
        return
    
    def disable_tiles(self, state):
        for tile in self.tiles:
            tile.button.setDisabled(state)
    
    def disable_arrows(self, state):
        for arrow in self.arrows:
            arrow.button.setDisabled(state)
    
    def on_tile_click(self, button_ref):
        self.game.play(button_ref)
        return
    
    def on_arrow_click(self, arrow_ref):
        self.game.play(arrow_ref)
        return
    
    def on_reset_click(self):
        self.game.play(reset = True)
        return
    
####################################################################################################
# MAIN

def main():
    game = core_game()
    monitor = core_monitor(game)

if __name__ == "__main__":
    main()
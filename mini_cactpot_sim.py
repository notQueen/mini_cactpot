from random import randrange
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QSizePolicy, QLabel, QPushButton

class core_game():
    
    LINES = [(0, 4, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
             (2, 4, 6), (0, 1, 2), (3, 4, 5), (6, 7, 8)]
    
    SCOREBOARD = {6: 10000, 7: 36, 8: 720, 9: 360, 10: 80, 11: 252, 12: 108, 13: 72, 14: 54, 15: 180,
                  16: 72, 17: 180, 18: 119, 19: 36, 20: 306, 21: 1080, 22: 144, 23: 1800, 24: 3600}

    def __init__(self) -> None:
        self.tiles = [core_tile() for _ in range(9)]
        self.lines = self.LINES
        self.reset()
    
    def play(self, ref: int) -> int:
        # GAME LOGIC GOES HERE ?
        pass
    
    def reset(self) -> None:
        self.state = 1
        self.attempts = 3
        self.make()
        
    def make(self):
        que = list(range(1, 10))
        for tile in self.tiles:
            tile.set(que.pop(randrange(len(que))))
    
    def get_state(self):
        return self.state
    
    def look(self, ref):
        return self.tiles[ref].look()
    
    def check_tile(self, tile_index):
        tile = self.tiles[tile_index]
        # rewrite me
        return tile.check()
    
    def check_line(self, line_index):
        line = self.lines[line_index]; sum = 0
        for tile in line:
            sum += self.tiles[tile].fetch()
        self.reset(); return sum
    
    def open(self, ref):
        self.tiles[ref].open = True
    
    def close(self, ref):
        self.tiles[ref].open = False

class core_tile():
    def __init__(self):
        # self.open: bool
        # self.value: int
        self.set()
    
    def look(self) -> int:
        if self.open: return self.value
        return 0
    
    def set(self, value=None) -> None:
        self.open = False
        self.value = value

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
        app = QApplication()
        window = QMainWindow()
        window.setWindowTitle("Mini-Cactpot Sim")
        
        main_wrapper = monitor_frame()
        window.setCentralWidget(main_wrapper.widget)
        
        reset_button = self.reset_button = monitor_button()
        reset_button.button.setText("Reset")
        reset_button.button.clicked.connect(self.reset)
        main_wrapper.layout.addWidget(reset_button.button, 3, 4)
        
        for key, arrow_symbol in enumerate(self.ARROWS):
            new_arrow = monitor_arrow(arrow_symbol)
            main_wrapper.layout.addWidget(new_arrow.button, (key - 4) * (key > 4), key * (key <= 4))
        
        for key, _ in enumerate(game.tiles):
            new_tile = monitor_tile()
            main_wrapper.layout.addWidget(new_tile.button, 1 + (int(key / 3)), 1 + (key % 3))
            new_tile.button.clicked.connect(lambda _ = None, payload = key: self.on_click(payload))
            self.tiles.append(new_tile)
        
        # window
            # widget -> main wrapper
                # layout < ^ monitor_frame
                    # 8 arrow buttons
                    # 9 tile butoons
                    # reset button
                    # widget -> scoreboard
        
        self.get_state()
        window.show()
        app.exec()
    
    def reset(self):
        pass
    
    def get_state(self):
        [tile.display(state) for tile, state in zip(self.tiles, self.game.get_state())]
        
    def on_click(self, button_ref):
        self.tiles[button_ref].display(self.game.tiles[button_ref].fetch())

    # what does a monitor need?
        # arrow symbols
        # a window
        # a grid of tiles
        # arrow buttons
        # a reset button
        # a scoreboard
        # wrappers

def main():
    game = core_game()
    monitor = core_monitor(game)

if __name__ == "__main__":
    main()
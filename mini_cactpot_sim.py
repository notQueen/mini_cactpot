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
    
    def reset(self) -> None:
        self.attempts = 3
        que = list(range(1, 10))
        for tile in self.tiles:
            tile.set(que.pop(randrange(len(que))))
    
    def get_state(self) -> list:
        return [tile.look() for tile in self.tiles]
    
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

class core_tile():
    def __init__(self):
        self.set()
    
    def look(self) -> int:
        if self.open: return self.value
        return 0
    
    def fetch(self) -> int:
        self.open = True
        return self.value
    
    def set(self, value=None) -> None:
        self.open = False
        self.value = value
        
    def is_open(self) -> bool:
        return self.open

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

class monitor_arrow(monitor_button):
    def __init__(self, symbol):
        super().__init__()
        self.button.setText(symbol)

class core_monitor():

    # ARROWS = ["⇘", "⇓", "⇓", "⇓", "⇙", "⇒", "⇒", "⇒"]
    ARROWS = ["↘", "↓", "↓", "↓", "↙", "→", "→", "→"]
    
    def __init__(self, game):
        self.game = game
        app = QApplication()
        window = QMainWindow()
        
        main_wrapper = monitor_frame()
        window.setCentralWidget(main_wrapper.widget)
        
        for key, arrow_symbol in enumerate(self.ARROWS):
            new_arrow = monitor_arrow(arrow_symbol)
            main_wrapper.layout.addWidget(new_arrow.button, (key - 4) * (key > 4), key * (key <= 4))
        
        for key, _ in enumerate(game.tiles):
            new_tile = monitor_tile()
            main_wrapper.layout.addWidget(new_tile.button, 1 + (key % 3), 1 + (int(key / 3)))
        
        # window
            # widget -> main wrapper
                # layout < ^ monitor_frame
                    # 8 arrow buttons
                    # 9 tile butoons
                    # reset button
                    # widget -> scoreboard

        window.show()
        app.exec()

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
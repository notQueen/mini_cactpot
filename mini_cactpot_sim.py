from random import randrange
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QSizePolicy, QLabel, QPushButton

class core_game():
    
    LINES = [(1, 5, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9),
             (3, 5, 7), (1, 2, 3), (4, 5, 6), (7, 8, 9)]
    
    SCOREBOARD = {6: 10000, 7: 36, 8: 720, 9: 360, 10: 80, 11: 252, 12: 108, 13: 72, 14: 54, 15: 180,
                  16: 72, 17: 180, 18: 119, 19: 36, 20: 306, 21: 1080, 22: 144, 23: 1800, 24: 3600}

    def __init__(self) -> None:
        self.tiles = [core_tile() for _ in range(9)]
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

class core_tile():
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

    
class monitor_frame():
    def __init__(self):
        widget = QWidget()
        layout = QGridLayout(widget)
        
        self.widget = widget
        self.layout = layout

class monitor_scoreboard(monitor_frame):
    def __init__(self):
        super().__init__()
    
class monitor_button():
    def __init__(self, parent):
        button = QPushButton()
        parent.addWidget(button)
        # customize buttons here
        self.button = button
    
class monitor_tile(monitor_button):
    def __init__(self):
        super().__init__()

class monitor_arrow(monitor_button):
    def __init__(self):
        super().__init__()

class core_monitor():

    ARROW_DOUBLE = ["⇘", "⇓", "⇓", "⇓", "⇙", "⇒", "⇒", "⇒"]
    ARROW_NORMAL = ["↘", "↓", "↓", "↓", "↙", "→", "→", "→"]
    
    def __init__(self, game):
        self.game = game
        app = QApplication()
        window = QMainWindow()
        
        frame_outer = monitor_frame()
        window.setCentralWidget(frame_outer.widget)
        
        

        
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
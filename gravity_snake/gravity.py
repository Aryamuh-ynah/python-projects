# gravity.py

from config import CELL_SIZE

class Gravity:
    def __init__(self):
        self.direction = 0  # 0=Down, 1=Left, 2=Up, 3=Right

    def rotate(self):
        """Rotate gravity 90 degrees clockwise"""
        self.direction = (self.direction + 1) % 4

    def get_vector(self):
        vectors = {
            0: (0, CELL_SIZE),     # Down
            1: (-CELL_SIZE, 0),    # Left
            2: (0, -CELL_SIZE),    # Up
            3: (CELL_SIZE, 0)      # Right
        }
        return vectors[self.direction]

    def get_name(self):
        names = ["↓ DOWN", "← LEFT", "↑ UP", "→ RIGHT"]
        return names[self.direction]
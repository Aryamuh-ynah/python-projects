# snake.py

from config import CELL_SIZE, GREEN, BLUE

class Snake:
    def __init__(self, start_pos):
        self.body = [start_pos]
        self.direction = (CELL_SIZE, 0)  # starting moving right
        self.grow = False

    def change_direction(self, new_dir):
        # Prevent 180 degree turns
        opposite = (-self.direction[0], -self.direction[1])
        if new_dir != opposite:
            self.direction = new_dir

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

        return new_head

    def grow_snake(self):
        self.grow = True

    def check_self_collision(self):
        return self.body[0] in self.body[1:]

    def draw(self, screen):
        for i, segment in enumerate(self.body):
            color = GREEN if i == 0 else BLUE
            import pygame
            pygame.draw.rect(screen, color, (segment[0], segment[1], CELL_SIZE - 1, CELL_SIZE - 1))
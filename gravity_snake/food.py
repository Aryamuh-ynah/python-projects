# food.py

import random
from config import WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, RED

class Food:
    def __init__(self, snake_body):
        self.position = self.spawn(snake_body)

    def spawn(self, snake_body):
        while True:
            x = random.randrange(0, WINDOW_WIDTH // CELL_SIZE) * CELL_SIZE
            y = random.randrange(0, WINDOW_HEIGHT // CELL_SIZE) * CELL_SIZE
            if (x, y) not in snake_body:
                return (x, y)

    def draw(self, screen):
        import pygame
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], CELL_SIZE - 1, CELL_SIZE - 1))
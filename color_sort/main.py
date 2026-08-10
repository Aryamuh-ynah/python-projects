import pygame
import sys
from config import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Color Sort Puzzle - Step 1")
clock = pygame.time.Clock()

def draw_bottle(surface, x, y, colors):
    """
    colors = list of color names from bottom to top
    Example: ["red", "blue", "green"]
    """
    # Bottle body
    body_rect = pygame.Rect(x, y + BOTTLE_NECK_HEIGHT, BOTTLE_WIDTH, BOTTLE_HEIGHT - BOTTLE_NECK_HEIGHT)
    pygame.draw.rect(surface, WHITE, body_rect, border_radius=12)
    pygame.draw.rect(surface, BLACK, body_rect, 3, border_radius=12)

    # Neck
    neck_x = x + (BOTTLE_WIDTH - BOTTLE_NECK_WIDTH) // 2
    neck_rect = pygame.Rect(neck_x, y, BOTTLE_NECK_WIDTH, BOTTLE_NECK_HEIGHT + 10)
    pygame.draw.rect(surface, WHITE, neck_rect, border_radius=6)
    pygame.draw.rect(surface, BLACK, neck_rect, 3, border_radius=6)

    # Draw liquid levels (from bottom)
    for i, color_name in enumerate(colors):
        color = COLOR_MAP.get(color_name, GRAY)
        level_y = y + BOTTLE_HEIGHT - (i + 1) * LEVEL_HEIGHT
        level_rect = pygame.Rect(x + 4, level_y, BOTTLE_WIDTH - 8, LEVEL_HEIGHT - 2)
        pygame.draw.rect(surface, color, level_rect, border_radius=6)

def main():
    # Example bottles (bottom → top)
    bottles = [
        ["red", "blue", "green", "yellow"],
        ["blue", "red"],
        ["green", "yellow", "blue"],
        [],                          # empty bottle
        ["orange", "purple", "pink"],
        ["cyan", "orange"],
    ]

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Drawing
        screen.fill(BACKGROUND)

        # Draw bottles in a row
        start_x = 80
        gap = 40
        for i, colors in enumerate(bottles):
            x = start_x + i * (BOTTLE_WIDTH + gap)
            y = 200
            draw_bottle(screen, x, y, colors)

        # Title
        font = pygame.font.SysFont("comicsansms", 40)
        title = font.render("Color Sort Puzzle", True, WHITE)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 40))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
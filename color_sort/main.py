import pygame
import sys
from config import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Color Sort Puzzle - Step 2")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 32)
small_font = pygame.font.SysFont("comicsansms", 24)

def draw_bottle(surface, x, y, colors, selected=False):
    """
    colors = list of color names from bottom to top
    selected = True if this bottle is currently selected
    """
    # Highlight if selected
    if selected:
        # Glow effect
        glow_rect = pygame.Rect(x - 8, y - 8, BOTTLE_WIDTH + 16, BOTTLE_HEIGHT + 16)
        pygame.draw.rect(surface, (255, 255, 100), glow_rect, border_radius=16)
    
    # Bottle body
    body_rect = pygame.Rect(x, y + BOTTLE_NECK_HEIGHT, BOTTLE_WIDTH, BOTTLE_HEIGHT - BOTTLE_NECK_HEIGHT)
    pygame.draw.rect(surface, WHITE, body_rect, border_radius=12)
    pygame.draw.rect(surface, BLACK, body_rect, 3, border_radius=12)

    # Neck
    neck_x = x + (BOTTLE_WIDTH - BOTTLE_NECK_WIDTH) // 2
    neck_rect = pygame.Rect(neck_x, y, BOTTLE_NECK_WIDTH, BOTTLE_NECK_HEIGHT + 10)
    pygame.draw.rect(surface, WHITE, neck_rect, border_radius=6)
    pygame.draw.rect(surface, BLACK, neck_rect, 3, border_radius=6)

    # Draw liquid levels (from bottom to top)
    for i, color_name in enumerate(colors):
        color = COLOR_MAP.get(color_name, GRAY)
        level_y = y + BOTTLE_HEIGHT - (i + 1) * LEVEL_HEIGHT
        level_rect = pygame.Rect(x + 4, level_y, BOTTLE_WIDTH - 8, LEVEL_HEIGHT - 2)
        pygame.draw.rect(surface, color, level_rect, border_radius=6)

def get_bottle_index(mouse_pos, bottle_positions):
    """Return the index of the bottle that was clicked, or None"""
    mx, my = mouse_pos
    for i, (x, y) in enumerate(bottle_positions):
        # Check if click is inside the bottle area
        if x <= mx <= x + BOTTLE_WIDTH and y <= my <= y + BOTTLE_HEIGHT:
            return i
    return None

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

    # Calculate positions of bottles
    start_x = 80
    gap = 40
    bottle_y = 220
    bottle_positions = []
    for i in range(len(bottles)):
        x = start_x + i * (BOTTLE_WIDTH + gap)
        bottle_positions.append((x, bottle_y))

    selected = None          # Currently selected bottle index

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    clicked = get_bottle_index(event.pos, bottle_positions)

                    if clicked is not None:
                        if selected is None:
                            # First selection
                            selected = clicked
                        elif selected == clicked:
                            # Clicked the same bottle → deselect
                            selected = None
                        else:
                            # Second bottle selected → ready for pouring (Step 3)
                            print(f"Pour from bottle {selected} to bottle {clicked}")
                            # For now just deselect after choosing destination
                            selected = None

        # ========== DRAW ==========
        screen.fill(BACKGROUND)

        # Title
        title = font.render("Color Sort Puzzle", True, WHITE)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 30))

        # Instruction
        if selected is None:
            instruction = small_font.render("Click a bottle to select", True, (180, 180, 180))
        else:
            instruction = small_font.render("Click another bottle to pour", True, (255, 255, 100))
        screen.blit(instruction, (WINDOW_WIDTH // 2 - instruction.get_width() // 2, 80))

        # Draw all bottles
        for i, colors in enumerate(bottles):
            x, y = bottle_positions[i]
            is_selected = (i == selected)
            draw_bottle(screen, x, y, colors, selected=is_selected)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
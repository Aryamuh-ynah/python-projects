import pygame
import sys
from config import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Color Sort Puzzle - Step 3")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 32)
small_font = pygame.font.SysFont("comicsansms", 24)

def draw_bottle(surface, x, y, colors, selected=False):
    if selected:
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

    # Liquid levels (bottom → top)
    for i, color_name in enumerate(colors):
        color = COLOR_MAP.get(color_name, GRAY)
        level_y = y + BOTTLE_HEIGHT - (i + 1) * LEVEL_HEIGHT
        level_rect = pygame.Rect(x + 4, level_y, BOTTLE_WIDTH - 8, LEVEL_HEIGHT - 2)
        pygame.draw.rect(surface, color, level_rect, border_radius=6)

def get_bottle_index(mouse_pos, bottle_positions):
    mx, my = mouse_pos
    for i, (x, y) in enumerate(bottle_positions):
        if x <= mx <= x + BOTTLE_WIDTH and y <= my <= y + BOTTLE_HEIGHT:
            return i
    return None

def can_pour(source, target):
    """Check if we can pour from source bottle to target bottle"""
    if not source:  # source is empty
        return False
    if len(target) >= MAX_LEVELS:  # target is full
        return False
    if not target:  # target is empty → always allowed
        return True
    # Top colors must match
    return source[-1] == target[-1]

def pour(source, target):
    """
    Pour as many units as possible from source to target.
    Returns the new source and target lists.
    """
    if not can_pour(source, target):
        return source, target

    color = source[-1]
    # How many units of this color are on top of source
    amount = 0
    for c in reversed(source):
        if c == color:
            amount += 1
        else:
            break

    # How much space is left in target
    space = MAX_LEVELS - len(target)
    pour_amount = min(amount, space)

    # Perform the pour
    for _ in range(pour_amount):
        target.append(source.pop())

    return source, target

def main():
    # Example level (bottom → top)
    bottles = [
        ["red", "blue", "green", "yellow"],
        ["blue", "red"],
        ["green", "yellow", "blue"],
        [],
        ["orange", "purple", "pink"],
        ["cyan", "orange"],
    ]

    # Bottle positions
    start_x = 80
    gap = 40
    bottle_y = 220
    bottle_positions = []
    for i in range(len(bottles)):
        x = start_x + i * (BOTTLE_WIDTH + gap)
        bottle_positions.append((x, bottle_y))

    selected = None

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = get_bottle_index(event.pos, bottle_positions)

                if clicked is not None:
                    if selected is None:
                        # Select source bottle (only if it has liquid)
                        if bottles[clicked]:
                            selected = clicked
                    elif selected == clicked:
                        # Deselect
                        selected = None
                    else:
                        # Try to pour
                        source = bottles[selected]
                        target = bottles[clicked]

                        if can_pour(source, target):
                            new_source, new_target = pour(source[:], target[:])  # copy lists
                            bottles[selected] = new_source
                            bottles[clicked] = new_target

                        selected = None  # always deselect after attempt

        # ========== DRAW ==========
        screen.fill(BACKGROUND)

        # Title
        title = font.render("Color Sort Puzzle", True, WHITE)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 30))

        # Instruction
        if selected is None:
            text = "Click a bottle to select"
            color = (180, 180, 180)
        else:
            text = "Click another bottle to pour"
            color = (255, 255, 100)
        instruction = small_font.render(text, True, color)
        screen.blit(instruction, (WINDOW_WIDTH // 2 - instruction.get_width() // 2, 80))

        # Draw bottles
        for i, colors in enumerate(bottles):
            x, y = bottle_positions[i]
            draw_bottle(screen, x, y, colors, selected=(i == selected))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
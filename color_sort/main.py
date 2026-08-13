import pygame
import sys
import copy
import random
from config import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Color Sort Puzzle")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 32)
small_font = pygame.font.SysFont("comicsansms", 24)
big_font = pygame.font.SysFont("comicsansms", 48)

# ====================== LEVEL SETTINGS ======================
# (number_of_colors, number_of_empty_bottles)
LEVEL_CONFIG = [
    (2, 2),   # Level 1 - Easy
    (4, 2),   # Level 2
    (4, 2),   # Level 3
    (6, 2),   # Level 4
    (8, 2),   # Level 5
]

ALL_COLORS = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "cyan"]

def generate_level(num_colors, num_empty):
    """Generate a random but solvable level"""
    colors = ALL_COLORS[:num_colors]
    
    # Create all color units (MAX_LEVELS of each color)
    units = []
    for color in colors:
        units.extend([color] * MAX_LEVELS)
    
    # Shuffle the units
    random.shuffle(units)
    
    # Create bottles
    total_bottles = num_colors + num_empty
    bottles = [[] for _ in range(total_bottles)]
    
    # Distribute the units randomly into the non-empty bottles
    bottle_indices = list(range(num_colors))  # only fill first num_colors bottles
    random.shuffle(bottle_indices)
    
    i = 0
    for unit in units:
        # Find a bottle that still has space
        while len(bottles[bottle_indices[i % num_colors]]) >= MAX_LEVELS:
            i += 1
        bottles[bottle_indices[i % num_colors]].append(unit)
        i += 1
    
    # Final shuffle of bottle order
    random.shuffle(bottles)
    
    return bottles

def draw_bottle(surface, x, y, colors, selected=False):
    if selected:
        glow_rect = pygame.Rect(x - 8, y - 8, BOTTLE_WIDTH + 16, BOTTLE_HEIGHT + 16)
        pygame.draw.rect(surface, (255, 255, 100), glow_rect, border_radius=16)

    body_rect = pygame.Rect(x, y + BOTTLE_NECK_HEIGHT, BOTTLE_WIDTH, BOTTLE_HEIGHT - BOTTLE_NECK_HEIGHT)
    pygame.draw.rect(surface, WHITE, body_rect, border_radius=12)
    pygame.draw.rect(surface, BLACK, body_rect, 3, border_radius=12)

    neck_x = x + (BOTTLE_WIDTH - BOTTLE_NECK_WIDTH) // 2
    neck_rect = pygame.Rect(neck_x, y, BOTTLE_NECK_WIDTH, BOTTLE_NECK_HEIGHT + 10)
    pygame.draw.rect(surface, WHITE, neck_rect, border_radius=6)
    pygame.draw.rect(surface, BLACK, neck_rect, 3, border_radius=6)

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
    if not source:
        return False
    if len(target) >= MAX_LEVELS:
        return False
    if not target:
        return True
    return source[-1] == target[-1]

def pour(source, target):
    if not can_pour(source, target):
        return source, target

    color = source[-1]
    amount = 0
    for c in reversed(source):
        if c == color:
            amount += 1
        else:
            break

    space = MAX_LEVELS - len(target)
    pour_amount = min(amount, space)

    for _ in range(pour_amount):
        target.append(source.pop())

    return source, target

def is_win(bottles):
    for bottle in bottles:
        if len(bottle) == 0:
            continue
        if len(bottle) != MAX_LEVELS or len(set(bottle)) > 1:
            return False
    return True

def draw_button(surface, text, x, y, width, height, active=True):
    color = (70, 130, 180) if active else (80, 80, 80)
    pygame.draw.rect(surface, color, (x, y, width, height), border_radius=10)
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2, border_radius=10)
    
    txt = small_font.render(text, True, WHITE)
    surface.blit(txt, (x + width//2 - txt.get_width()//2, y + height//2 - txt.get_height()//2))
    return pygame.Rect(x, y, width, height)

def get_bottle_positions(num_bottles):
    total_width = num_bottles * BOTTLE_WIDTH + (num_bottles - 1) * 30
    start_x = max(20, (WINDOW_WIDTH - total_width) // 2)
    bottle_y = 230
    positions = []
    for i in range(num_bottles):
        x = start_x + i * (BOTTLE_WIDTH + 30)
        positions.append((x, bottle_y))
    return positions

def main():
    current_level = 0
    num_colors, num_empty = LEVEL_CONFIG[current_level]
    bottles = generate_level(num_colors, num_empty)
    moves = 0
    history = []

    bottle_positions = get_bottle_positions(len(bottles))
    selected = None
    won = False
    level_complete = False

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart current level (new random)
                    num_colors, num_empty = LEVEL_CONFIG[current_level]
                    bottles = generate_level(num_colors, num_empty)
                    selected = None
                    won = False
                    level_complete = False
                    moves = 0
                    history = []
                    bottle_positions = get_bottle_positions(len(bottles))

                if event.key == pygame.K_n:  # Next level
                    if current_level < len(LEVEL_CONFIG) - 1:
                        current_level += 1
                        num_colors, num_empty = LEVEL_CONFIG[current_level]
                        bottles = generate_level(num_colors, num_empty)
                        selected = None
                        won = False
                        level_complete = False
                        moves = 0
                        history = []
                        bottle_positions = get_bottle_positions(len(bottles))

                if event.key == pygame.K_u and history and not won:
                    bottles = history.pop()
                    moves = max(0, moves - 1)
                    selected = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                # Undo button
                undo_rect = pygame.Rect(WINDOW_WIDTH - 140, 25, 110, 40)
                if undo_rect.collidepoint(mouse_pos) and history and not won:
                    bottles = history.pop()
                    moves = max(0, moves - 1)
                    selected = None
                    continue

                # Next Level button
                if level_complete:
                    next_rect = pygame.Rect(WINDOW_WIDTH//2 - 80, WINDOW_HEIGHT//2 + 80, 160, 45)
                    if next_rect.collidepoint(mouse_pos):
                        if current_level < len(LEVEL_CONFIG) - 1:
                            current_level += 1
                            num_colors, num_empty = LEVEL_CONFIG[current_level]
                            bottles = generate_level(num_colors, num_empty)
                            selected = None
                            won = False
                            level_complete = False
                            moves = 0
                            history = []
                            bottle_positions = get_bottle_positions(len(bottles))
                        continue

                if not won and not level_complete:
                    clicked = get_bottle_index(mouse_pos, bottle_positions)

                    if clicked is not None:
                        if selected is None:
                            if bottles[clicked]:
                                selected = clicked
                        elif selected == clicked:
                            selected = None
                        else:
                            source = bottles[selected]
                            target = bottles[clicked]

                            if can_pour(source, target):
                                history.append(copy.deepcopy(bottles))
                                new_source, new_target = pour(source[:], target[:])
                                bottles[selected] = new_source
                                bottles[clicked] = new_target
                                moves += 1

                                if is_win(bottles):
                                    won = True
                                    level_complete = True

                            selected = None

        # ========== DRAW ==========
        screen.fill(BACKGROUND)

        title = font.render(f"Color Sort - Level {current_level + 1}", True, WHITE)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 20))

        moves_text = small_font.render(f"Moves: {moves}", True, (200, 200, 200))
        screen.blit(moves_text, (30, 30))

        can_undo = len(history) > 0 and not won
        draw_button(screen, "Undo (U)", WINDOW_WIDTH - 140, 25, 110, 40, active=can_undo)

        if level_complete:
            text = "Level Complete!"
            color = (100, 255, 100)
        elif selected is None:
            text = "Click a bottle to select"
            color = (180, 180, 180)
        else:
            text = "Click another bottle to pour"
            color = (255, 255, 100)

        instruction = small_font.render(text, True, color)
        screen.blit(instruction, (WINDOW_WIDTH // 2 - instruction.get_width() // 2, 70))

        for i, colors in enumerate(bottles):
            x, y = bottle_positions[i]
            draw_bottle(screen, x, y, colors, selected=(i == selected))

        if level_complete:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            if current_level == len(LEVEL_CONFIG) - 1:
                win_text = big_font.render("YOU BEAT THE GAME!", True, (100, 255, 120))
            else:
                win_text = big_font.render("LEVEL COMPLETE!", True, (100, 255, 120))

            screen.blit(win_text, (WINDOW_WIDTH//2 - win_text.get_width()//2, WINDOW_HEIGHT//2 - 50))

            if current_level < len(LEVEL_CONFIG) - 1:
                draw_button(screen, "Next Level", WINDOW_WIDTH//2 - 80, WINDOW_HEIGHT//2 + 80, 160, 45)
            else:
                restart_text = small_font.render("Press R to play again", True, WHITE)
                screen.blit(restart_text, (WINDOW_WIDTH//2 - restart_text.get_width()//2, WINDOW_HEIGHT//2 + 50))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
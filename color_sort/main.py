import pygame
import sys
import copy
from config import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Color Sort Puzzle")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 32)
small_font = pygame.font.SysFont("comicsansms", 24)
big_font = pygame.font.SysFont("comicsansms", 48)

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
    """
    Win only when every non-empty bottle is completely full
    with a single color.
    """
    for bottle in bottles:
        if len(bottle) == 0:
            continue
        # Must be full AND all same color
        if len(bottle) != MAX_LEVELS or len(set(bottle)) > 1:
            return False
    return True

def create_level():
    return [
        ["red", "blue", "green", "red"],
        ["blue", "green", "yellow", "blue"],
        ["green", "yellow", "red", "yellow"],
        ["yellow", "red", "blue", "green"],
        [],
        [],
    ]

def draw_button(surface, text, x, y, width, height, active=True):
    color = (70, 130, 180) if active else (80, 80, 80)
    pygame.draw.rect(surface, color, (x, y, width, height), border_radius=10)
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2, border_radius=10)
    
    txt = small_font.render(text, True, WHITE)
    surface.blit(txt, (x + width//2 - txt.get_width()//2, y + height//2 - txt.get_height()//2))
    return pygame.Rect(x, y, width, height)

def main():
    bottles = create_level()
    moves = 0
    history = []               # for undo

    start_x = 80
    gap = 40
    bottle_y = 220
    bottle_positions = []
    for i in range(len(bottles)):
        x = start_x + i * (BOTTLE_WIDTH + gap)
        bottle_positions.append((x, bottle_y))

    selected = None
    won = False

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    bottles = create_level()
                    selected = None
                    won = False
                    moves = 0
                    history = []
                if event.key == pygame.K_u and history and not won:  # Undo with keyboard
                    bottles = history.pop()
                    moves = max(0, moves - 1)
                    selected = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                # Check Undo button
                undo_rect = pygame.Rect(WINDOW_WIDTH - 140, 25, 110, 40)
                if undo_rect.collidepoint(mouse_pos) and history and not won:
                    bottles = history.pop()
                    moves = max(0, moves - 1)
                    selected = None
                    continue

                if not won:
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
                                # Save state before pouring
                                history.append(copy.deepcopy(bottles))

                                new_source, new_target = pour(source[:], target[:])
                                bottles[selected] = new_source
                                bottles[clicked] = new_target
                                moves += 1

                                if is_win(bottles):
                                    won = True

                            selected = None

        # ========== DRAW ==========
        screen.fill(BACKGROUND)

        # Title
        title = font.render("Color Sort Puzzle", True, WHITE)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 25))

        # Moves
        moves_text = small_font.render(f"Moves: {moves}", True, (200, 200, 200))
        screen.blit(moves_text, (30, 30))

        # Undo Button
        can_undo = len(history) > 0 and not won
        draw_button(screen, "Undo (U)", WINDOW_WIDTH - 140, 25, 110, 40, active=can_undo)

        # Instruction / Win message
        if won:
            text = "YOU WIN!  Press R to Restart"
            color = (100, 255, 100)
        elif selected is None:
            text = "Click a bottle to select"
            color = (180, 180, 180)
        else:
            text = "Click another bottle to pour"
            color = (255, 255, 100)

        instruction = small_font.render(text, True, color)
        screen.blit(instruction, (WINDOW_WIDTH // 2 - instruction.get_width() // 2, 90))

        # Draw bottles
        for i, colors in enumerate(bottles):
            x, y = bottle_positions[i]
            draw_bottle(screen, x, y, colors, selected=(i == selected))

        # Win overlay
        if won:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            win_text = big_font.render("YOU WIN!", True, (100, 255, 120))
            screen.blit(win_text, (WINDOW_WIDTH//2 - win_text.get_width()//2, WINDOW_HEIGHT//2 - 40))

            restart_text = small_font.render("Press R to play again", True, WHITE)
            screen.blit(restart_text, (WINDOW_WIDTH//2 - restart_text.get_width()//2, WINDOW_HEIGHT//2 + 30))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
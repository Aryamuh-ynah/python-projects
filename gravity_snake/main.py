# main.py

import pygame
import sys
from config import *
from snake import Snake
from food import Food
from gravity import Gravity

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gravity Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 26)
big_font = pygame.font.SysFont("consolas", 48)

def draw_grid(screen):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))

def main():
    snake = Snake((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    food = Food(snake.body)
    gravity = Gravity()
    score = 0
    game_over = False

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -CELL_SIZE))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, CELL_SIZE))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-CELL_SIZE, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((CELL_SIZE, 0))
                    elif event.key == pygame.K_SPACE:
                        gravity.rotate()
                else:
                    if event.key == pygame.K_r:
                        # Restart
                        snake = Snake((WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                        food = Food(snake.body)
                        gravity = Gravity()
                        score = 0
                        game_over = False

        if not game_over:
            new_head = snake.move()

            # Wall collision
            if (new_head[0] < 0 or new_head[0] >= WINDOW_WIDTH or
                new_head[1] < 0 or new_head[1] >= WINDOW_HEIGHT or
                snake.check_self_collision()):
                game_over = True
            else:
                # Eat food
                if new_head == food.position:
                    snake.grow_snake()
                    score += 1
                    food = Food(snake.body)

        # ========== DRAW ==========
        screen.fill(BLACK)
        draw_grid(screen)

        food.draw(screen)
        snake.draw(screen)

        # UI
        score_text = font.render(f"Score: {score}", True, YELLOW)
        screen.blit(score_text, (15, 12))

        grav_text = font.render(f"Gravity: {gravity.get_name()}  (Space)", True, ORANGE)
        screen.blit(grav_text, (15, 45))

        if game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            text = big_font.render("GAME OVER", True, RED)
            screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, WINDOW_HEIGHT//2 - 60))

            restart = font.render("Press R to Restart", True, WHITE)
            screen.blit(restart, (WINDOW_WIDTH//2 - restart.get_width()//2, WINDOW_HEIGHT//2 + 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
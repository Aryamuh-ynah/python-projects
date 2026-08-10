import pygame
import random
import sys

pygame.init()

# ====================== CONFIG ======================
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
CELL_SIZE = 20
FPS = 12

# Colors
BLACK = (15, 15, 20)
DARK_GRAY = (30, 30, 40)
WHITE = (240, 240, 240)
GREEN = (50, 220, 100)
RED = (220, 60, 80)
BLUE = (60, 140, 255)
YELLOW = (255, 220, 50)
PURPLE = (180, 80, 255)

# ====================== SETUP ======================
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gravity Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 28)
big_font = pygame.font.SysFont("consolas", 48)

# ====================== SNAKE & FOOD ======================
def random_food(snake):
    while True:
        x = random.randrange(0, WINDOW_WIDTH // CELL_SIZE) * CELL_SIZE
        y = random.randrange(0, WINDOW_HEIGHT // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake:
            return (x, y)

snake = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]
direction = (CELL_SIZE, 0)   # starting moving right
food = random_food(snake)
score = 0
game_over = False

# ====================== MAIN LOOP ======================
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)
            else:
                if event.key == pygame.K_r:          # Restart
                    snake = [(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)]
                    direction = (CELL_SIZE, 0)
                    food = random_food(snake)
                    score = 0
                    game_over = False

    if not game_over:
        # Move snake
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        # Wall collision
        if (new_head[0] < 0 or new_head[0] >= WINDOW_WIDTH or
            new_head[1] < 0 or new_head[1] >= WINDOW_HEIGHT or
            new_head in snake):
            game_over = True
        else:
            snake.insert(0, new_head)

            # Eat food
            if new_head == food:
                score += 1
                food = random_food(snake)
            else:
                snake.pop()

    # ====================== DRAW ======================
    screen.fill(BLACK)

    # Grid (subtle)
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, DARK_GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, DARK_GRAY, (0, y), (WINDOW_WIDTH, y))

    # Food
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

    # Snake
    for i, segment in enumerate(snake):
        color = GREEN if i == 0 else BLUE
        pygame.draw.rect(screen, color, (segment[0], segment[1], CELL_SIZE - 1, CELL_SIZE - 1))

    # Score
    score_text = font.render(f"Score: {score}", True, YELLOW)
    screen.blit(score_text, (15, 12))

    # Game Over
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
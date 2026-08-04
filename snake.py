import pygame
import random

pygame.init()

# Colors
red = (255, 0, 0)
blue = (0, 0, 200)
grey = (200, 200, 200)
green = (0, 255, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)

win_width = 900
win_height = 600

window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Snake Game")

sn = 10
sn_speed = 15

clock = pygame.time.Clock()

font = pygame.font.SysFont("comicsansms", 35)
score_font = pygame.font.SysFont("comicsansms", 25)


def user_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    window.blit(value, [10, 10])


def game_snake(sn, sn_len_list):
    for x in sn_len_list:
        pygame.draw.rect(window, blue, [x[0], x[1], sn, sn])


def message(text, color):
    mesg = font.render(text, True, color)
    window.blit(mesg, [win_width / 6, win_height / 3])


def game_loop():
    game_over = False
    game_close = False

    x1 = win_width / 2
    y1 = win_height / 2
    x1_change = 0
    y1_change = 0

    sn_length = 1
    sn_list = []

    foodx = round(random.randrange(0, win_width - sn) / 10.0) * 10.0
    foody = round(random.randrange(0, win_height - sn) / 10.0) * 10.0

    while not game_over:

        # ---------- Game Over Screen ----------
        while game_close:
            window.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            user_score(sn_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()  # Restart the game

        # ---------- Event Handling ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -sn
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = sn
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -sn
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = sn
                    x1_change = 0

        # ---------- Boundary Check ----------
        if x1 >= win_width or x1 < 0 or y1 >= win_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        window.fill(grey)
        pygame.draw.rect(window, green, [foodx, foody, sn, sn])

        # Update snake body
        snake_head = [x1, y1]
        sn_list.append(snake_head)

        if len(sn_list) > sn_length:
            del sn_list[0]

        # ---------- Self Collision ----------
        for segment in sn_list[:-1]:
            if segment == snake_head:
                game_close = True

        game_snake(sn, sn_list)
        user_score(sn_length - 1)

        pygame.display.update()

        # ---------- Food Collision ----------
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, win_width - sn) / 10.0) * 10.0
            foody = round(random.randrange(0, win_height - sn) / 10.0) * 10.0
            sn_length += 1

        clock.tick(sn_speed)

    pygame.quit()
    quit()


game_loop()
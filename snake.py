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
white = (255, 255, 255)
dark_grey = (40, 40, 40)

win_width = 900
win_height = 600

window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Snake Game")

sn = 10
sn_speed = 15
border_thickness = 10          # Border thickness

clock = pygame.time.Clock()

font = pygame.font.SysFont("comicsansms", 35)
score_font = pygame.font.SysFont("comicsansms", 25)


def user_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    window.blit(value, [20, 15])


def game_snake(sn, sn_len_list):
    for x in sn_len_list:
        pygame.draw.rect(window, blue, [x[0], x[1], sn, sn])


def message(text, color):
    mesg = font.render(text, True, color)
    window.blit(mesg, [win_width / 6, win_height / 3])


def draw_border():
    # Outer border
    pygame.draw.rect(window, white, [0, 0, win_width, win_height], border_thickness)
    
    # Optional: darker inner line for better look
    pygame.draw.rect(window, dark_grey, 
                     [border_thickness, border_thickness, 
                      win_width - 2*border_thickness, 
                      win_height - 2*border_thickness], 2)


def game_loop():
    game_over = False
    game_close = False

    x1 = win_width / 2
    y1 = win_height / 2
    x1_change = 0
    y1_change = 0

    sn_length = 1
    sn_list = []

    # Food should spawn inside the border
    foodx = round(random.randrange(border_thickness, win_width - sn - border_thickness) / 10.0) * 10.0
    foody = round(random.randrange(border_thickness, win_height - sn - border_thickness) / 10.0) * 10.0

    while not game_over:

        # ---------- Game Over Screen ----------
        while game_close:
            window.fill(black)
            draw_border()
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
                        game_loop()

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

        # ---------- Boundary Check (with border) ----------
        if (x1 >= win_width - border_thickness or 
            x1 < border_thickness or 
            y1 >= win_height - border_thickness or 
            y1 < border_thickness):
            game_close = True

        x1 += x1_change
        y1 += y1_change

        window.fill(grey)
        draw_border()                                   # Draw the border every frame
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
            foodx = round(random.randrange(border_thickness, win_width - sn - border_thickness) / 10.0) * 10.0
            foody = round(random.randrange(border_thickness, win_height - sn - border_thickness) / 10.0) * 10.0
            sn_length += 1

        clock.tick(sn_speed)

    pygame.quit()
    quit()


game_loop()
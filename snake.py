import pygame
import random
import time

pygame.init()
red = (255, 0, 0)
blue = (0, 0, 200)
grey = (200, 200, 200)
green = (0, 255, 0)
yellow = (255, 255, 0)

win_width = 600
win_height = 400

window = pygame.display.set_mode((win_width, win_height))
# time.sleep(5)

pygame.display.set_caption("Snake Game")

sn = 10
sn_speed = 15

score = 0

# fonts = pygame.font.get_fonts()

# print(fonts) #print all available fonts
font = pygame.font.SysFont("comicsansms", 35)
score_font = pygame.font.SysFont("notosansmonocjksc", 25)

def user_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    window.blit(value, [0, 0])

def game_snake():
    pass

def game_loop():
    global score
    game_over = False
    x1 = win_width/2
    y2 = win_height/2
    x1_change = 0
    y1_change = 0

    sn_length = 1

    sn_list = []

    foodx = round(random.randrange(0, win_width - sn) / 10.0) * 10.0
    foody = round(random.randrange(0, win_height - sn) / 10.0) * 10.0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -sn
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = sn
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -sn
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = sn
                    x1_change = 0

        if x1 >= win_width or x1 < 0 or y2 >= win_height or y2 < 0:
            game_over = True

        x1 += x1_change
        y2 += y1_change

        window.fill(grey)
        pygame.draw.rect(window, green, [foodx, foody, sn, sn])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y2)
        sn_list.append(snake_head)

        if len(sn_list) > sn_length:
            del sn_list[0]

        for segment in sn_list[:-1]:
            if segment == snake_head:
                game_over = True

        for segment in sn_list:
            pygame.draw.rect(window, blue, [segment[0], segment[1], sn, sn])

        user_score(score)
        pygame.display.update()

        if x1 == foodx and y2 == foody:
            foodx = round(random.randrange(0, win_width - sn) / 10.0) * 10.0
            foody = round(random.randrange(0, win_height - sn) / 10.0) * 10.0
            sn_length += 1
            score += 10

        time.sleep(0.05)


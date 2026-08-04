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

def game_snake(sn, sn_len_list):
    for x in sn_len_list:
        pygame.draw.rect(window, blue, [x[0], x[1], sn, sn])


def msg(text, color):
    mesg = font.render(text, True, color)
    window.blit(mesg, [win_width / 6, win_height / 3])

def loop():
    gameOver = False
    gameCount = False

    x1 = win_width / 2
    y1 = win_height / 2
    x1_change = 0
    y1_change = 0

    sn_length = 1
    sn_len_list = []

    foodx = round(random.randrange(0, win_width - sn) / 10.0) * 10.0
    foody = round(random.randrange(0, win_height - sn) / 10.0) * 10.0

    while gameClose == True:
        window.fill(gray)
        msg("You Lost! Press C-Play Again or Q-Quit", red)
        user_score(sn_length - 1)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEDOWN:
                if event.key == pygame.K_q:
                    gameOver = True
                    gameClose = False
                if event.key == pygame.K_c:
                    loop()

        for event in pygame.event.get():
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


        if x1 >= win_width or x1 < 0 or y1 >= win_height or y1 < 0:
            gameClose = True

        x1 += x1_change
        y1 += y1_change

        window.fill(grey)
        pygame.draw.rect(window, green, [foodx, foody, sn, sn])

        sn_size = []
        sn_size.append(x1)
        sn_size.append(y1)
        sn_len_list.append(sn_size)

        if len(sn_len_list) > sn_length: 
            del sn_len_list[0]

        game_snake(sn, sn_len_list)
        user_score(sn_length - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, win_width - sn) / 10.0) * 10.0
            foody = round(random.randrange(0, win_height - sn) / 10.0) * 10.0
            sn_length += 1

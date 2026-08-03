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
font = pygame.font.Sysfont("comicsansms", 35)
score_font = pygame.font.Sysfont("notosansmonocjksc", 25)
import pygame
import sys
from settings import *
from level import Level
from game_data import level_0

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))  # Height / width
pygame.display.set_caption(title="Pirate Hunt")
clock = pygame.time.Clock()
level = Level(level_0, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("gray")
    level.run()

    pygame.display.update()
    clock.tick(60)

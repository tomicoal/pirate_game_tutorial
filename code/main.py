import pygame
import sys
from settings import *
from level import Level
from game_data import level_0_tiles
from overworld import Overworld


class Game:
    def __init__(self):
        self.max_level = 2
        self.overworld = Overworld(0, self.max_level, screen)

    def run(self):
        self.overworld.run()



pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))  # Height / width
pygame.display.set_caption(title="Pirate Hunt")
clock = pygame.time.Clock()
level = Level(level_0_tiles, screen)
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("blue")
    game.run()

    pygame.display.update()
    clock.tick(60)

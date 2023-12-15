import pygame
import sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI


class Game:
    def __init__(self):

        # game attributes
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100
        self.coins_collected = 0

        # audio
        self.level_bg_music = pygame.mixer.Sound('./audio/level_music.wav')
        self.overworld_music = pygame.mixer.Sound('./audio/overworld_music.wav')
        self.level_bg_music.set_volume(0.5)
        self.overworld_music.set_volume(0.5)

        # overworld creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.overworld_music.play(loops=-1)

        # UI
        self.ui = UI(screen)


    def create_level(self, current_level, ):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.level_bg_music.play(loops=-1)
        self.overworld_music.stop()


    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        self.level_bg_music.stop()
        self.overworld_music.play(loops=-1)


    def change_coins(self, amount):
        self.coins_collected += amount

    def change_health(self, amount):
        self.current_health += amount

    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 100
            self.coins_collected = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.status = 'overworld'
            self.level_bg_music.stop()
            self.overworld_music.play(loops=-1)


    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins_collected)
            self.check_game_over()


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))  # Height / width
pygame.display.set_caption(title="Pirate Run")
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    game.run()


    pygame.display.update()
    clock.tick(60)

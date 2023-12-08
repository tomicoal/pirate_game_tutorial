import pygame


class UI:
    def __init__(self, surface):
        # setup
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load('./graphics/ui/health_bar.png').convert_alpha()
        self.health_bar_topleft = (54, 39)
        self.bar_max_width = 152
        self.bar_height = 4

        # coins
        self.coin = pygame.image.load('./graphics/ui/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(50, 61))
        self.font = pygame.font.Font('./graphics/ui/ARCADEPI.TTF', 30)


    def show_health(self, current_health, full_health):
        self.display_surface.blit(self.health_bar, (20, 10))
        current_health_ratio = current_health/full_health
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect(self.health_bar_topleft, (current_bar_width ,self.bar_height))
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect)

    def show_coins(self, coin_amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coins_text_image = self.font.render(str(coin_amount), False, '#33323D')
        x = self.coin_rect.right + 4
        coins_text_rect = coins_text_image.get_rect(midleft=(x, self.coin_rect.centery))
        self.display_surface.blit(coins_text_image, coins_text_rect)

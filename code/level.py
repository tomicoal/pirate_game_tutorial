import pygame
from tiles import StaticTile, Crate, CoinTile, PalmsTile
from settings import tile_size, screen_with
from player import Player
from particles import ParticleEffect
from support import import_csv_layout, import_cut_graphics


class Level:
    def __init__(self, level_data, surface):

        # General setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = 0

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates
        crates_layout = import_csv_layout(level_data['crates'])
        self.crates_sprite = self.create_tile_group(crates_layout, 'crates')

        # coins
        coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprite = self.create_tile_group(coins_layout, 'coins')

        # foreground palms
        fg_palms_layout = import_csv_layout(level_data['fg_palms'])
        self.fg_palms_sprite = self.create_tile_group(fg_palms_layout, 'fg_palms')

        # Dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False


    # def create_jump_particles(self, pos):
    #     if self.player.sprite.facing_right:
    #         pos -= pygame.math.Vector2(10,-3)
    #     else:
    #         pos += pygame.math.Vector2(10, 3)
    #     jump_particle_sprite = ParticleEffect(pos, "jump")
    #     self.dust_sprite.add(jump_particle_sprite)


    # def get_player_on_ground(self):
    #     if self.player.sprite.on_ground:
    #         self.player_on_ground = True
    #     else:
    #         self.player_on_ground = False


    # def create_landing_dust(self):
    #     if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
    #         if self.player.sprite.facing_right:
    #             offset = pygame.math.Vector2(10, 0)
    #         else:
    #             offset = pygame.math.Vector2(-10, 0)
    #         fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, "land")
    #         self.dust_sprite.add(fall_dust_particle)


    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                # !! values in csv are strings !!
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    # static
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('./graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('./graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    # animated
                    if type == 'coins':
                        if val == "0":
                            sprite = CoinTile(tile_size, x, y, './graphics/coins/gold')
                        else:
                            sprite = CoinTile(tile_size, x, y, './graphics/coins/silver')

                    if type == 'fg_palms':
                        sprite = PalmsTile(tile_size, x, y, './graphics/terrain/palm_small')

                    sprite_group.add(sprite)

        return sprite_group


    # def scroll_x(self):
    #     player = self.player.sprite
    #     player_x = player.rect.centerx
    #     direction_x = player.direction.x
    #
    #     if player_x < screen_with/5 and direction_x < 0:
    #         self.world_shift = 8
    #         player.speed = 0
    #     elif player_x > (screen_with/5)*4 and direction_x > 0:
    #         self.world_shift = -8
    #         player.speed = 0
    #     else:
    #         self.world_shift = 0
    #         player.speed = 8

    # def horizontal_movement_collision(self):
    #     player = self.player.sprite
    #     player.rect.x += player.direction.x * player.speed
    #
    #     for sprite in self.tiles.sprites():
    #         if sprite.rect.colliderect(player.rect):
    #             if player.direction.x < 0:
    #                 player.rect.left = sprite.rect.right
    #                 player.on_left = True
    #                 self.current_x = player.rect.left
    #             elif player.direction.x > 0:
    #                 player.rect.right = sprite.rect.left
    #                 player.on_right = True
    #                 self.current_x = player.rect.right
    #
    #     if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
    #         player.on_left = False
    #     if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
    #         player.on_right = False


    # def vertical_movement_collision(self):
    #     player = self.player.sprite
    #     player.apply_gravity()
    #
    #     for sprite in self.tiles.sprites():
    #         if sprite.rect.colliderect(player.rect):
    #             if player.direction.y > 0:
    #                 player.rect.bottom = sprite.rect.top
    #                 player.direction.y = 0
    #                 player.on_ground = True
    #             elif player.direction.y < 0:
    #                 player.rect.top = sprite.rect.bottom
    #                 player.direction.y = 0
    #                 player.on_ceiling = True
    #
    #         if player.on_ground and player.direction.y > 0 or player.direction.y > player.gravity:
    #             player.on_ground = False
    #         if player.on_ceiling and player.direction.y > 0:
    #             player.on_ceiling = False


    def run(self):
        # run the entire game / level
        # #Dust
        # self.dust_sprite.update(self.world_shift)
        # self.dust_sprite.draw(self.display_surface)

        # terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
        # grass
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)
        # crates
        self.crates_sprite.draw(self.display_surface)
        self.crates_sprite.update(self.world_shift)
        # coins
        self.coins_sprite.draw(self.display_surface)
        self.coins_sprite.update(self.world_shift)
        # palms
        self. fg_palms_sprite.draw(self.display_surface)
        self.fg_palms_sprite.update(self.world_shift)

        # Player
        # self.player.update()
        # self.horizontal_movement_collision()
        # self.get_player_on_ground()
        # self.vertical_movement_collision()
        # self.create_landing_dust()
        # self.player.draw(self.display_surface)

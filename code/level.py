import pygame
from tiles import Tile, StaticTile, Crate, CoinTile, PalmsTile
from enemy import Enemy
from settings import tile_size, screen_height, screen_width
from player import Player
from particles import ParticleEffect
from support import import_csv_layout, import_cut_graphics
from decoration import Sky, Water, Clouds
from game_data import levels


class Level:
    def __init__(self, current_level, surface, create_overworld):

        # General setup
        self.display_surface = surface

        # overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        level_content = level_data['content']
        self.new_max_level = level_data['unlock']

        self.world_shift = 0
        self.current_x = None

        # player setup
        player_layout = import_csv_layout(level_content['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # terrain setup
        terrain_layout = import_csv_layout(level_content['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # grass setup
        grass_layout = import_csv_layout(level_content['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates
        crates_layout = import_csv_layout(level_content['crates'])
        self.crates_sprite = self.create_tile_group(crates_layout, 'crates')

        # coins
        coins_layout = import_csv_layout(level_content['coins'])
        self.coins_sprite = self.create_tile_group(coins_layout, 'coins')

        # foreground palms
        fg_palms_layout = import_csv_layout(level_content['fg_palms'])
        self.fg_palms_sprite = self.create_tile_group(fg_palms_layout, 'fg_palms')

        # background palms
        bg_palms_layout = import_csv_layout(level_content['bg_palms'])
        self.bg_palms_sprite = self.create_tile_group(bg_palms_layout, 'bg_palms')

        # enemies
        enemies_layout = import_csv_layout(level_content['enemies'])
        self.enemies_sprite = self.create_tile_group(enemies_layout, 'enemies')

        # constraint
        constraint_layout = import_csv_layout(level_content['constraints'])
        self.constraint_sprite = self.create_tile_group(constraint_layout, 'constraints')

        # decorations
        self.sky = Sky(7)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 40, level_width)
        self.clouds = Clouds(350, level_width, 30)

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, -3)
        else:
            pos += pygame.math.Vector2(10, 3)
        jump_particle_sprite = ParticleEffect(pos, "jump")
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 0)
            else:
                offset = pygame.math.Vector2(-10, 0)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, "land")
            self.dust_sprite.add(fall_dust_particle)

    def create_tile_group(self, layout, tile_type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                # !! values in csv are strings !!
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    # static
                    if tile_type == 'terrain':
                        terrain_tile_list = import_cut_graphics('./graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if tile_type == 'grass':
                        grass_tile_list = import_cut_graphics('./graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if tile_type == 'crates':
                        sprite = Crate(tile_size, x, y)

                    # animated
                    if tile_type == 'coins':
                        if val == "0":
                            sprite = CoinTile(tile_size, x, y, './graphics/coins/gold')
                        else:
                            sprite = CoinTile(tile_size, x, y, './graphics/coins/silver')

                    if tile_type == 'fg_palms':
                        if val == "0":
                            sprite = PalmsTile(tile_size, x, y, './graphics/terrain/palm_small', 38)
                        else:
                            sprite = PalmsTile(tile_size, x, y, './graphics/terrain/palm_large', 64)

                    if tile_type == 'bg_palms':
                        sprite = PalmsTile(tile_size, x, y, './graphics/terrain/palm_bg', 64)

                    if tile_type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if tile_type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                # !! values in csv are strings !!
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load('./graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemies_sprite.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprite, False):
                enemy.reverse()

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 3 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > (screen_width / 3) * 2 and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        collidable_sprites = (self.terrain_sprites.sprites() + self.crates_sprite.sprites()
                              + self.fg_palms_sprite.sprites())
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        collidable_sprites = (self.terrain_sprites.sprites() + self.crates_sprite.sprites()
                              + self.fg_palms_sprite.sprites())

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

            if player.on_ground and player.direction.y > 0 or player.direction.y > player.gravity:
                player.on_ground = False
            if player.on_ceiling and player.direction.y > 0:
                player.on_ceiling = False

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, 0)

    def check_finish(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.create_overworld(self.current_level, self.new_max_level)
        elif keys[pygame.K_ESCAPE]:
            self.create_overworld(self.current_level, 0)

    def run(self):
        # run the entire game / level
        self.input()
        self.check_death()
        self.check_finish()

        # decoration
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # background palms
        self.bg_palms_sprite.update(self.world_shift)
        self.bg_palms_sprite.draw(self.display_surface)

        # terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        # enemies
        self.enemies_sprite.update(self.world_shift)
        self.enemies_sprite.draw(self.display_surface)
        # constraints
        self.constraint_sprite.update(self.world_shift)
        # self.constraint_sprite.draw(self.display_surface)
        self.enemy_collision_reverse()
        # crates
        self.crates_sprite.update(self.world_shift)
        self.crates_sprite.draw(self.display_surface)
        # coins
        self.coins_sprite.update(self.world_shift)
        self.coins_sprite.draw(self.display_surface)
        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)
        # palms
        self.fg_palms_sprite.update(self.world_shift)
        self.fg_palms_sprite.draw(self.display_surface)
        # player sprites
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        self.scroll_x()

        # Dust
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # water decoration
        self.water.draw(self.display_surface, self.world_shift)

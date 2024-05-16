# This file was created by Ayden Jafari

# Final Goal: Create different levels, add speed power-up boost, more or bigger enemies going horizontally, health bar


import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path
import time

class Teleport(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.groups = game.all_sprites, game.teleport
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(NAVY)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        # Check for collision with player
        if pg.sprite.collide_rect(self, self.game.player):
            # Teleport the player up 3 spaces from their current position
            self.game.player.rect.y -= 3 * TILESIZE  # Move up 3 tiles
            self.game.player.teleported = True


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.groups = game.all_sprites, game.enemy
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(NEON)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 5
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.direction *= -1

        # Check for collision with player
        if pg.sprite.collide_rect(self, self.game.player):
            self.game.quit()  # Quit the game if collision occurs


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.groups = game.all_sprites, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(NEON)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 2
        self.direction = 1  

    def update(self):
        self.rect.y += self.speed * self.direction
        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.direction *= -1


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.groups = game.all_sprites, game.mob
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(NEON)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 2
        self.direction_x = 1  # Horizontal
        self.direction_y = 1  # Vertical

    def update(self):
        # Horizontal movement
        self.rect.x += self.speed * self.direction_x
        # Vertical movement
        self.rect.y += self.speed * self.direction_y
        #check boundaries
        if self.rect.bottom >= HEIGHT or self.rect.top <= 0:
            self.direction_y *= -1  # Reverse vertical direction
        #Check boundaries
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction_x *= -1  # Reverse horizontal direction

class Game:
    
    
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.start_time = time.time()
        self.time_limit = 90
        self.game_over = False

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        self.teleport = pg.sprite.Group()
        self.obstacle = pg.sprite.Group()
        self.mob = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)
                elif tile == 'C':
                    Coin(self, col, row)
                elif tile == 'O':
                    Obstacle(self, col, row)
                elif tile == 'E':
                    Enemy(self, col, row)
                elif tile == 'T':
                    Teleport(self, col, row)
                elif tile == 'M':
                    Mob(self, col, row)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            time_left = max(self.time_limit - (time.time() - self.start_time), 0)
            if time_left <= 0:
                self.restart_game()
            elif self.player.moneybag >= 99:
                self.win_game()
        self.game_over = True
        self.draw()

    def restart_game(self):
        self.start_time = time.time()
        self.player.moneybag = 0
        self.new()

    def win_game(self):
        self.playing = False
        self.game_over = True

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        if not self.game_over:
            self.all_sprites.update()
            self.obstacles.update()
            self.enemy.update()
            self.teleport.update()
            self.mob.update()
            if pg.sprite.spritecollideany(self.player, self.obstacles):
                self.restart_game()
            if pg.sprite.spritecollideany(self.player, self.mob):
                self.restart_game()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, BLACK, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, BLACK, (0, y), (WIDTH, y))

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x * TILESIZE, y * TILESIZE)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.obstacles.draw(self.screen)
        if not self.game_over:
            self.draw_text(self.screen, f"Score: {self.player.moneybag}", 32, RED, 1, 1)
            time_left = max(self.time_limit - (time.time() - self.start_time), 0)
            self.draw_text(self.screen, f"Time left: {int(time_left)}", 32, RED, 1, 2)
        else:
            self.draw_text(self.screen, "Game Over", 64, WHITE, WIDTH // 2, HEIGHT // 2)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()


# Start game
if __name__ == "__main__":
    g = Game()
    while True:
        g.new()
        g.run()



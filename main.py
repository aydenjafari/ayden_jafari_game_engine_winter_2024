import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path
import time

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.start_time = time.time()  # Timer start time
        self.time_limit = 45  # Time limit in seconds
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
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)

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
            elif self.player.moneybag >= 50:
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
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

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
        if not self.game_over:
            self.draw_text(self.screen, f"Score: {self.player.moneybag}", 32, WHITE, 1, 1)
            time_left = max(self.time_limit - (time.time() - self.start_time), 0)
            self.draw_text(self.screen, f"Time left: {int(time_left)}", 32, WHITE, 1, 2)
        else:
            if self.player.moneybag >= 50:
                self.draw_text(self.screen, "You Win!", 64, WHITE, WIDTH // 2, HEIGHT // 2)
            else:
                self.draw_text(self.scree

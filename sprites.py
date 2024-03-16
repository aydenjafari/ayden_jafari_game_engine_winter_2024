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
        self.time_limit = 30  # Time limit in seconds
        self.score = 0  # Player's score
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
            if self.score >= 55 or time.time() - self.start_time > self.time_limit:
                self.playing = False
        self.game_over = True
        self.draw()

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
            if self.score >= 55:
                self.draw_text(self.screen, "You Win!", 64, WHITE, WIDTH // 2, HEIGHT // 2)
            else:
                self.draw_text(self.screen, "Game Over", 64, WHITE, WIDTH // 2, HEIGHT // 2)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

# Instantiate the game
g = Game()
while True:
    g.new()
    g.run()



















#       # This file was created by Ayden Jafari
# import pygame as pg
# from settings import *

# class Player(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites
#         # init super class
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = pg.Surface((TILESIZE, TILESIZE))
#         self.image.fill(GREEN)
#         self.rect = self.image.get_rect()
#         self.vx, self.vy = 0, 0
#         self.x = x * TILESIZE
#         self.y = y * TILESIZE
#         self.moneybag = 0
    
#     def get_keys(self):
#         self.vx, self.vy = 0, 0
#         keys = pg.key.get_pressed()
#         if keys[pg.K_LEFT] or keys[pg.K_a]:
#             self.vx = -PLAYER_SPEED  
#         if keys[pg.K_RIGHT] or keys[pg.K_d]:
#             self.vx = PLAYER_SPEED  
#         if keys[pg.K_UP] or keys[pg.K_w]:
#             self.vy = -PLAYER_SPEED  
#         if keys[pg.K_DOWN] or keys[pg.K_s]:
#             self.vy = PLAYER_SPEED
#         if self.vx != 0 and self.vy != 0:
#             self.vx *= 0.7071
#             self.vy *= 0.7071

#     # def move(self, dx=0, dy=0):
#     #     if not self.collide_with_walls(dx, dy):
#     #         self.x += dx
#     #         self.y += dy

#     # def collide_with_walls(self, dx=0, dy=0):
#     #     for wall in self.game.walls:
#     #         if wall.x == self.x + dx and wall.y == self.y + dy:
#     #             return True
#     #     return False
            
#     def collide_with_walls(self, dir):
#         if dir == 'x':
#             hits = pg.sprite.spritecollide(self, self.game.walls, False)
#             if hits:
#                 if self.vx > 0:
#                     self.x = hits[0].rect.left - self.rect.width
#                 if self.vx < 0:
#                     self.x = hits[0].rect.right
#                 self.vx = 0
#                 self.rect.x = self.x
#         if dir == 'y':
#             hits = pg.sprite.spritecollide(self, self.game.walls, False)
#             if hits:
#                 if self.vy > 0:
#                     self.y = hits[0].rect.top - self.rect.height
#                 if self.vy < 0:
#                     self.y = hits[0].rect.bottom
#                 self.vy = 0
#                 self.rect.y = self.y
    
#     def collide_with_group(self, group, kill):
#         hits = pg.sprite.spritecollide(self, group, kill)
#         if hits:
#             if str(hits[0].__class__.__name__) == "Coin":
#                 self.moneybag += 1

#     def update(self):
#         self.get_keys()
#         self.x += self.vx * self.game.dt
#         self.y += self.vy * self.game.dt
#         self.rect.x = self.x
#         # add collision later
#         self.collide_with_walls('x')
#         self.rect.y = self.y
#         # add collision later
#         self.collide_with_walls('y')
#         self.collide_with_group(self.game.coins, True)
          
#         # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
#         # if coin_hits:
#         #     print("I got a coin")
        

 




# class Wall(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites, game.walls
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = pg.Surface((TILESIZE, TILESIZE))
#         self.image.fill(BLUE)
#         self.rect = self.image.get_rect()
#         self.x = x
#         self.y = y
#         self.rect.x = x * TILESIZE
#         self.rect.y = y * TILESIZE

# class Coin(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites, game.coins
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = pg.Surface((TILESIZE, TILESIZE))
#         self.image.fill(YELLOW)
#         self.rect = self.image.get_rect()
#         self.x = x
#         self.y = y
#         self.rect.x = x * TILESIZE
#         self.rect.y = y * TILESIZE  
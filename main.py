#This file was created by Ayden Jafari

#Import necessary libraries
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
        self.clock = pg.time.Clock() #creates clock and sets up frame rate
        self.load_data()
        self.start_time = time.time()  # should iniate timer
        self.time_limit = 60  # Timer begins with a minute
        self.game_over = False #tracks if game is over

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
        self.obstacles = pg.sprite.Group()  # Grouping obstacles and adding them to game
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'O':  # Add obstacle with letter O
                    Obstacle(self, col, row)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 #Keeps track of time and frames per sec
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

    def restart_game(self): #restart game if money is full or time is out
        self.start_time = time.time() #initiate timer after reset
        self.player.moneybag = 0 # reset moneybag
        self.new() #reset player

    def win_game(self): #game is won if player stops playing and money is 99
        self.playing = False
        self.game_over = True

    def quit(self): # game is quit
        pg.quit()
        sys.exit()

    def update(self):
        if not self.game_over:  # Only update if the game is still being playrd
            self.all_sprites.update()
            self.obstacles.update()

            # if player collides with obstacles reset money timer and player position
            if pg.sprite.spritecollideany(self.player, self.obstacles):
                self.restart_game()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, BLUE, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, RED, (0, y), (WIDTH, y))

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
        if not self.game_over: #if game is still being played each money adds 1 while each second decreases
            self.draw_text(self.screen, f"Score: {self.player.moneybag}", 32, RED, 1, 1)
            time_left = max(self.time_limit - (time.time() - self.start_time), 0)
            self.draw_text(self.screen, f"Time left: {int(time_left)}", 32, RED, 1, 2)
        else:
            self.draw_text(self.screen, "Game Over", 64, WHITE, WIDTH // 2, HEIGHT // 2)
        pg.display.flip() #if not game playing, reset game

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Assigning the groups for sprites
        self.groups = game.all_sprites, game.obstacles
        # Initialize obstacle
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # Creating filling for obstace
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # color
        self.image.fill(RED)
        # fill
        self.rect = self.image.get_rect()
        # position
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE 
        # speed
        self.speed = 2
        # initial direction
        self.direction = 1  

    # Update obstacle for change of direction
    def update(self):
        # Move vertically depending on speed and direction
        self.rect.y += self.speed * self.direction
        # if hits bottom make obstacle bounce 
        #basically reversing
        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.direction *= -1  # Change direction


# start game
g = Game()
while True:
    g.new()
    g.run()




#Sources are, OG Build, Scott, LeMaster Tech Youtube channel


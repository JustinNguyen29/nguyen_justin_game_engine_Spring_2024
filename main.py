# This file was created by Justin Nguyen

# importing libraries
import pygame as pg
from settings import *
from sprites import *
import sys
from random import randint
from os import path

# create a game class 
class Game:
    # initializing class
    def __init__(self):
        pg.init()

        # set the display to width WIDTH and height HEIGHT
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        # set caption
        pg.display.set_caption("My First Video Game")

        # timer for display
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500,100)
        self.running = True
        # later on we'll story game info with this
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        # 'r'     open for reading (default)
        # 'w'     open for writing, truncating the file first
        # 'x'     open for exclusive creation, failing if the file already exists
        # 'a'     open for writing, appending to the end of the file if it exists
        # 'b'     binary mode
        # 't'     text mode (default)
        # '+'     open a disk file for updating (reading and writing)
        # 'U'     universal newlines mode (deprecated)
        # below opens file for reading in text mode
        # with 
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)        

    def new(self):
        # makes sprites into a group
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        # makes player at x = 10 y = 10
        # self.player = Player(self, 10, 10)
        # adds the player to sprites
        # self.all_sprites.add(self.player)
        # newsted for loop to print walls
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 'c':
                    Coin(self, col, row)


    # run method
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            # this is input
            self.events()
            # this is processing
            self.update()
            # this is output
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def input(self):
        #print(self.clock.get_fps())
        pass

    # update function to update all sprites
    def update(self):
        self.all_sprites.update()

    # draw_grid function to draw the grid with height HEIGHT
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    # draw function fills the screen with black, draws grid, draws sprites
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):
        self.playing
        for event in pg.event.get():
            # when you hit the red x the window closes the game ends
            if event.type == pg.QUIT:
                self.quit()
                print("the game has ended")
            # nested if statements for controlling movement
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx = -1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy = -1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx = 1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy = 1)

    def show_start_screen(self):
        pass
    
    def show_go_screen(self):
        pass
    



# Instantiate Game
g = Game()
# g.show_go_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()
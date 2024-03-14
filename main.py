# This file was created by Justin Nguyen
# period 4
# importing libraries
import pygame as pg
from settings import *
from sprites import *
from utils import *
import sys
from random import randint
from os import path

# New things to include
# Teleport
# Enemies following player
# Scrolling backgrounds
# Scoreboard

class Cooldown():
    # sets all properties to zero when instantiated...
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
        # ticking ensures the timer is counting...
    # must use ticking to count up or down
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
    # resets event time to zero - cooldown reset
    def countdown(self, x):
        x = x - self.delta
        if x != None:
            return x
    def event_reset(self):
        self.event_time = floor((pg.time.get_ticks())/1000)
    # sets current time
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)

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
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'baby_yoda.png')).convert_alpha()
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)        

    def new(self):
        # create timer
        self.cooldown = Timer(self)
        # makes sprites into a group
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'p':
                    self.player = Player(self, col, row)
                if tile == 'c':
                    Coin(self, col, row)
                if tile == "u":
                    PowerUp(self, col, row)
                if tile == 'm':
                    Mob(self, col, row)
                if tile == 'P':
                    Portal(self, col, row, 5, 20)


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
        # tick the test timer
        self.cooldown.ticking()
        self.all_sprites.update()

    # draw_grid function to draw the grid with height HEIGHT
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
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)

     # draw function fills the screen with black, draws grid, draws sprites   
    def draw(self):
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            # draw the timer
            self.draw_text(self.screen, str(self.cooldown.current_time), 24, BGCOLOR, WIDTH/2 - 32, 2)
            pg.display.flip()

    def events(self):
        self.playing
        for event in pg.event.get():
            # when you hit the red x the window closes the game ends
            if event.type == pg.QUIT:
                self.quit()
                print("the game has ended")

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
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
        self.boss_spawned = False
        # later on we'll story game info with this
        self.load_data()
        self.game_over = False
        self.bosses = pg.sprite.Group()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'baby_yoda.png')).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, 'wall.png')).convert_alpha()
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)    

    def new(self):
        # create timer
        self.cooldown = Timer(self)
        # make all sprites into a group
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        self.slow_downs = pg.sprite.Group()
        self.weapons = pg.sprite.Group()
        self.bosses = pg.sprite.Group()
        # go through each line of the text file searching for key letters and setting letter to object
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
                if tile == 's':
                    SlowDown(self, col, row)

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
        self.cooldown.ticking()
        self.all_sprites.update()
        # Check if all coins are collected and all mobs are killed
        if len(self.coins) == 0 and len(self.mobs) == 0 and not self.bosses and not self.boss_spawned:
            print("All coins collected and all mobs killed. Spawning the final boss.")
            self.spawn_final_boss()

    def spawn_final_boss(self):
        boss_x, boss_y = 10, 10  # Set coordinates where the boss should spawn
        FinalBoss(self, boss_x, boss_y)
        self.boss_spawned = True  # Set the flag to indicate the boss has been spawned
        print("Final boss spawned at (10, 10)")

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
            for boss in self.bosses:
                boss.draw_health_bar(self.screen)
            # draw the timer
            self.draw_text(self.screen, str(self.player.moneybag), 64, PURPLE, 1, 1)
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
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen - press any key to play", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        self.screen.fill(ORANGE)
        # text for win
        self.draw_text(self.screen, "YOU WIN", 100, WHITE, WIDTH/3000, HEIGHT/160)
        pg.display.flip()
        self.wait_for_key()

    def show_end_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "You died", 25, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
        
    def stop_game(self):
        self.playing = False



# Instantiate Game
g = Game()
g.show_start_screen()
g.new()
g.run()
#g.show_go_screen()
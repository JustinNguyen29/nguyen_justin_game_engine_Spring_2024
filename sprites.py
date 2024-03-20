# This file was created by: Justin Nguyen
# Appreciation to Chris Bradfield
import pygame as pg
from settings import *
import math
import random

# write a player class
class Player(pg.sprite.Sprite):
    # initializing player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 300
        self.moneybag = 0

    # get keys function which gets input from keyboard and corresponds to direction of player
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed

    # collide with walls group with nested if stateents if player collides with top/bottom left/right of wall
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False )
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    # collide with group function that checks if player collides with another class
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
                print("You collected a coin!")
                print("Coin count: " + str(self.moneybag)) # printing coin statements
            if str(hits[0].__class__.__name__) == "PowerUp":
                self.speed += 200 # increase player speed by 200
            if str(hits[0].__class__.__name__) == "SlowDown":
                self.speed -= 100 # decrease player speed by 100  
            if str(hits[0].__class__.__name__) == "Portal":
                # set max_x and max_y to maximimum dimension of the window
                max_x = WIDTH - TILESIZE * 10
                max_y = WIDTH - TILESIZE * 10
                # generate random x, y coordinates
                random_x = random.randint(0, max_x // TILESIZE) * TILESIZE
                random_y = random.randint(0, max_y // TILESIZE) * TILESIZE     
                # Teleport the player to the random position
                self.x = random_x
                self.y = random_y
                self.rect.x = self.x
                self.rect.y = self.y
            if str(hits[0].__class__.__name__) == "Mob":
                self.playing = False          

    # new motion
    # check if player collides with groups
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.portals, True)
        self.collide_with_group(self.game.slow_downs, True)      




# Wall class
class Wall(pg.sprite.Sprite):
    # Initializing the class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def update(self):
        # self.rect.x += 1
        # self.rect.y += 1
        pass

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # decreased width and height of the coin so it fits within the cell
        self.image = pg.Surface((TILESIZE - 2, TILESIZE - 2))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # added 1.4 to the position to center the coin
        self.rect.x = x * TILESIZE + 1.4
        self.rect.y = y * TILESIZE + 1.4

# Initializes PowerUp class
class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# initializes slowDown class
class SlowDown(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.slow_downs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# initializes mob class
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 100  # Set a consistent speed for the Mob

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:  # Moving right- hit the left side of the wall
                    self.x = hits[0].rect.left - self.rect.width
                elif self.vx < 0:  # Moving left- hit the right side of the wall
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:  # Moving down- hit the top side of the wall
                    self.y = hits[0].rect.top - self.rect.height
                elif self.vy < 0:  # Moving up- hit the bottom side of the wall
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        # utilized AI to help find the distance to player and normalizing the vector. I decided to use this method
        # as it provided a more streamlined approach to the mob following the player
        # Calculate the difference in x and y between mob and player
        dx = self.game.player.rect.x - self.rect.x
        dy = self.game.player.rect.y - self.rect.y

        # Calculate the distance to the player using Distance Formula
        distance = math.sqrt(dx**2 + dy**2)

        # Normalize the vector and multiply by mob speed to get velocity
        if distance != 0:
            self.vx = (dx / distance) * self.speed
            self.vy = (dy / distance) * self.speed
        else:
            self.vx = 0
            self.vy = 0

        # Update rect for collision detection
        self.x += self.vx * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')

        # Move vertically and handle vertical collisions
        self.y += self.vy * self.game.dt
        self.rect.y = self.y
        self.collide_with_walls('y')

# Initializing portal Class
class Portal(pg.sprite.Sprite):
    def __init__(self, game, x, y, destination_x, destination_y):
        self.groups = game.all_sprites, game.portals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        # Destination coordinates for the corresponding Portal2
        self.destination_x = TILESIZE
        self.destination_y = TILESIZE


# This file was created by: Justin Nguyen
# Appreciation to Chris Bradfield
import pygame as pg
from settings import *

# write a player class
class Player(pg.sprite.Sprite):
    # initializing player
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED

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

    def collide_with_coins(self, dir):
        score = 0
        font = pg.font.Font(None, 36)
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.coins, False)
            for hit in hits:
                hit.image.fill(BGCOLOR)
                score += 1
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.coins, False)
            for hit in hits:
                hit.image.fill(BGCOLOR)
                score += 1


    # new motion
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.collide_with_coins('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_coins('y')

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
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # added 1.4 to the position to center the coin
        self.rect.x = x * TILESIZE + 1.4
        self.rect.y = y * TILESIZE + 1.4

# This file was created by: Justin Nguyen
# Appreciation to Chris Bradfield
import pygame as pg
from settings import *
import math
import random
import sys
from pygame.math import Vector2

vec = pg.math.Vector2

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
        self.speed = PLAYER_SPEED
        self.last_dir = (0, -1)  # Initialize last_dir with an upward direction
        self.moneybag = 0
        self.weapon_drawn = False
        self.weapon_dir = (0, 0)

    # get keys function which gets input from keyboard and corresponds to direction of player
    def get_keys(self):
        keys = pg.key.get_pressed()
        moving = False
        if keys[pg.K_e]:
            impulse = Impulse(self.game, self)
            impulse.trigger()
        if keys[pg.K_LEFT]:
            self.vx = -self.speed
            self.last_dir = (-1, 0)
            moving = True
        elif keys[pg.K_RIGHT]:
            self.vx = self.speed
            self.last_dir = (1, 0)
            moving = True
        elif keys[pg.K_UP]:
            self.vy = -self.speed
            self.last_dir = (0, -1)
            moving = True
        elif keys[pg.K_DOWN]:
            self.vy = self.speed
            self.last_dir = (0, 1)
            moving = True
        else:
            self.vx, self.vy = 0, 0  # Stop moving when no arrow keys are pressed

        if keys[pg.K_SPACE] and moving:  # Ensure player is moving to attack
            if not hasattr(self, 'weapon'):
                self.weapon = Weapon(self.game, self.rect.centerx, self.rect.centery, 10, 5, self.last_dir)



        # Weapon spawning logic
        if keys[pg.K_SPACE]:
            if not hasattr(self, 'weapon'):  # Check if the player already has a weapon
                # Assuming weapon should spawn at player's location and move in the last movement direction
                # You may want to adjust where the weapon spawns relative to the player's position
                self.weapon = Weapon(self.game, self.rect.centerx, self.rect.top, 10, 5, self.last_dir)
                print("Weapon spawned")  # Debug message to confirm spawning



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
                # if self.moneybag >= 5:
                    # self.game.stop_game()
                    # self.game.show_go_screen()                   
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
                self.kill()              
                self.game.stop_game()
                while True:
                    self.game.show_end_screen()

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
        self.collide_with_group(self.game.mobs, False)
        self.collide_with_group(self.game.bosses, True)



# Wall class
class Wall(pg.sprite.Sprite):
    # Initializing the class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

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
        self.impulse_velocity = Vector2(0, 0)  # Additional attribute to handle impulse force


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
        dx = self.game.player.rect.x - self.rect.x
        dy = self.game.player.rect.y - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:
            normalized_dx = dx / distance
            normalized_dy = dy / distance
            self.vx = normalized_dx * self.speed
            self.vy = normalized_dy * self.speed
        else:
            self.vx = 0
            self.vy = 0

        self.rect.x += self.vx * self.game.dt
        self.rect.y += self.vy * self.game.dt

        # Apply impulse force
        self.rect.x += int(self.impulse_velocity.x)
        self.rect.y += int(self.impulse_velocity.y)

        # Reset impulse_velocity after applying it
        self.impulse_velocity = Vector2(0, 0)

        # Handle collisions with walls
        self.collide_with_walls('x')
        self.collide_with_walls('y')

    def create_particles(self):
        for _ in range(20):  # Create 20 particles
            particle = Particle(self.rect.centerx, self.rect.centery)
            self.game.all_sprites.add(particle)



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

# modified from ChatGPT
class Weapon(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, dir):
        self.groups = game.all_sprites, game.weapons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.dir = dir
        self.base_width = w
        self.base_height = h
        self.hitbox_extension = 5  # Reduce the hitbox size
        self.image = pg.Surface((self.base_width + self.hitbox_extension, self.base_height + self.hitbox_extension))
        self.image.fill(WHITE)  # Color of the sword
        self.rect = self.image.get_rect()
        self.update_position(x, y, dir)

    def update_position(self, x, y, dir):
        offset = 20  # Distance from player center
        if dir == (0, -1):  # Up
            self.rect.centerx = x
            self.rect.top = y - offset
        elif dir == (0, 1):  # Down
            self.rect.centerx = x
            self.rect.bottom = y + offset
        elif dir == (-1, 0):  # Left
            self.rect.right = x - offset
            self.rect.centery = y
        elif dir == (1, 0):  # Right
            self.rect.left = x + offset
            self.rect.centery = y

    def update(self):
        # Continuously update position with the player
        self.update_position(self.game.player.rect.centerx, self.game.player.rect.centery, self.game.player.last_dir)

        # Collision detection with mobs
        hits = pg.sprite.spritecollide(self, self.game.mobs, False, pg.sprite.collide_mask)
        for hit in hits:
            print("Hit a mob!")  # Debugging print statement
            hit.create_particles()
            hit.kill()  # Remove the mob from the game
        
        # Collision detection with final boss
        boss_hits = pg.sprite.spritecollide(self, self.game.bosses, False, pg.sprite.collide_mask)
        for boss in boss_hits:
            boss.get_hit()
            print("Hit the boss!")  # Debugging print statement


class Impulse:
    # utilized OpenAI to help with implementation
    def __init__(self, game, player, radius=100, force=500):
        self.game = game
        self.player = player
        self.radius = radius
        self.force = force

    def trigger(self):
        player_pos = Vector2(self.player.rect.center)
        for mob in self.game.mobs:
            mob_pos = Vector2(mob.rect.center)
            distance = player_pos.distance_to(mob_pos)
            if distance < self.radius and distance > 0:  # Avoid division by zero
                direction = mob_pos - player_pos
                direction.normalize_ip()
                # Apply force inversely proportional to distance
                mob.impulse_velocity += direction * (self.force / max(1, distance))
                print(f"Mob repelled to {mob.rect.center} with impulse velocity {mob.impulse_velocity}")


# modified from ChatGPT
class Particle(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((5, 5))  # Size of the particle
        self.image.fill(RED)  # Red particles
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pg.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * random.randint(2, 5)
        self.lifetime = random.randint(20, 50)  # Frames before dying

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()


class FinalBoss(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.bosses
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE * 2, TILESIZE * 2))  # Boss is larger than other sprites
        self.image.fill(RED)  # Change color as desired
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.health = 2  # Boss needs to be hit once
        self.max_health = 2  # Max health for the health bar
        self.speed = 200  # Set a consistent speed for the Mob
        self.impulse_velocity = Vector2(0, 0)


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
        dx = self.game.player.rect.x - self.rect.x
        dy = self.game.player.rect.y - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:
            normalized_dx = dx / distance
            normalized_dy = dy / distance
            self.vx = normalized_dx * self.speed
            self.vy = normalized_dy * self.speed
        else:
            self.vx = 0
            self.vy = 0

        self.rect.x += self.vx * self.game.dt
        self.rect.y += self.vy * self.game.dt

        # Apply impulse force
        self.rect.x += int(self.impulse_velocity.x)
        self.rect.y += int(self.impulse_velocity.y)

        # Reset impulse_velocity after applying it
        self.impulse_velocity = Vector2(0, 0)

        # Handle collisions with walls
        self.collide_with_walls('x')
        self.collide_with_walls('y')

    def create_particles(self):
        for _ in range(20):  # Create 20 particles
            particle = Particle(self.rect.centerx, self.rect.centery)
            self.game.all_sprites.add(particle)


    def draw_health_bar(self, surface):
        # Calculate the width of the health bar
        health_bar_width = self.rect.width * (self.health / self.max_health)
        health_bar = pg.Rect(self.rect.x, self.rect.y - 10, health_bar_width, 5)
        outline_rect = pg.Rect(self.rect.x, self.rect.y - 10, self.rect.width, 5)
        pg.draw.rect(surface, RED, health_bar)
        pg.draw.rect(surface, WHITE, outline_rect, 2)  # Draw border around health bar

    def get_hit(self):
        self.health -= 1
        print(f"Boss health: {self.health}")  # Debugging print statement to check health
        if self.health <= 0:
            self.kill()



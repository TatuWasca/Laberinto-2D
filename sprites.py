import pygame as pg
import random
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2

########################################(Collision)########################################
def collide_with_walls(sprite, group, dir):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        if dir == 'x':
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
        if dir == 'y':
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
         

########################################(Spritesheet class)########################################
class Spritesheet:
    # Utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    ############### get image ###############
    def get_image(self, x, y, width, height):
        # Grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image

########################################(Player class)########################################
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.current_frame = -1
        self.last_updated = 0
        self.state = "idle"
        self.isdead = False
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.friction =  -.12
        self.acceleration = vec(0, 0)
        self.rect.center = self.pos
        self.hit_rect.center = self.rect.center

    ############### get keys ###############
    def get_keys(self):
        self.acceleration = vec(0,0)
        if self.state not in ['dead', 'win', 'spawn', 'none']:
            # Checks for pressed keys and updates state and velocity
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.acceleration.x -= PLAYER_SPEED
                self.state = "moving left"
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.acceleration.x += PLAYER_SPEED
                self.state = "moving right"
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.acceleration.y -= PLAYER_SPEED
                self.state = "moving up"
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.acceleration.y += PLAYER_SPEED
                self.state = "moving down"
            if (keys[pg.K_DOWN] or keys[pg.K_s]) and (keys[pg.K_RIGHT] or keys[pg.K_d]):
                self.acceleration *= 0.7071
                self.state = "moving right and down"
            if (keys[pg.K_DOWN] or keys[pg.K_s]) and (keys[pg.K_LEFT] or keys[pg.K_a]):
                self.acceleration *= 0.7071
                self.state = "moving left and down"
            if (keys[pg.K_UP] or keys[pg.K_w]) and (keys[pg.K_RIGHT] or keys[pg.K_d]):
                self.acceleration *= 0.7071
                self.state = "moving right and up"
            if (keys[pg.K_UP] or keys[pg.K_w]) and (keys[pg.K_LEFT] or keys[pg.K_a]):
                self.acceleration *= 0.7071
                self.state = "moving left and up"

    ############### load images ###############
    def load_images(self):
        # Load all player frames
        self.idle_frames = [self.game.spritesheet.get_image(0, 0, 32, 32),
                            self.game.spritesheet.get_image(32, 0, 32, 32),
                            self.game.spritesheet.get_image(64, 0, 32, 32),
                            self.game.spritesheet.get_image(96, 0, 32, 32),
                            self.game.spritesheet.get_image(128, 0, 32, 32),
                            self.game.spritesheet.get_image(160, 0, 32, 32)]
        self.walking_t = [self.game.spritesheet.get_image(192, 0, 32, 32)]
        self.walking_d = [self.game.spritesheet.get_image(224, 0, 32, 32)]
        self.walking_l = [self.game.spritesheet.get_image(256, 0, 32, 32)]
        self.walking_r = [self.game.spritesheet.get_image(288, 0, 32, 32)]
        self.walking_t_r = [self.game.spritesheet.get_image(320, 0, 32, 32)]
        self.walking_d_l = [self.game.spritesheet.get_image(352, 0, 32, 32)]
        self.walking_t_l = [self.game.spritesheet.get_image(384, 0, 32, 32)]
        self.walking_d_r = [self.game.spritesheet.get_image(416, 0, 32, 32)]
        self.dead_frames = [self.game.spritesheet.get_image(448, 0, 32, 32),
                            self.game.spritesheet.get_image(480, 0, 32, 32),
                            self.game.spritesheet.get_image(512, 0, 32, 32),
                            self.game.spritesheet.get_image(544, 0, 32, 32),
                            self.game.spritesheet.get_image(576, 0, 32, 32),
                            self.game.spritesheet.get_image(608, 0, 32, 32),
                            self.game.spritesheet.get_image(640, 0, 32, 32),
                            self.game.spritesheet.get_image(672, 0, 32, 32),
                            self.game.spritesheet.get_image(704, 0, 32, 32),
                            self.game.spritesheet.get_image(736, 0, 32, 32),
                            self.game.spritesheet.get_image(736, 0, 32, 32)]
        self.spawn_frames = [self.game.spritesheet.get_image(0, 32, 32, 32),
                            self.game.spritesheet.get_image(32, 32, 32, 32),
                            self.game.spritesheet.get_image(64, 32, 32, 32),
                            self.game.spritesheet.get_image(96, 32, 32, 32),
                            self.game.spritesheet.get_image(128, 32, 32, 32),
                            self.game.spritesheet.get_image(160, 32, 32, 32),
                            self.game.spritesheet.get_image(192, 32, 32, 32),
                            self.game.spritesheet.get_image(224, 32, 32, 32),
                            self.game.spritesheet.get_image(256, 32, 32, 32),
                            self.game.spritesheet.get_image(288, 32, 32, 32),
                            self.game.spritesheet.get_image(320, 32, 32, 32)]
        self.win_frames = [self.game.spritesheet.get_image(320, 32, 32, 32),
                            self.game.spritesheet.get_image(352, 32, 32, 32),
                            self.game.spritesheet.get_image(384, 32, 32, 32),
                            self.game.spritesheet.get_image(416, 32, 32, 32),
                            self.game.spritesheet.get_image(448, 32, 32, 32),
                            self.game.spritesheet.get_image(480, 32, 32, 32),
                            self.game.spritesheet.get_image(512, 32, 32, 32),
                            self.game.spritesheet.get_image(544, 32, 32, 32),
                            self.game.spritesheet.get_image(576, 32, 32, 32),
                            self.game.spritesheet.get_image(608, 32, 32, 32),
                            self.game.spritesheet.get_image(640, 32, 32, 32),
                            self.game.spritesheet.get_image(672, 32, 32, 32),
                            self.game.spritesheet.get_image(704, 32, 32, 32),
                            self.game.spritesheet.get_image(736, 32, 32, 32),
                            self.game.spritesheet.get_image(0, 64, 32, 32),
                            self.game.spritesheet.get_image(32, 64, 32, 32),
                            self.game.spritesheet.get_image(64, 64, 32, 32),
                            self.game.spritesheet.get_image(96, 64, 32, 32),
                            self.game.spritesheet.get_image(128, 64, 32, 32),
                            self.game.spritesheet.get_image(160, 64, 32, 32),
                            self.game.spritesheet.get_image(192, 64, 32, 32),
                            self.game.spritesheet.get_image(192, 64, 32, 32)]
        
    ############### animate ###############
    def animate(self):
        now = pg.time.get_ticks()
        # Idle animation
        if self.state == 'idle':
            if now - self.last_updated > 200:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                self.image = self.idle_frames[self.current_frame]
        # Diagonal animation
        elif self.state in ['moving right and up', 'moving left and up', 'moving right and down','moving left and down']:
            self.current_frame = 0
            if now - self.last_updated > 100:
                self.last_updated = now
                if self.state == 'moving right and up':
                    self.image = self.walking_t_r[0]
                elif self.state == 'moving left and up':
                    self.image = self.walking_t_l[0]
                elif self.state == 'moving right and down':
                    self.image = self.walking_d_r[0]
                elif self.state == 'moving left and down':
                    self.image = self.walking_d_l[0]
            self.state = 'idle'
        # Vertical and horizontal animation
        elif self.state in ['moving right', 'moving left', 'moving down','moving up']:
            self.current_frame = 0
            if now - self.last_updated > 100:
                self.last_updated = now
                if self.state == 'moving left' or self.state == 'moving right':
                    if self.state == 'moving left':
                        self.image = self.walking_l[0]
                    elif self.state == 'moving right':
                        self.image = self.walking_r[0]
                elif self.state == 'moving up' or self.state == 'moving down':
                    if self.state == 'moving up':
                        self.image = self.walking_t[0]
                    elif self.state == 'moving down':
                        self.image = self.walking_d[0]
            self.state = 'idle'
        # Death animation
        elif self.state == 'dead':
            now = pg.time.get_ticks()
            if now - self.last_updated > 50:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.dead_frames)
                self.image = self.dead_frames[self.current_frame]
                if self.current_frame - 1 == 9:
                    # Locks on last frame
                    self.image = self.dead_frames[10]
                    self.state = 'none'

                    # Calls game over screen
                    self.game.curr_menu = self.game.gameover_menu
                    self.game.playing = False
        # Spawn animation
        elif self.state == 'spawn':
            now = pg.time.get_ticks()
            if now - self.last_updated > 75:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.spawn_frames)
                self.image = self.spawn_frames[self.current_frame]
                if self.current_frame == 10:
                    # Changes to normal animation
                    self.state = 'idle'
                    self.current_frame = -1
        # Win animation
        elif self.state == 'win':
            now = pg.time.get_ticks()
            if now - self.last_updated > 75:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.win_frames)
                self.image = self.win_frames[self.current_frame]
                if self.current_frame - 1 == 20:
                    # Locks on last frame
                    self.image = self.win_frames[21]
                    self.state = 'none'

                    # Calls game over screen
                    self.game.curr_menu = self.game.win_menu
                    self.game.playing = False
    
    ############### update ###############
    def update(self):
        self.get_keys()

        # Updates the position depending on the image and velocity
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.acceleration += self.vel * self.friction
        self.vel += self.acceleration * self.game.dt * 60
        self.pos += self.vel * self.game.dt + (self.acceleration * .5) * (self.game.dt  * self.game.dt)

        # Check collision and updates pos
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')

        self.rect.center = self.hit_rect.center
        self.animate()

########################################(Mob class)########################################
class Mob(pg.sprite.Sprite):
    def __init__( self, game, grid_x, grid_y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.rect.topleft = (grid_x * TILESIZE, grid_y * TILESIZE)
        self.direction = random.choice( [ 'N', 'S', 'E', 'W' ] ) 
        self.next_mob_movement = pg.time.get_ticks() + 3500
        self.hit_rect.topleft = self.rect.topleft
        self.last_updated = 0

    ############### move to grid ###############
    def moveToGrid(self, grid_x, grid_y):
        # Allow position to be reset 
        self.rect.topleft = (grid_x * TILESIZE, grid_y * TILESIZE)

    ############### available moves ###############
    def availableMoves(self):
        #Consult the map to see where is good to go from here. We only consider walls, not other NPCs 
        map_x, map_y = (self.rect.x // TILESIZE, self.rect.y // TILESIZE)
        exits = []
        if ( self.game.navmap[ map_y-1 ][ map_x ] != '#' ):
            exits.append( 'N' )
        if ( self.game.navmap[ map_y ][ map_x+1 ] != '#' ):
            exits.append( 'E' )
        if ( self.game.navmap[ map_y+1 ][ map_x ] != '#' ):
            exits.append( 'S' )
        if ( self.game.navmap[ map_y ][ map_x-1 ] != '#' ):
            exits.append( 'W' )
        return exits

    ############### get opposite direction ###############
    def getOppositeDirection(self):
        opposites = { 'N':'S', 'S':'N', 'E':'W', 'W':'E' }
        return opposites[ self.direction ]

    ############### move forward ###############
    def moveForward(self):
        now = pg.time.get_ticks()
        if now - self.last_updated > 10:
            self.last_updated = now
            # Whichever direction we're moving in, go forward
            if ( self.direction == 'N' ):
                self.rect.y -= MOB_SPEED 
            elif ( self.direction == 'E' ):
                self.rect.x += MOB_SPEED 
            elif ( self.direction == 'S' ):
                self.rect.y += MOB_SPEED 
            else:  # W
                self.rect.x -= MOB_SPEED 

    ############### update ###############
    def update(self):
        now = pg.time.get_ticks()
        if (now > self.next_mob_movement):
            self.next_mob_movement = now + 5
            exits = self.availableMoves()
            
            # Generally: Keep moving in current direction, never u-turn 
            opposite = self.getOppositeDirection()
            
            # Checks if mob position is in a tile by dividing its position for the tile size and getting a remainder of 0
            if self.rect.x % 32 == 0 and self.rect.y % 32 == 0:
                # 50% change of continuing forward at an intersection
                if ( self.direction in exits and ( len( exits ) == 1 or random.randrange( 0,100 ) <= 50 ) ):
                    pass
                elif ( self.direction not in exits and len( exits ) == 1 ):
                    self.direction = exits[0]   # maybe u-turn
                else:  # more than 1 exit
                    if ( opposite in exits ):
                        exits.remove( opposite )
                    self.direction = random.choice( exits )
            # Move-it- Move-it
            self.moveForward()

            self.hit_rect.topleft = self.rect.topleft
        
########################################(Exit class)########################################
class Exit(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.exits
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.rect.x = x
        self.rect.y = y

########################################(Obstacle class)########################################
class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
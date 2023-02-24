import pygame as pg
import pytmx
from settings import *

vec = pg.math.Vector2

########################################(Check collision)########################################(
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

########################################(TiledMap class)########################################
class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    ############### render ###############
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))  

    ############### make map ###############
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

########################################(Camera class)########################################
class Camera:
    def __init__(self, game, width, height):
        self.game = game
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    ############### apply ###############
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    ############### apply rect ###############
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    ############### update ###############
    def update(self, target):
        x = -target.rect.centerx + int(self.game.width / 2)
        y = -target.rect.centery + int(self.game.height / 2)

        # Limit scrolling to map size
        x = min(0, x)  # Left
        y = min(0, y)  # Top
        x = max(-(self.width - self.game.width), x)  # Right
        y = max(-(self.height - self.game.height), y)  # Bottom
        self.camera = pg.Rect(x, y, self.width, self.height)

########################################(Timer class)########################################
class Timer:
    def __init__(self, game, wait_time):
        self.game = game
        self.wait_time = wait_time
        self.last_updated = 0
        self.time = int((DEFAULT_TIME / (int(self.game.difficulty) + 1)) * 60)

        mins, secs = divmod(self.time, 60)
        self.time_left = '{:02d}:{:02d}'.format(mins, secs)

    ############### check time ###############
    def check_time(self):
        now = pg.time.get_ticks()

        # Checks time every second
        if now - self.last_updated > 1000 + self.wait_time:
            self.wait_time = 0
            if self.time > 1:
                self.last_updated = now
                self.time -= 1
                
                # Formats to minutes and seconds
                mins, secs = divmod(self.time, 60)
                self.time_left = '{:02d}:{:02d}'.format(mins, secs)
            elif self.time == 1 and self.game.player.state != 'win':
                self.last_updated = now
                self.time -= 1

                # Formats to minutes and seconds
                mins, secs = divmod(self.time, 60)
                self.time_left = '{:02d}:{:02d}'.format(mins, secs)

                # Plays death sound and animation
                pg.mixer.music.fadeout(1000)
                self.game.effects_sounds['death'].play()

                self.game.player.current_frame = -1
                self.game.player.state = 'dead' 
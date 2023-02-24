import pygame as pg
import sys
import random
import configparser
import os
from os import path
from settings import *
from sprites import *
from tilemap import *
from menu import *

########################################(HUD and others)########################################
def generate_exit(p_spawn, e_spawns, m_height, m_width):
    # Filters out all the possible spawn near the player spawn and chooses one from that list
    spawn = []
    if p_spawn[0] < m_width / 2:
        if p_spawn[1] < m_height / 2:
            spawn = filter(lambda y: (not(y[0] < m_width/2 and y[1] < m_height/2)), e_spawns) # Top Left Corner
        elif p_spawn[1] > m_height / 2:
            spawn = filter(lambda y: (not(y[0] < m_width/2 and y[1] > m_height/2)), e_spawns) # Bottom left Corner
    elif p_spawn[0] > m_width / 2:
        if p_spawn[1] < m_height / 2 :
            spawn = filter(lambda y: (not(y[0] > m_width/2 and y[1] < m_height/2)), e_spawns) # Top right Corner
        elif p_spawn[1] > m_height / 2:
            spawn = filter(lambda y: (not(y[0] > m_width/2 and y[1] > m_height/2)), e_spawns) # Bottom right Corner
    spawn = random.choice(list(spawn))
    return spawn
 
########################################(Game class)########################################
class Game:
    def __init__(self):
        pg.init()
        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.VIDEORESIZE])
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        # Get all files
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')
        self.map_folder = path.join(self.game_folder, 'maps')
        self.music_folder = path.join(self.game_folder, 'music')

        # Starts the config parser
        self.configParser = configparser.ConfigParser()
        self.configFilePath = os.path.join(self.game_folder, 'config.cfg')
        self.configParser.read(self.configFilePath)
        
        # Loads width and height for starting the screen as well if its fullscreen or not
        self.isFullscreen = str(self.configParser.get("info","FULLSCREEN"))
        self.width = int(self.configParser.get("info","WIDTH"))
        self.height = int(self.configParser.get("info","HEIGHT"))
        self.fps = int(self.configParser.get("info","FPS"))
        self.difficulty = int(self.configParser.get("info","DIFFICULTY"))
        self.general_vol = int(self.configParser.get("info","GENERAL_VOLUME"))
        self.music_vol = int(self.configParser.get("info","MUSIC_VOLUME"))

        # Loads default map
        self.curr_map = 'debugmap.tmx'

        # Creates screen checking fullscreen
        if self.isFullscreen == 'True':
            self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        else:
            self.screen = pg.display.set_mode((self.width, self.height), pg.RESIZABLE)

        pg.display.set_caption('Laberinto 2D')
        pg.mouse.set_visible(False)
        self.clock = pg.time.Clock()
        self.load_data()
    
    ############### load data ###############
    def load_data(self):
        # Fonts
        self.font = path.join(self.img_folder, FONT)
        self.Titlefont = pg.font.Font(self.font, 20)
        self.Textfont = pg.font.Font(self.font, 15)
        self.Smalltextfont = pg.font.Font(self.font, 10)

        # Sprites
        self.spritesheet = Spritesheet(path.join(self.img_folder, PLAYER_IMG))
        self.mob_img = pg.image.load(path.join(self.img_folder, MOB_IMG))
        self.exit_img = pg.image.load(path.join(self.img_folder, EXIT_IMG))

        # Menu system
        self.main_menu = MainMenu(self)
        self.choosemap = ChooseMapMenu(self)
        self.difficulty_menu = DifficultyMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.paused_menu = PauseMenu(self)
        self.gameover_menu = GameoverMenu(self)
        self.win_menu = WinMenu(self)
        self.curr_menu = self.main_menu
        
        # Music
        pg.mixer.music.load(path.join(self.music_folder, MAIN_MENU_MUSIC))

        # Sound effects
        self.effects_sounds = {}
        for type in EFFECT_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(self.music_folder, EFFECT_SOUNDS[type]))
            self.effects_sounds[type].set_volume(self.general_vol / 100)
        pg.mixer.music.set_volume(self.music_vol / 100)
        pg.mixer.music.play(loops=-1)

        # Variables
        self.playing = False
        self.draw_debug = False

    ############### new ###############
    def new(self):
        # Map and navmesh
        self.map = TiledMap(path.join(self.map_folder, self.curr_map))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.navmap = self.generate_navmesh()

        # Initialize all sprites as a group
        self.all_sprites = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.exits = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        
        # Generates a player spawn, then does the same with the exit and collision map
        self.playerspawns = []
        self.p_spawn = []
        self.exitspawns = []
        self.e_spawn = []

        self.generate_colmap()

        self.spawn = random.choice(self.playerspawns)     
        self.e_spawn = generate_exit(self.spawn, self.exitspawns, self.map.height, self.map.width)

        # Creates player and the exit
        self.exit = Exit(self, self.e_spawn[0], self.e_spawn[1], 32, 32)
        self.player = Player(self, self.spawn[0] + 16, self.spawn[1] + 16)

        # Generate the camera and timer
        self.camera = Camera(self, self.map.width, self.map.height)
        self.timer = Timer(self, 1000)
        self.timer.last_updated = pg.time.get_ticks()
        if self.curr_menu == self.difficulty_menu:
            self.timer.wait_time = 3500

        # Generates fog
        self.light = pg.image.load(path.join(self.img_folder, LIGHT_IMG)).convert_alpha()
        if int(self.difficulty) == 0:
            self.light = pg.transform.smoothscale(self.light, (700, 700))
        elif int(self.difficulty) == 1:
            self.light = pg.transform.smoothscale(self.light, (550, 550))
        elif int(self.difficulty) == 2:
            self.light = pg.transform.smoothscale(self.light, (400, 400))
        elif int(self.difficulty) == 3:
            self.light = pg.transform.smoothscale(self.light, (250, 250))
        self.light_rect = self.light.get_rect()
        self.fog = self.screen.copy()

        # Display spawn animation
        self.player.state = 'none'
        self.player.image = self.player.spawn_frames[0]

        if self.curr_menu == self.difficulty_menu:
            # Animation for starting
            surf = self.screen.copy()
            num = 0
            last_updated = 0
            alpha = 250
            while num < 8:  
                # Updates every 350 ticks
                now = pg.time.get_ticks()
                if now - last_updated > 350:
                    last_updated = now

                    self.dt = self.clock.tick(self.fps) / 1000.0 # fix for Python 2.x
                    self.update()
                    self.draw()

                    surf.set_alpha(alpha)
                    surf.fill((255,255,255))
                    self.screen.blit(surf, (0,0))  
                    pg.display.update()

                    num += 1
                    alpha -= 50
        self.player.state = 'spawn' 

        # Plays game music
        pg.mixer.music.load(path.join(self.music_folder, GAME_MUSIC))
        pg.mixer.music.play(loops=-1)
        
    ############### game loop ###############
    def run(self):
        while self.playing:
            self.dt = self.clock.tick(self.fps) / 1000.0 # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    ############### quit ###############
    def quit(self):
        # Exits the game 
        pg.quit()
        sys.exit()

    ############### update ###############
    def update(self):
        # Check time left
        self.timer.check_time()

        # Checks if the player was hit by a mob or reached the exit
        self.check_hits()
        self.check_win()

        # Update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    ############### draw ###############
    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        self.screen.blit(self.exit_img, self.camera.apply(self.exit))

        # Draws all sprites
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))            
        
        # Draws fog
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.fill(BLACK)
        self.fog.blit(self.light, self.light_rect)
        self.screen.blit(self.fog, (0,0), special_flags=pg.BLEND_RGBA_MIN)

        # Draws HUD
        self.draw_text('FPS: ' +  "{:.0f}".format(self.clock.get_fps()), 10, 5, 10, 'left')
        self.draw_text('Time Left: ' + self.timer.time_left, 15, self.width/2, 10, 'center')    

        pg.display.flip()

    ############### events ###############
    def events(self):
        # Catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.VIDEORESIZE:
                self.configParser.set("info","WIDTH", str(event.w))
                self.configParser.set("info","HEIGHT", str(event.h))

                # Writing the new config into the file
                with open(self.configFilePath, 'w') as configfile:
                    self.configParser.write(configfile)
                    configfile.close()

                self.width = int(self.configParser.get("info","WIDTH"))
                self.height = int(self.configParser.get("info","HEIGHT"))

                # Resets the fog surface
                self.fog = self.screen.copy()

                # Resets all in-game menu
                self.paused_menu.__init__(self)
                self.gameover_menu.__init__(self)
                self.win_menu.__init__(self)
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.curr_menu = self.paused_menu
                    self.playing = False

    ############### generate colmap ###############
    def generate_colmap(self):
        # Creates collision map and save exits and player coordinates
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.playerspawns.append([tile_object.x,tile_object.y])
            if tile_object.name == 'exit':
                self.exitspawns.append([tile_object.x, tile_object.y])   
            if tile_object.name == 'mob':
                Mob(self, tile_object.x / 32, tile_object.y/ 32)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

    ############### generate navmesh ###############
    def generate_navmesh(self):
        map = []
        row = ''

        # Creates a 2d list with all meausures of the map, escaled to the tilesize
        for y in range(0, int(self.map.height / TILESIZE)):
            for x in range(0, int(self.map.width / TILESIZE)):
                row += '#'
                if x == int(self.map.width/TILESIZE) - 1:
                    map.append(row)
                    row = ''
                x += 1
            y += 1

        # Replaces the position of a nav object in the map 
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'nav':
                row = list(map[int(tile_object.y/TILESIZE)])
                row[int(tile_object.x/TILESIZE)] = '.'
                map[int(tile_object.y/TILESIZE)] = ''.join(row)      
        return map

    ############### check hits###############
    def check_hits(self):
        if self.player.state not in ['dead', 'win']:
            hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
            if hits:
                # Plays death sound and animation
                pg.mixer.music.fadeout(1000)
                self.effects_sounds['death'].play()

                self.player.current_frame = -1
                self.player.state = 'dead'

    ############### check win ###############
    def check_win(self):
        if self.player.pos.x - 16  == self.e_spawn[0] and self.player.pos.y - 16 == self.e_spawn[1] and self.player.state != 'win':
            # Plays win sound and animation
            pg.mixer.music.fadeout(1000)
            self.effects_sounds['win'].play()

            self.player.current_frame = -1
            self.player.state = 'win' 
            
            # Updates map status
            if self.curr_map != MAPS[0]:
                self.configParser.set(self.curr_map, "COMPLETED", 'True')
                self.configParser.set(self.curr_map, "DIF", str(self.difficulty))

                # Writing the new config into the file
                with open(self.configFilePath, 'w') as configfile:
                    self.configParser.write(configfile)
                    configfile.close()

    ############### draw text ###############
    def draw_text(self, text, size, x, y, align):
        # Checks size
        if size == 20:
            text_surface = self.Titlefont.render(text, True, WHITE)
        if size == 15:
            text_surface = self.Textfont.render(text, True, WHITE)
        if size == 10:
            text_surface = self.Smalltextfont.render(text, True, WHITE)

        # Changes the position of text
        text_rect = text_surface.get_rect()

        # Checks align
        if align == "center":
            text_rect.center = (x,y)
        if align == "left":
            text_rect.left, text_rect.centery = x, y 

        self.screen.blit(text_surface, text_rect)
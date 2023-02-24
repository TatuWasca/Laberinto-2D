import pygame as pg
from os import path
from settings import *

########################################(Menu superclass)########################################
class Menu:
    def __init__(self, game):
        self.game = game
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY, self.DEBUG_MAP_KEY = False, False, False, False, False, False, False
        self.mid_w, self.mid_h = self.game.width / 2, self.game.height / 2
        self.run_display = True
        self.cursor_rect = pg.Rect(0, 0, 20, 20)
        self.offset = -50

    ############### draw cursor ###############
    def draw_cursor(self):
        self.game.draw_text('*', 20, self.cursor_rect.x, self.cursor_rect.y + 5, 'center')

    ############### blit screen ###############
    def blit_screen(self):
        self.game.draw_text('FPS: ' +  "{:.0f}".format(self.game.clock.get_fps()), 10, 5, 10, 'left')  
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY, self.DEBUG_MAP_KEY = False, False, False, False, False, False, False

        # Fixes player and mob movement if the game is paused
        self.game.dt = self.game.clock.tick(self.game.fps) / 1000.0# fix for Python 2.x

        pg.display.update()
    
    ############### relaod all menus ###############
    def reload_all_menus(self):
        # Reloads the menu system and saves the current menu status
        current_menu_state = self.game.curr_menu.state
        
        self.game.main_menu.__init__(self.game)
        self.game.choosemap.__init__(self.game)
        self.game.difficulty_menu.__init__(self.game)
        self.game.options.__init__(self.game)
        self.game.credits.__init__(self.game)
        self.game.paused_menu.__init__(self.game)
        self.game.gameover_menu.__init__(self.game)
        self.game.win_menu.__init__(self.game)

        self.game.curr_menu.state = current_menu_state
        self.game.curr_menu.check_state()

    ############### events ###############
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.VIDEORESIZE:
                self.game.configParser.set("info","WIDTH", str(event.w))
                self.game.configParser.set("info","HEIGHT", str(event.h))

                # Writing the new config into the file
                with open(self.game.configFilePath, 'w') as configfile:
                    self.game.configParser.write(configfile)
                    configfile.close()

                self.game.width = int(self.game.configParser.get("info","WIDTH"))
                self.game.height = int(self.game.configParser.get("info","HEIGHT"))

                # Reload global menu variables
                self.mid_w, self.mid_h = self.game.width / 2, self.game.height / 2
                self.reload_all_menus()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.START_KEY = True
                if event.key == pg.K_BACKSPACE or event.key == pg.K_ESCAPE:
                    self.BACK_KEY = True
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.DOWN_KEY = True
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.UP_KEY = True
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.LEFT_KEY = True
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.RIGHT_KEY = True
                if event.key == pg.K_h and self.game.choosemap.ismap4com == 'True':
                    self.DEBUG_MAP_KEY = True

########################################(MainMenu class)########################################
class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.exitx, self.exity = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
    
    ############### display menu ###############
    def display_menu(self):
        self.run_display = True
        self.game.screen.fill(BLACK)
        while self.run_display:
            self.events()
            self.check_input()

            self.game.screen.fill(BLACK)
            self.game.draw_text('Laberinto 2D', 20, self.mid_w, self.mid_h - 20, 'center')
            self.game.draw_text('Start Game', 15, self.startx, self.starty, 'center')
            self.game.draw_text('Options', 15, self.optionsx, self.optionsy, 'center')
            self.game.draw_text('Credits', 15, self.creditsx, self.creditsy, 'center')
            self.game.draw_text('Exit', 15, self.exitx, self.exity, 'center')

            self.draw_cursor()
            self.blit_screen()

    ############### move cursor ###############
    def move_cursor(self):
        if self.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
    
    ############### check state ###############
    def check_state(self):
        # Debug for rezising window
        if self.state == 'Start':
            self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        elif self.state == 'Options':
            self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
        elif self.state == 'Credits':
            self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
        elif self.state == 'Exit':
            self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)

    ############### check input ###############
    def check_input(self):
        self.move_cursor()
        if self.START_KEY:
            if self.state == 'Start':
                self.game.curr_menu = self.game.choosemap
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Exit':
                self.game.quit()
            self.run_display = False

########################################(Choose Map class)########################################
class ChooseMapMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "map1"
        self.map1x, self.map1y = self.mid_w, self.mid_h + 30
        self.map2x, self.map2y = self.mid_w, self.mid_h + 50
        self.map3x, self.map3y = self.mid_w, self.mid_h + 70
        self.map4x, self.map4y = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.map1x + self.offset, self.map1y)

        # Gets map status
        self.ismap1com = str(self.game.configParser.get("map1.tmx","COMPLETED"))
        self.ismap2com = str(self.game.configParser.get("map2.tmx","COMPLETED"))
        self.ismap3com = str(self.game.configParser.get("map3.tmx","COMPLETED"))
        self.ismap4com = str(self.game.configParser.get("map4.tmx","COMPLETED"))

        self.map1dif = int(self.game.configParser.get("map1.tmx","DIF")) + 1
        self.map2dif = int(self.game.configParser.get("map2.tmx","DIF")) + 1
        self.map3dif = int(self.game.configParser.get("map3.tmx","DIF")) + 1
        self.map4dif = int(self.game.configParser.get("map4.tmx","DIF")) + 1
    
    ############### display menu ###############
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.events()
            self.check_input()

            self.game.screen.fill(BLACK)
            self.game.draw_text('Choose a map', 20, self.mid_w, self.mid_h - 30, 'center')

            self.game.draw_text('Level 1', 15, self.map1x, self.map1y, 'center')
            self.game.draw_text('Level 2', 15, self.map2x, self.map2y, 'center')
            self.game.draw_text('Level 3', 15, self.map3x, self.map3y, 'center')
            self.game.draw_text('Level 4', 15, self.map4x, self.map4y, 'center')

            # Hell
            if self.ismap1com == 'False':
                pg.draw.rect(self.game.screen, WHITE, pg.Rect(self.map2x - 40, self.map2y, 80, 2))
            else:
                self.game.draw_text(self.map1dif * 'X', 15, self.map1x + 50, self.map1y, 'left')

            if self.ismap2com == 'False':
                pg.draw.rect(self.game.screen, WHITE, pg.Rect(self.map3x - 40, self.map3y, 80, 2))
            else:
                self.game.draw_text(self.map2dif * 'X', 15, self.map2x + 50, self.map2y, 'left')

            if self.ismap3com == 'False':
                pg.draw.rect(self.game.screen, WHITE, pg.Rect(self.map4x - 40, self.map4y, 80, 2))
            else: 
                self.game.draw_text(self.map3dif * 'X', 15, self.map3x + 50, self.map3y, 'left')

            if self.ismap4com == 'True':
                self.game.draw_text(self.map4dif * 'X', 15, self.map4x + 50, self.map4y, 'left')

            self.draw_cursor()
            self.blit_screen()

    ############### move cursor ###############
    def move_cursor(self):
        if self.DOWN_KEY:
            if self.state == 'map1':
                self.cursor_rect.midtop = (self.map2x + self.offset, self.map2y)
                self.state = 'map2'
            elif self.state == 'map2':
                self.cursor_rect.midtop = (self.map3x + self.offset, self.map3y)
                self.state = 'map3'
            elif self.state == 'map3':
                self.cursor_rect.midtop = (self.map4x + self.offset, self.map4y)
                self.state = 'map4'
            elif self.state == 'map4':
                self.cursor_rect.midtop = (self.map1x + self.offset, self.map1y)
                self.state = 'map1'
        elif self.UP_KEY:
            if self.state == 'map1':
                self.cursor_rect.midtop = (self.map4x + self.offset, self.map4y)
                self.state = 'map4'
            elif self.state == 'map2':
                self.cursor_rect.midtop = (self.map1x + self.offset, self.map1y)
                self.state = 'map1'
            elif self.state == 'map3':
                self.cursor_rect.midtop = (self.map2x + self.offset, self.map2y)
                self.state = 'map2'
            elif self.state == 'map4':
                self.cursor_rect.midtop = (self.map3x + self.offset, self.map3y)
                self.state = 'map3'
    
    ############### check state ###############
    def check_state(self):
        # Debug for rezising window
        if self.state == 'map1':
            self.cursor_rect.midtop = (self.map1x + self.offset, self.map1y)
        elif self.state == 'map2':
            self.cursor_rect.midtop = (self.map2x + self.offset, self.map2y)
        elif self.state == 'map3':
            self.cursor_rect.midtop = (self.map3x + self.offset, self.map3y)
        elif self.state == 'map4':
            self.cursor_rect.midtop = (self.map4x + self.offset, self.map4y)

    ############### check input ###############
    def check_input(self):
        self.move_cursor()
        if self.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.START_KEY:
            # Checks if the map is completed
            if self.state == 'map1':
                self.game.curr_menu = self.game.difficulty_menu
                self.game.curr_map = MAPS[1]
                self.run_display = False
            elif self.state == 'map2' and self.ismap1com == 'True':
                self.game.curr_menu = self.game.difficulty_menu
                self.game.curr_map = MAPS[2]
                self.run_display = False
            if self.state == 'map3' and self.ismap2com == 'True':
                self.game.curr_menu = self.game.difficulty_menu
                self.game.curr_map = MAPS[3]
                self.run_display = False
            elif self.state == 'map4' and self.ismap3com == 'True':
                self.game.curr_menu = self.game.difficulty_menu
                self.game.curr_map = MAPS[4]
                self.run_display = False
        elif self.DEBUG_MAP_KEY:
            self.game.curr_menu = self.game.difficulty_menu
            self.game.curr_map = MAPS[0]
            self.run_display = False

########################################(DifficultyMenu)########################################
class DifficultyMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Easy'
        self.easyx, self.easyy = self.mid_w, self.mid_h + 30
        self.mediumx, self.mediumy = self.mid_w, self.mid_h + 50
        self.hardx, self.hardy = self.mid_w, self.mid_h + 70
        self.extremex, self.extremey = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)

    ############### display menu ###############
    def display_menu(self):
        self.run_display = True

        # Fixes cursor to default position
        self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)
        self.state = 'Easy'
        while self.run_display:
            self.events()
            self.check_input()

            if not self.START_KEY:
                self.game.screen.fill(BLACK)
                self.game.draw_text('Choose a difficulty', 20, self.mid_w, self.mid_h - 30, 'center')
                self.game.draw_text('Easy', 15, self.easyx, self.easyy, 'center')
                self.game.draw_text('Medium', 15, self.mediumx, self.mediumy, 'center')
                self.game.draw_text('Hard', 15, self.hardx, self.hardy, 'center')
                self.game.draw_text('Extreme', 15, self.extremex, self.extremey, 'center')

                self.draw_cursor()
                self.blit_screen()

    ############### move cursor ###############
    def move_cursor(self):
        if self.DOWN_KEY:
            if self.state == 'Easy':
                self.cursor_rect.midtop = (self.mediumx + self.offset, self.mediumy)
                self.state = 'Medium'
            elif self.state == 'Medium':
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
                self.state = 'Hard'
            elif self.state == 'Hard':
                self.cursor_rect.midtop = (self.extremex + self.offset, self.extremey)
                self.state = 'Extreme'
            elif self.state == 'Extreme':
                self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)
                self.state = 'Easy'
        elif self.UP_KEY:
            if self.state == 'Easy':
                self.cursor_rect.midtop = (self.extremex + self.offset, self.extremey)
                self.state = 'Extreme'
            elif self.state == 'Medium':
                self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)
                self.state = 'Easy'
            elif self.state == 'Hard':
                self.cursor_rect.midtop = (self.mediumx + self.offset, self.mediumy)
                self.state = 'Medium'
            elif self.state == 'Extreme':
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
                self.state = 'Hard'

    ############### check state ###############
    def check_state(self):
        # Debug for rezising window
        if self.state == 'Easy':
            self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)
        elif self.state == 'Medium':
            self.cursor_rect.midtop = (self.mediumx + self.offset, self.mediumy)
        elif self.state == 'Hard':
            self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
        elif self.state == 'Extreme':
            self.cursor_rect.midtop = (self.extremex + self.offset, self.extremey)

    ############### check input ###############
    def check_input(self):
        self.move_cursor()
        if self.BACK_KEY:
            self.game.curr_menu = self.game.choosemap
            self.run_display = False
        elif self.START_KEY:
            if self.state == 'Easy':
                self.game.configParser.set("info","DIFFICULTY", '0')
            elif self.state == 'Medium':
                self.game.configParser.set("info","DIFFICULTY", '1')
            elif self.state == 'Hard':
                self.game.configParser.set("info","DIFFICULTY", '2')
            elif self.state == 'Extreme':
                self.game.configParser.set("info","DIFFICULTY", '3')

            # Writing the new config into the file
            with open(self.game.configFilePath, 'w') as configfile:
                self.game.configParser.write(configfile)
                configfile.close()

            pg.mixer.music.stop()
            self.game.effects_sounds['level_start'].play()

            # Animation for starting
            surf = self.game.screen.copy()
            num = 0
            last_updated = 0
            alpha = 0
            while num < 8:  
                # Updates every 350 ticks
                now = pg.time.get_ticks()
                if now - last_updated > 350:
                    last_updated = now

                    surf.set_alpha(alpha)
                    surf.fill((255,255,255))
                    self.game.screen.blit(surf, (0,0))  
                    pg.display.update()

                    num += 1
                    alpha += 50

            self.run_display = False
            self.game.playing = True
            
            self.game.difficulty = self.game.configParser.get("info","DIFFICULTY")
            self.game.new()

########################################(OptionsMenu)########################################
class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Fps'

        # Position of all text
        self.generalx, self.generaly = self.mid_w - 150, self.mid_h - 80
        self.fulx, self.fuly = self.mid_w - 140, self.mid_h - 60
        self.fpsx, self.fpsy = self.mid_w - 140, self.mid_h - 40
        self.volx, self.voly = self.mid_w - 150, self.mid_h - 10
        self.genvolx, self.genvoly = self.mid_w - 140, self.mid_h + 10
        self.musvolx, self.musvoly = self.mid_w - 140, self.mid_h + 30
        self.appx, self.appy = self.mid_w - 150, self.mid_h + 70
        self.cursor_rect.midtop = (self.fpsx + self.offset, self.fpsy + 7.5)

        # Variables
        self.isFul = self.game.configParser.get("info","Fullscreen")
        self.new_fps = int(self.game.configParser.get("info","FPS"))
        self.new_general_vol = int(self.game.configParser.get("info","GENERAL_VOLUME"))
        self.new_music_vol = int(self.game.configParser.get("info","MUSIC_VOLUME"))

    ############### display menu ###############
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.events()

            self.game.screen.fill(BLACK)
            self.game.draw_text('Options', 20, self.mid_w, self.mid_h - 100, 'center')

            self.game.draw_text('General', 15, self.generalx, self.generaly, 'left')
            self.game.draw_text('Fullscreen', 15, self.fulx, self.fuly, 'left')
            self.game.draw_text(str(self.isFul), 15, self.fulx + 200, self.fuly, 'left')
            self.game.draw_text('Fps', 15, self.fpsx, self.fpsy, 'left')
            self.game.draw_text(str(self.new_fps), 15, self.fpsx + 200, self.fpsy, 'left')

            self.game.draw_text('Volume', 15, self.volx, self.voly, 'left')
            self.game.draw_text('General volume', 15, self.genvolx, self.genvoly, 'left')
            self.game.draw_text(str(self.new_general_vol), 15, self.genvolx + 200, self.genvoly, 'left')
            self.game.draw_text('Music volume', 15, self.musvolx, self.musvoly, 'left')
            self.game.draw_text(str(self.new_music_vol), 15, self.musvolx + 200, self.musvoly, 'left')

            self.game.draw_text('Apply changes', 15, self.appx, self.appy, 'left')

            self.check_input()
            self.draw_cursor()
            self.blit_screen()

    ############### move cursor ###############
    def move_cursor(self):
        if self.BACK_KEY:
            # Fixes cursor to default position
            self.cursor_rect.midtop = (self.fpsx + self.offset, self.fpsy + 7.5)
            self.state = 'Fps'
            
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.DOWN_KEY:
            if self.state == 'Ful':
                self.cursor_rect.midtop = (self.fpsx + self.offset, self.fpsy + 7.5)
                self.state = 'Fps'
            elif self.state == 'Fps':
                self.cursor_rect.midtop = (self.genvolx + self.offset, self.genvoly + 7.5)
                self.state = 'General volume'
            elif self.state == 'General volume':
                self.cursor_rect.midtop = (self.musvolx + self.offset, self.musvoly + 7.5)
                self.state = 'Music volume'
            elif self.state == 'Music volume':
                self.cursor_rect.midtop = (self.appx + self.offset, self.appy + 7.5)
                self.state = 'Apply'
            elif self.state == 'Apply':
                self.cursor_rect.midtop = (self.fulx + self.offset, self.fuly + 7.5)
                self.state = 'Ful'
        elif self.UP_KEY:
            if self.state == 'Ful':
                self.cursor_rect.midtop = (self.appx + self.offset, self.appy + 7.5)
                self.state = 'Apply'
            elif self.state == 'Fps':
                self.cursor_rect.midtop = (self.fulx + self.offset, self.fuly + 7.5)
                self.state = 'Ful'
            elif self.state == 'General volume':
                self.cursor_rect.midtop = (self.fpsx + self.offset, self.fpsy + 7.5)
                self.state = 'Fps'
            elif self.state == 'Music volume':
                self.cursor_rect.midtop = (self.genvolx + self.offset, self.genvoly + 7.5)
                self.state = 'General volume'
            elif self.state == 'Apply':
                self.cursor_rect.midtop = (self.musvolx + self.offset, self.musvoly + 7.5)
                self.state = 'Music volume'

    ############### check state ###############
    def check_state(self):
        # Debug for rezising window
        if self.state == 'Fps':
            self.cursor_rect.midtop = (self.fpsx + self.offset, self.fpsy + 7.5)
        elif self.state == 'General volume':
            self.cursor_rect.midtop = (self.genvolx + self.offset, self.genvoly + 7.5)
        elif self.state == 'Music volume':
            self.cursor_rect.midtop = (self.musvolx + self.offset, self.musvoly + 7.5)
        elif self.state == 'Apply':
            self.cursor_rect.midtop = (self.appx + self.offset, self.appy + 7.5)

    ############### check input ###############
    def check_input(self):
        self.move_cursor()
        if self.LEFT_KEY:
            if self.state == 'Ful':
                self.isFul = 'True'
            elif self.state == 'Fps':
                if self.new_fps > 60:
                    self.new_fps -= 10
            elif self.state == 'General volume':
                if self.new_general_vol > 0:
                    self.new_general_vol -= 5
            elif self.state == 'Music volume':
                if self.new_music_vol > 0:
                    self.new_music_vol -= 5
        if self.RIGHT_KEY:
            if self.state == 'Ful':
                self.isFul = 'False'
            elif self.state == 'Fps':
                if self.new_fps < 500:
                    self.new_fps += 10
            elif self.state == 'General volume':
                if self.new_general_vol < 100:
                    self.new_general_vol += 5
            elif self.state == 'Music volume':
                if self.new_music_vol < 100:
                    self.new_music_vol += 5
        if self.START_KEY:
            if self.state == 'Apply':
                if str(self.isFul) == 'True':
                    self.game.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
                    surface = pg.display.get_surface() 
                    W, H = surface.get_width(), surface.get_height()

                    
                    self.game.configParser.set("info","FULLSCREEN", str(self.isFul))
                    self.game.configParser.set("info","WIDTH", str(W))
                    self.game.configParser.set("info","HEIGHT", str(H))
                else:
                    self.game.screen = pg.display.set_mode((1024, 768), pg.RESIZABLE)

                    self.game.configParser.set("info","FULLSCREEN", str(self.isFul))
                    self.game.configParser.set("info","WIDTH", '1024')
                    self.game.configParser.set("info","HEIGHT", '768')

                # Setting the configuration
                self.game.configParser.set("info","FPS", str(self.new_fps))
                self.game.configParser.set("info","GENERAL_VOLUME", str(self.new_general_vol)) 
                self.game.configParser.set("info","MUSIC_VOLUME", str(self.new_music_vol))

                # Writing the new config into the file
                with open(self.game.configFilePath, 'w') as configfile:
                    self.game.configParser.write(configfile)
                    configfile.close()

                # Reloading every variable
                self.game.isFullscreen = str(self.game.configParser.get("info","FULLSCREEN"))
                self.game.width = int(self.game.configParser.get("info","WIDTH"))
                self.game.height = int(self.game.configParser.get("info","HEIGHT"))
                self.game.fps = int(self.game.configParser.get("info","FPS"))
                self.game.general_vol = int(self.game.configParser.get("info","GENERAL_VOLUME"))
                self.game.music_vol = int(self.game.configParser.get("info","MUSIC_VOLUME"))

                # Reloads music and sound effects volume
                for type in EFFECT_SOUNDS:
                    self.game.effects_sounds[type].set_volume(self.game.general_vol / 100)
                pg.mixer.music.set_volume(self.game.music_vol / 100)

                # Reloading classes
                self.game.screen.fill(BLACK)
                self.reload_all_menus()

########################################(Credits menu)########################################
class CreditsMenu(Menu):
    def __init__(self,game):
        Menu.__init__(self, game)
        self.state = 'Credits'

    ############### display menu ###############
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.events()
            if self.START_KEY or self.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.screen.fill(BLACK)

            self.game.draw_text('Credits', 20, self.mid_w, self.mid_h - 20, 'center')
            self.game.draw_text('Programming by TatuWasca', 15, self.mid_w, self.mid_h + 10, 'center')
            self.game.draw_text('Textures by DoomManiac', 15, self.mid_w, self.mid_h + 30, 'center')

            self.blit_screen()

    ############### check state ###############
    def check_state(self):
        # Debug for rezising window, exception in this case
        pass

########################################(PauseMenu)########################################
class PauseMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Resume"
        self.resumex, self.resumey = self.mid_w, self.mid_h + 30
        self.exitx, self.exity = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
    
    ############### display menu ###############
    def display_menu(self):
        self.run_display = True
        
        # Fixes cursor to default position
        self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
        self.state = 'Resume'
        while self.run_display:
            self.events()
            self.check_input()

            # Draws screen
            self.game.screen.fill(BLACK)
            pg.draw.rect(self.game.screen, WHITE, pg.Rect(self.game.width/4 - 8, self.game.height/4 - 8, self.game.width/2 + 16, self.game.height/2 + 16))
            pg.draw.rect(self.game.screen, BLACK, pg.Rect(self.game.width/4, self.game.height/4, self.game.width/2, self.game.height/2))

            self.game.draw_text('Paused', 20, self.mid_w, self.mid_h - 20, 'center')
            self.game.draw_text('Resume', 15, self.resumex, self.resumey, 'center')
            self.game.draw_text('Exit', 15, self.exitx, self.exity, 'center')

            self.draw_cursor()
            self.blit_screen()

    ############### move cursor ###############
    def move_cursor(self):
        if self.DOWN_KEY or self.UP_KEY:
            if self.state == 'Resume':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
                self.state = 'Resume'

    ############### check state ###############
    def check_state(self):
        # Debug for rezising window
        if self.state == 'Resume':
            self.cursor_rect.midtop = (self.resumex + self.offset, self.resumey)
        elif self.state == 'Exit':
            self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)

    ############### check input ###############
    def check_input(self):
        self.move_cursor()
        if self.START_KEY:
            if self.state == 'Resume':
                # Resets the fog surface
                self.game.fog = self.game.screen.copy()

                self.game.playing = True
            elif self.state == 'Exit':
                pg.mixer.music.load(path.join(self.game.music_folder, MAIN_MENU_MUSIC))
                pg.mixer.music.play(loops=-1)

                # Reloading classes
                self.game.load_data()
                self.game.screen.fill(BLACK)

                self.game.curr_menu = self.game.main_menu
            self.run_display = False

########################################(GameoverMenu)########################################
class GameoverMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Retry"
        self.retryx, self.retryy = self.mid_w, self.mid_h + 30
        self.exitx, self.exity = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.retryx + self.offset, self.retryy)
    
    ############### display menu ###############
    def display_menu(self):
        self.run_display = True
        
        # Fixes cursor to default position
        self.cursor_rect.midtop = (self.retryx + self.offset, self.retryy)
        self.state = 'Retry'
        while self.run_display:
            self.events()
            self.check_input()

            # Draws screen
            self.game.screen.fill(BLACK)
            pg.draw.rect(self.game.screen, WHITE, pg.Rect(self.game.width/4 - 8, self.game.height/4 - 8, self.game.width/2 + 16, self.game.height/2 + 16))
            pg.draw.rect(self.game.screen, BLACK, pg.Rect(self.game.width/4, self.game.height/4, self.game.width/2, self.game.height/2))

            self.game.draw_text('Game Over', 20, self.mid_w, self.mid_h - 20, 'center')
            self.game.draw_text('Retry', 15, self.retryx, self.retryy, 'center')
            self.game.draw_text('Exit', 15, self.exitx, self.exity, 'center')

            self.draw_cursor()
            self.blit_screen()

    ############### move cursor ###############
    def move_cursor(self):
        if self.DOWN_KEY or self.UP_KEY:
            if self.state == 'Retry':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.retryx + self.offset, self.retryy)
                self.state = 'Retry'

    ############### check state ###############
    def check_state(self):
        # Debug for rezising window
        if self.state == 'Retry':
            self.cursor_rect.midtop = (self.retryx + self.offset, self.retryy)
        elif self.state == 'Exit':
            self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)

    ############### check input ###############
    def check_input(self):
        self.move_cursor()
        if self.START_KEY:
            if self.state == 'Retry':
                self.game.new()
                self.game.playing = True
            elif self.state == 'Exit':
                pg.mixer.music.load(path.join(self.game.music_folder, MAIN_MENU_MUSIC))
                pg.mixer.music.play(loops=-1)

                # Reloading classes
                self.game.load_data()
                self.game.screen.fill(BLACK)

                self.game.curr_menu = self.game.main_menu
            self.run_display = False

########################################(WinMenu)########################################
class WinMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Retry"
        self.retryx, self.retryy = self.mid_w, self.mid_h + 30
        self.exitx, self.exity = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.retryx + self.offset, self.retryy)
    
    ############### display menu ###############
    def display_menu(self):
        self.run_display = True
        
        # Checks if the map is the last one
        if self.game.choosemap.state != 'map4':
            self.state = 'Next'

        while self.run_display:
            self.events()
            self.check_input()

            # Draws screen
            self.game.screen.fill(BLACK)
            pg.draw.rect(self.game.screen, WHITE, pg.Rect(self.game.width/4 - 8, self.game.height/4 - 8, self.game.width/2 + 16, self.game.height/2 + 16))
            pg.draw.rect(self.game.screen, BLACK, pg.Rect(self.game.width/4, self.game.height/4, self.game.width/2, self.game.height/2))

            if self.game.choosemap.state != 'map4': 
                self.game.draw_text('You Win!', 20, self.mid_w, self.mid_h - 20, 'center')
                self.game.draw_text('Next level', 15, self.retryx, self.retryy, 'center')
                self.game.draw_text('Retry', 15, self.retryx, self.retryy + 20, 'center')
                self.game.draw_text('Exit', 15, self.exitx, self.exity + 20, 'center')
            else:
                self.game.draw_text('Level Passed!', 20, self.mid_w, self.mid_h - 20, 'center')
                self.game.draw_text('Retry', 15, self.retryx, self.retryy, 'center')
                self.game.draw_text('Exit', 15, self.exitx, self.exity, 'center')

            self.draw_cursor()
            self.blit_screen()

    ############### move cursor ###############
    def move_cursor(self):
        if self.DOWN_KEY:
            if self.game.choosemap.state != 'map4':
                if self.state == 'Next':
                    self.cursor_rect.midtop = (self.retryx + self.offset, self.retryy + 20)
                    self.state = 'Retry'
                elif self.state == 'Retry':
                    self.cursor_rect.midtop = (self.exitx + self.offset, self.exity + 20)
                    self.state = 'Exit'
                elif self.state == 'Exit':
                    self.cursor_rect.midtop = (self.retryx + self.offset, self.retryy)
                    self.state = 'Next'
            else: 
                if self.state == 'Retry':
                    self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                    self.state = 'Exit'
                elif self.state == 'Exit':
                    self.cursor_rect.midtop = (self.retryx + self.offset, self.retryy)
                    self.state = 'Retry'
        elif self.UP_KEY:
            if self.game.choosemap.state != 'map4':
                if self.state == 'Next':
                    self.cursor_rect.midtop = (self.exitx + self.offset, self.exity + 20)
                    self.state = 'Exit'
                elif self.state == 'Retry':
                    self.cursor_rect.midtop = (self.retryx + self.offset, self.retryy)
                    self.state = 'Next'
                elif self.state == 'Exit':
                    self.cursor_rect.midtop = (self.retryx + self.offset, self.retryy + 20)
                    self.state = 'Retry'
            else: 
                if self.state == 'Retry':
                    self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                    self.state = 'Exit'
                elif self.state == 'Exit':
                    self.cursor_rect.midtop = (self.retryx + self.offset, self.retryy)
                    self.state = 'Retry'

    ############### check state ###############
    def check_state(self):
        # Debug for rezising window 
        if self.game.choosemap.state != 'map4':
            if self.state == 'Next':
                self.cursor_rect.midtop = (self.retryx + self.offset, self.retryy)
            elif self.state == 'Retry':
                self.cursor_rect.midtop = (self.retryx + self.offset, self.retryy + 20)
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity + 20)
        else: 
            if self.state == 'Retry':
                self.cursor_rect.midtop = (self.retryx + self.offset, self.retryy)
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)

    ############### check input ###############
    def check_input(self):
        self.move_cursor()
        if self.START_KEY:
            if self.state == 'Next':
                if self.game.curr_map == 'map1.tmx':
                    self.game.curr_map = MAPS[2]
                elif self.game.curr_map == 'map2.tmx':
                    self.game.curr_map = MAPS[3]
                elif self.game.curr_map == 'map3.tmx':
                    self.game.curr_map = MAPS[4]

                self.game.new()
                self.game.playing = True
            elif self.state == 'Retry':
                self.game.new()
                self.game.playing = True
            elif self.state == 'Exit':
                pg.mixer.music.load(path.join(self.game.music_folder, MAIN_MENU_MUSIC))
                pg.mixer.music.play(loops=-1)

                # Reloading classes
                self.game.load_data()
                self.game.screen.fill(BLACK)

                self.game.curr_menu = self.game.main_menu
            self.run_display = False
import pygame, sys, time, math
from flamingo import *
from DefaultSettings import *
from os import path
from random import choice
from buttons_levels import *
from os import path

# slownik obrazkow

__all_game_images = {}


class Game:
    def __init__(self, level=0):

        pygame.mixer.init()
        pygame.init()

        sound_path = path.join(sound_folder, "sandy seaside_0.ogg")
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play(-1)

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption(title)
        self.Clock = pygame.time.Clock()
        self.GameOver = False
        self.GamePaused = False
        self.action = None
        self.mute = False
        self.FPS = FPS
        self.font = pygame.font.match_font(font)
        self.FlammingsHome = 0
        self.FlammingsOut = 0
        self.flam_freq = 3000
        self.coconut_timer = 0
        self.flamingo_timer = 0
        self.load_data()

    def load_data(self):

        self.game_images = {}

        for name, image in GAME_IMAGES.items():
            self.game_images[name] = pygame.image.load(path.join(images_folder, image)).convert_alpha()

    def new(self, level):

        level.initialize()
        self.level_number = level.level
        self.flamingolevelnumber = level.all_flamming
        self.all_sprites = level.all_sprites
        self.escape = level.escape
        self.floors = level.floors
        self.water = level.water
        self.images = level.images
        self.title = level.title
        self.to_save = level.to_save
        self.button_icons = level.button_icons
        self.timeleft = level.time*60
        self.activeButtons = level.activeButtons
        self.coconuts = pygame.sprite.Group()
        self.cursor = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        self.flamingo = pygame.sprite.Group()
        self.button_icons = pygame.sprite.Group()
        self.FlamBlocker = pygame.sprite.Group()

    def run(self):

        while not self.GameOver:

            tick = self.Clock.tick(self.FPS)

            if self.GamePaused == False:

                self.timeleft -= tick / 1000.0

                if float("%0.2f" % self.timeleft) * 10 < 0:
                    self.GameOver = True
                    self.timeleft = 0

                if len(self.flamingo) == 0 and self.FlammingsOut == self.flamingolevelnumber and len(self.FlamBlocker) == 0:
                    break

            self.events()

            if self.GamePaused == False:

                self.update()

            self.draw()

    def update(self):

        self.all_sprites.update()
        self.FlamBlocker.update()
        now = pygame.time.get_ticks()

        # In the first level we have coconuts

        if self.level_number == 2:
            if now - self.coconut_timer > Coconut_freq:
                self.coconut_timer = now

                Coconut(self)
                play_sound(self, "coconut_sound.wav")

        if now - self.flamingo_timer > self.flam_freq:
            self.flamingo_timer = now

            if self.FlammingsOut < self.flamingolevelnumber:
                self.FlammingsOut += 1
                play_sound(self, "appear2.wav")
                self.flamingo.add(Flamingo(self))

        if self.mute == True:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

        if self.action == Roles.Exploder and (len(self.FlamBlocker) != 0):

            for flam in self.FlamBlocker:
                self.FlamBlocker.remove(flam)
                self.all_sprites.remove(flam)
            play_sound(self, "explosion.wav")

    def events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.GameOver = True
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    self.GameOver = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                if not self.mute and not self.GamePaused:
                    play_sound(self, "coin_drop.ogg")

                c = Cursor(game, mx, my)
                self.cursor.add(c)

    def draw(self):

        self.cursor.draw(self.screen)
        self.cursor.remove()
        self.FlamBlocker.draw(self.screen)
        self.screen.fill(background_color)
        self.buttons.draw(self.screen)
        self.button_icons.draw(self.screen)
        self.all_sprites.draw(self.screen)

        self.images.draw(self.screen)
        self.water.draw(self.screen)
        self.escape.draw(self.screen)

        self.all_sprites.remove(self.cursor)

        BottomMenu(game)
        pygame.display.flip()


    def start_level_screen(self):
        self.screen.fill(background_color)
        self.put_text_on_the_screen(65, 1.5*MainMenuMargin, "Level {}".format(self.level_number), 40, Colors.pink4)
        self.put_text_on_the_screen(screen_width / 2, 1.75 * MainMenuMargin, self.title, 75, Colors.pink4)
        self.put_text_on_the_screen(screen_width / 2, MainMenuMargin*5, "Number of flamings:   {}".format(self.flamingolevelnumber), 40, Colors.pink3)
        self.put_text_on_the_screen(screen_width / 2, MainMenuMargin*7, "{} %  To Be Saved".format(int(100*self.to_save//self.flamingolevelnumber)), 40, Colors.pink3)
        self.put_text_on_the_screen(screen_width / 2, screen_height / 2, "Time:   {} Minutes".format(self.timeleft//60), 40, Colors.pink3)
        self.put_text_on_the_screen(screen_width / 2, screen_height * 3 / 4, "Press MOUSE button to continue", 60, Colors.pink4)
        pygame.display.flip()
        self.get_the_response()

    def next_level(self, succeded):

        self.screen.fill(background_color)
        self.level_message(succeded)
        pygame.display.flip()
        self.get_the_response()

    def start_screen(self):
        self.screen.fill(background_color)
        self.screen.blit(get_graphic("palm0.jpg", 350, 400), (screen_width-200, -50, 200, 200))
        self.screen.blit(get_graphic("palm1.jpg", 250, 300), (-10, screen_height-300, 300, 100))
        self.put_text_on_the_screen(screen_width / 2, MainMenuMargin*5, "FLEMMINGS", 75, Colors.pink4)
        self.put_text_on_the_screen(screen_width / 2, MainMenuMargin*7, "Press MOUSE button to continue", 55, Colors.pink4)
        pygame.display.flip()
        self.get_the_response()

    def end_screen(self):
        self.screen.fill(background_color)
        self.screen.blit(get_graphic("palm0.jpg", 350, 400), (screen_width-200, -50, 200, 200))
        self.screen.blit(get_graphic("palm1.jpg", 250, 300), (-10, screen_height-300, 300, 100))
        self.put_text_on_the_screen(screen_width / 2, MainMenuMargin*5, "The End", 75, Colors.pink4)
        self.put_text_on_the_screen(screen_width / 2, MainMenuMargin*7, "Thank you!", 55, Colors.pink4)
        pygame.display.flip()

    def level_message(self, succeded):

        self.screen.fill(background_color)
        if not succeded:
            text = ["Level Failed!", "Press MOUSE button to Try again"]
            self.put_text_on_the_screen(screen_width / 2, screen_height - 150, "Click ESC to leave the game", 40,  Colors.pink4)

        else:
            text = ["LEVEL SUCCEDED!",  "Press MOUSE button to continue"]

        time = self.time_left()
        self.put_text_on_the_screen(65, 1.5 * MainMenuMargin, "Level {}".format(self.level_number), 40,  Colors.pink4)
        self.put_text_on_the_screen(screen_width / 2, 1.75 * MainMenuMargin, text[0], 75, Colors.pink4)
        self.put_text_on_the_screen(screen_width / 2, 200, "You needed: {}".format(self.to_save), 40, Colors.pink3)
        self.put_text_on_the_screen(screen_width / 2, 250, "You saved: {}".format(self.FlammingsHome), 40, Colors.pink3)
        self.put_text_on_the_screen(screen_width / 2, 300, "Time left: {}:{} ".format(time[0], time[1]), 40,  Colors.pink3)
        self.put_text_on_the_screen(screen_width / 2, screen_height - 200, text[1], 55,  Colors.pink4)

    def get_the_response(self):

        pause = True
        while pause:

            self.Clock.tick(self.FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.GameOver = True
                    pause = False

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                        self.GameOver = True
                        pause = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.GameOver = False
                    pause = False

    def put_text_on_the_screen(self, x, y, text, size, color, bgcolor=background_color):
        font = pygame.font.Font(self.font, size)
        text_surface = font.render(text, True, color, bgcolor)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def time_left(self):
        return [int(self.timeleft / 60), int(self.timeleft % 60)]

    def success(self):
        self.to_save <= self.FlammingsHome

    def clear(self):
        self.FlammingsHome = 0
        self.FlammingsOut = 0
        self.flam_freq = 3000
        self.coconut_timer = 0
        self.flamingo_timer = 0


# Our Game

game = Game()
game.start_screen()
level_number = 1

while not game.GameOver:

    if level_number < 2:
        game.new(Level(level_number))
        game.start_level_screen()
        game.run()

        if game.to_save <= game.FlammingsHome : #game.success():
            game.next_level(True)
            level_number += 1
            if level_number == 2:
                game.clear()
                game.new(Level(level_number))
                game.run()

            else:
                break

        else:
            game.clear()
            game.next_level(False)

    else:
        game.next_level(True)
        game.clear()
        break

game.end_screen()
pause = True
while pause:
    game.Clock.tick(game.FPS)

    for event in pygame.event.get():

        if event.type in [pygame.KEYDOWN, pygame.QUIT, pygame.MOUSEBUTTONDOWN]:
            pause = False

pygame.quit()

from DefaultSettings import *
import pygame

class Tiles(pygame.sprite.Sprite):

    def __init__(self, x, y, image, size_x, size_y):#, move=0):
        pygame.sprite.Sprite.__init__(self)

        self.size_x = size_x
        self.size_y = size_y
        self.image = get_graphic(image, self.size_x, self.size_y)
        self.image.set_colorkey(background_color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Images(pygame.sprite.Sprite):

    def __init__(self, x, y, image, size_x=DefaultImageSize_x, size_y=DefaultImageSize_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_graphic(image, size_x, size_y)
        self.image.set_colorkey(background_color)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width / 2, screen_height / 2)
        self.rect.x = x
        self.rect.y = y

class ButtonImages(pygame.sprite.Sprite):

    def __init__(self,  x, y, image, size_x=IconSize, size_y=IconSize):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_graphic(image, size_x, size_y)
        self.image.set_colorkey(background_color)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width / 2, screen_height / 2)
        self.rect.x = x
        self.rect.y = y


class Cursor(Tiles):

    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.cursor
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.transform.scale(self.game.game_images["kursor"], (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Escape(pygame.sprite.Sprite):

    def __init__(self, x, y, image, size_x=DefaultImageSize_x, size_y=DefaultImageSize_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_graphic(image, size_x, size_y)
        self.image.set_colorkey(background_color)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width / 2, screen_height / 2)
        self.rect.x = x
        self.rect.y = y

class MenuButton1(pygame.sprite.Sprite):

    def __init__(self, game, x, y, action=None):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.image = get_graphic("woodenTile.jpg", ButtonSize, ButtonSize)
        self.image.set_colorkey(background_color)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width / 2, screen_height / 2)
        self.rect.x = x
        self.rect.y = y
        self.action = action
        self.is_active = True
        self.update()

    def Check_active(self):
        if self.is_active and self.action in self.game.activeButtons:
            return True
        else:
            return False

    def special_action(self):

        if self.action == Roles.Mute:
            self.game.mute = not self.game.mute

        elif self.action == Roles.SlowerFPS:
            self.game.flam_freq += 400

        elif self.action == Roles.FastFPS:
            self.game.flam_freq -= 400

        elif self.action == Roles.Pause:
            self.game.GamePaused = not self.game.GamePaused

        if self.action in [Roles.Bubble, Roles.Exploder, Roles.Blocker]:

            self.game.action = self.action


    def update(self):

        if self.game.GamePaused and self.action != Roles.Pause:
            self.is_active = False
            self.game.action = Roles.Pause

        if not self.game.GamePaused and not self.is_active:
            self.is_active = True

        clicked = pygame.sprite.spritecollide(self, self.game.cursor, True)

        if clicked and self.Check_active():
                self.special_action()

                if not self.game.mute:
                    play_sound(self.game, "cork.flac")

        elif clicked:
            self.game.cursor.image = get_graphic("cross.png", 20, 20)

class BottomMenu:

    def __init__(self, game):
        self.game = game
        self.ButtonSize = ButtonSize
        self.font = 'freesansbold.ttf'
        self.fontsize = 15
        self.ButtonGap = 10
        self.draw()

    def draw(self):

        __y_marg = 505
        __next_button = self.ButtonSize + self.ButtonGap

        self.rect_list = [(self.ButtonGap, __y_marg, Roles.Bubble),
                          (self.ButtonGap + __next_button, __y_marg, Roles.Digger),
                          (self.ButtonGap + 2 * __next_button, __y_marg, Roles.Blocker),
                          (self.ButtonGap + 3 * __next_button, __y_marg, Roles.Exploder),
                          (self.ButtonGap + 4 * __next_button, __y_marg, Roles.Pause),
                          (self.ButtonGap + 5 * __next_button, __y_marg, Roles.SlowerFPS),
                          (self.ButtonGap + 6 * __next_button, __y_marg, Roles.FastFPS),
                          (self.ButtonGap + 7 * __next_button, __y_marg, Roles.Mute)]

        pygame.draw.aaline(self.game.screen, Colors.pink3, (0, __y_marg - 7), (screen_width, __y_marg - 7),5)

        self.game.buttons.empty()
        for rect in self.rect_list:
            b = MenuButton1(self.game, *rect)
            self.game.buttons.add(b)
        self.load_text(self.game)

    def put_text_on_the_screen(self, game, x, y, text, size):
        self.game = game
        font = pygame.font.Font(self.font, size)
        text_surface = font.render(text, True, Colors.pink3, Colors.white)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        game.screen.blit(text_surface, text_rect)

    def load_text(self, game):

        self.game = game

        time = self.time_left(game)
        self.put_text_on_the_screen(game, screen_width - 120, screen_height - 80, "Save {}".format(self.game.to_save), self.fontsize)
        self.put_text_on_the_screen(game, screen_width - 120, screen_height - 60, "Out: {}".format(game.FlammingsOut), self.fontsize)
        self.put_text_on_the_screen(game, screen_width - 120, screen_height - 40, "Home: {}".format(str(self.game.FlammingsHome)),  self.fontsize)
        self.put_text_on_the_screen(game, screen_width - 120, screen_height - 20, "Time: {}:{} ".format(time[0], time[1]), self.fontsize)
        pygame.display.flip()

    def time_left(self, game):
        self.game = game
        return [int(game.timeleft / 60), int(game.timeleft % 60)]

class Level:

    def __init__(self, level_number):
        self.level = level_number

        self.all_sprites = pygame.sprite.Group()
        self.escape = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.images = pygame.sprite.Group()
        self.water = pygame.sprite.Group()
        self.button_icons = pygame.sprite.Group()

    def initialize(self):
        if self.level == 1:
            return self.__initialize1()
        else:
            return self.__initialize2()

    def __initialize2(self):

        self.title = "Coconut rain!"
        self.all_flamming = 20
        self.to_save = 2
        self.time = 2
        self.activeButtons = [Roles.Pause, Roles.FastFPS, Roles.SlowerFPS, Roles.Bubble, Roles.Mute]
        self.images.add( Images(50, 175, "palma_1.png", 200, 240))
        self.images.add( Images(20, 165, "palma_1.png", 200, 240))
        self.images.add( Images(-20, 185, "palma_1.png", 200, 240))
        self.images.add( Images(screen_width - 225, 165, "palma_1.png", 350, 390))
        self.images.add( Images(screen_width - 210, 185, "palma_1.png", 200, 240))
        self.images.add( Images(screen_width - 125, screen_height - 225, "kaluza.png", 100, 75))
        self.images.add( Images(95, screen_height - 225, "kaluza.png", 100, 75))
        self.images.add( Images(110, screen_height - 190, "coconut_1.png", 30, 30))

        for it in self.images:
            self.all_sprites.add(it)

        e = Escape(screen_width - 60, screen_height - 230, "Gold_0.png", 70, 45)
        self.all_sprites.add(e)
        self.escape.add(e)

        for floor in Floors_list:
            self.floors.add( Tiles(*floor, "DirtRock.png", TileSize, TileSize) )

        for water in Water_list:
            self.floors.add( Tiles(*water, "watertop.png", TileSize, int(0.5 * TileSize)) )

        self.floors.add( Tiles(20, 85, "ground.png", 200, int(0.75 * TileSize)) )
        self.floors.add( Tiles( 150, 150, "ground.png", 200, int(0.75 * TileSize)) )

        for it in self.floors:
            self.all_sprites.add(it)

        for icon in icon_list:
            self.button_icons.add( ButtonImages(*icon))

        for it in self.button_icons:
            self.all_sprites.add(it)

    def __initialize1(self):

        self.title = "Use blockers!"
        self.all_flamming = 30
        self.to_save = 15
        self.time = 3


        self.images.add(Images(screen_width/2+150, 180, "palma_1.png", 200, 240))
        self.activeButtons = [Roles.Pause, Roles.FastFPS, Roles.SlowerFPS, Roles.Exploder, Roles.Blocker, Roles.Mute]

        for it in self.images:
            self.all_sprites.add(it)

        e = Escape(screen_width-500, screen_height - 200, "Gold_0.png", 70, 45)
        self.all_sprites.add(e)
        self.escape.add(e)

        for water in Water_list:
            self.water.add( Tiles(*water, "watertop.png", TileSize, int(0.5 * TileSize)) )

        self.floors.add(Tiles(screen_width/2, screen_height - 182, "ground.png", 300, 40 ))
        self.floors.add(Tiles(65, 50, "ground.png", 200, 40))
        self.floors.add(Tiles(150, 50, "ground.png", 200, 40))
        self.floors.add(Tiles(300, 50, "ground.png", 200, 40))

        self.floors.add(Tiles(screen_width - 200, screen_width - 235, "ground.png", 200, 40))
        self.floors.add(Tiles(screen_width - 200, screen_width - 235, "ground.png", 200, 40))

        self.floors.add(Tiles(630, 145, "ground.png", 200, 40))

        self.floors.add(Tiles(85, 240, "ground.png", 200, 40))
        self.floors.add(Tiles(170, 240, "ground.png", 200, 40))
        self.floors.add(Tiles(275, 240, "ground.png", 200, 40))

        for it in self.floors:
            self.all_sprites.add(it)

        for icon in icon_list:
            self.button_icons.add(ButtonImages(*icon))

        for it in self.button_icons:
            self.all_sprites.add(it)




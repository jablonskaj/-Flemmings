from DefaultSettings import *
import pygame
import random
from random import choice
from buttons_levels import *
vector = pygame.math.Vector2


class Flamingo(pygame.sprite.Sprite):

    def __init__(self, game):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_graphics()
        self.image = self.falling_frames_r[0]
        self.image.set_colorkey(background_color)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width/2, screen_height/2)
        self.pos = vector(flamingo_start_x, flamingo_start_y)
        self.diff = vector(0.001, Speed)
        self.gravity = 0
        self.is_falling = False
        self.was_colliding = False
        self.inbubble = False
        self.exposed = True
# pilnowanko
        self.guard = False
        self.explosion = False
        self.update()

    def load_graphics(self):

        self.falling_frames_r = [pygame.transform.scale(self.game.game_images[image], (flamingoSize, flamingoSize))
                                 for image in ["fly1", "fly2"]]
        self.falling_frames_l = [pygame.transform.flip(it, True, False) for it in self.falling_frames_r]
        self.falling_in_bubble_frames = [pygame.transform.scale(self.game.game_images[image], (60, 50))
                               for image in ["bubble_fly1", "bubble_fly2"]]

        self.walking_in_bubble_frames = [pygame.transform.scale(self.game.game_images[image], (60, 50))
                                 for image in ["bubble_walk_2", "bubble_walk_1"]]

        self.walking_frames_r = [pygame.transform.scale(self.game.game_images[image], (flamingoSize, flamingoSize))
                                for image in ["fleming1", "fleming2"]]

        self.walking_frames_l = [pygame.transform.flip(it, True, False) for it in self.walking_frames_r]

        self.exploading_frames = [pygame.transform.scale(self.game.game_images[image], (Explosion_size, Explosion_size))
                               for image in ["exp1", "exp2", "exp3", "exp4", "exp5","exp6"]]

    def animation(self):

        now = pygame.time.get_ticks()
        if now - self.last_update > 200:
            self.last_update = now

            if self.diff.y > 0:
                self.current_frame = (self.current_frame + 1) % len(self.falling_frames_r)
                if not self.inbubble:
                    if self.diff.x >0:
                        self.image = self.falling_frames_r[self.current_frame]
                    else:
                        self.image = self.falling_frames_l[self.current_frame]
                else:
                    self.image = self.falling_in_bubble_frames[self.current_frame]

            elif self.diff.x > 0:
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_r)
                if not self.inbubble:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_in_bubble_frames[self.current_frame]

            elif self.diff.x < 0:
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                self.image = self.walking_frames_l[self.current_frame]
            if self.explosion:

                self.current_frame = (self.current_frame + 1)
                self.image = self.exploading_frames[self.current_frame]

                if self.image == self.exploading_frames[5]:
                    self.kill()
            else:
                pass

            self.rect = self.image.get_rect()

    def update(self):
        self.gravity = 0

        collide_down = pygame.sprite.spritecollide(self, self.game.floors, False)

        if not self.explosion:

            if self.is_falling and collide_down:
                self.diff.y = 0
                if self.diff.x > 0:
                    self.diff.x = Speed
                else:
                    self.diff.x = -Speed
                self.rect.midbottom = self.pos
                self.is_falling = False
            elif not collide_down:
                self.is_falling = True
                self.gravity = 5
                if self.diff.x > 0:
                    self.diff.x = 2
                else:
                    self.diff.x = -2
                self.diff.y = Speed

            if collide_down:
                self.pos.y = collide_down[0].rect.top


        #if self.diff.x != 0:

         #   self.rect.y -= 1
          #  collide_side = pygame.sprite.spritecollide(self, self.game.floors, False)
          #  self.rect.y += 1

           # if collide_side:
            #    self.diff.x *= -1

        # wrap flammings the sides of the screen

        if self.pos.x > screen_width - 0.5 * flamingoButtonSize and self.diff.x > 0:
            self.diff.x *= -1

        if self.pos.x + 0.5*flamingoButtonSize < 0 and self.diff.x < 0:
            self.diff.x *= -1

        self.diff.y += self.gravity
        self.pos += self.diff + 0.5 * vector(0, self.gravity)
        self.animation()
        self.rect.midbottom = self.pos

        if self.diff.y > 0:
            bum = pygame.sprite.spritecollide(self, self.game.floors, False)
            if bum:
                self.pos.y = bum[0].rect.top
                self.diff.y = 0

        self.rect.midbottom = self.pos + (5, 5)

        # Check if the flaming was clicked

        flamingo_clicked = pygame.sprite.spritecollide(self, self.game.cursor, True)

        if flamingo_clicked:
            play_sound(self.game, "cork.flac")

            if self.game.action == Roles.Bubble and self.exposed == True:
                self.exposed = False
                self.inbubble = True

            elif self.game.action == Roles.Blocker:
                if self.diff.y == 0:
                    self.kill()
                    c = Tiles(self.pos.x, self.pos.y-40, "stand.png", flamingoSize+10, flamingoSize+10)
                    self.game.FlamBlocker.add(c)
                    self.game.FlamBlocker.draw(self.game.screen)
                    self.game.all_sprites.add(c)

                # Check if the flaming was clicked

        flamingo_blocked = pygame.sprite.spritecollide(self, self.game.FlamBlocker, False)


        if flamingo_blocked and not self.was_colliding:
            self.diff.x *= -1

        self.was_colliding = flamingo_blocked

        water_hit = pygame.sprite.spritecollide(self, self.game.water, False)

        if water_hit:
            self.kill()
            play_sound(self.game, "explosion.wav")

        # Check if the flaming was hit by coconut
        if self.game.level_number == 2:

            coconut_bum = pygame.sprite.spritecollide(self, self.game.coconuts, False)

            if coconut_bum:
                if self.exposed:
                    self.explosion = True
                    self.diff.y = 0
                    self.diff.x = 0
                    play_sound(self.game, "explosion.wav")

        # Check if the flaming reach the exit

        reach_exit = pygame.sprite.spritecollide(self, self.game.escape, False)

        if reach_exit:
            self.game.FlammingsHome += 1
            self.kill()
            play_sound(self.game, "spell3.wav")


class Coconut(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.coconuts
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = pygame.transform.scale(self.game.game_images["coconut"], (Coconut_size,Coconut_size+2))
        self.image.set_colorkey(background_color)
        self.rect = self.image.get_rect()
        self.pos = vector(random.randrange(50, screen_width-50), random.randrange(-10, 10))
        self.diff = vector(choice([-10, 10]), 5)
        self.gravity = 1
        if self.pos.x > screen_width:
           self.diff.x = - self.diff.x
        self.mask = pygame.mask.from_surface(self.image)
        self.update()

    def update(self):

        self.pos.x += self.diff.x
        self.pos.y += self.diff.y + self.gravity
        self.pos += self.diff + 0.5 * vector(0, self.gravity)

        self.rect.midbottom = self.pos
        collision = pygame.sprite.spritecollide(self, self.game.floors, False)#,  pygame.sprite.collide_mask)
        if collision:
            self.kill()

        if self.rect.left > screen_width + 100 or self.rect.right < -100:
            self.kill()


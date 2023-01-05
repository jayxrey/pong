#===============================================================================================#
# Name        : pingpong.py                                                                    #
# Description : Python version ping-pong game.                                               #
# Author      : Jay Reyes (COMP112.2)                                                                #                                                                    #
#===============================================================================================#
#import needed libraries
import pygame
import os
import sys
import time


#defining colors
black=(0,0,0)
white=(255,255,255)
d_green=(0,100,0)
green=(0,255,0)
d_blue=(10,100,200)
blue=(0,0,255)
yellow=(255,238,0)
grey=(210,210,210)

#defining variables
screensz = (600,500)
bar_width = 80
bar_move = 5
ball_diam = 10
ball_rad = ball_diam//2
#=============================================================================#
#                           Function Definitions                              #
#=============================================================================#

class Ball(object):
     """creates a ball bounded by screen edges"""
     def __init__(self, screensz):
          self.screensize = screensz

          self.centerx = int(screensz[0]*0.5)
          self.centery = int(screensz[1]*0.5)

          self.radius = 8

          self.rect = pygame.Rect(self.centerx-self.radius,
                                  self.centery-self.radius,
                                  self.radius*2, self.radius*2)

          self.color = (blue)

          self.direction = [1,1]

          self.speedx = 2
          self.speedy = 5

          self.hit_edge_bottom = False

     def update(self, bar):
          """changes the direction of the ball/ causes ball to bounce"""
          self.centerx += self.direction[0]*self.speedx
          self.centery += self.direction[1]*self.speedy

          self.rect.center = (self.centerx, self.centery)

          if self.rect.top <= 0:
               self.direction[1] = 1
          if self.rect.right >= self.screensize[0]-1:
               self.direction[0] = -1
          if self.rect.left <= 0:
               self.direction[0] = 1
          if self.rect.colliderect(bar.rect):
               self.direction[1] = -1
          elif self.rect.bottom >= self.screensize[1]:
               self.hit_edge_bottom = True

     def render(self, screen):
          pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
          pygame.draw.circle(screen, (0,0,0), self.rect.center, self.radius, 1)

class Bar(pygame.sprite.Sprite):
     """creates bar for ball(s) to bounce off of controlled by R & L keys"""
     def __init__(self):
          pygame.sprite.Sprite.__init__(self)
          self.image = pygame.Surface((bar_width,10))
          self.image.fill(black)
          pygame.draw.rect(self.image, green, (0,0, bar_width, 10))
          self.rect = self.image.get_rect()
     def move_right(self):
          if self.rect.x < screensz[0]-bar_width:
               self.rect.x += bar_move
     def move_left(self):
          if self.rect.x > 0:
               self.rect.x -= bar_move

#=============================================================================#
#                               Main Game Part                                #
#=============================================================================#
def start(screen):

    pygame.display.set_mode(screensz)
    # create a font object
    font = pygame.font.Font(None, 32)

    # create a text surface object,
    # on which text is drawn on it.
    title = font.render('Pong Game', True, green)
    # set the position of the text.
    title_pos = title.get_rect(centerx = screensz[0]//2, y = screensz[1]//3)

    play = font.render('Play', True, white, blue)
    play_pos = play.get_rect(centerx = screensz[0]//2, y = screensz[1]//1.5)

    instructions = font.render('Use arrow keys to move the bar', True, white)
    instructions_pos = instructions.get_rect(centerx = screensz[0]//2, y = screensz[1]//2.5)

    # infinite loop
    while True:
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))

        screen.blit(title, title_pos)
        screen.blit(play, play_pos)
        screen.blit(instructions, instructions_pos)

        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get():

            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:

                # deactivates the pygame library
                pygame.quit()

                # quit the program.
                quit()

            #janky play button
            if event.type == pygame.MOUSEBUTTONDOWN and 276 <= pygame.mouse.get_pos()[0] <= 325 and 335 <= pygame.mouse.get_pos()[1] <= 356 :
                return();

            # Draws the surface object to the screen.
            pygame.display.update()

def game(screen):
    #create a list which contains all sprites
    all_sprites_list = pygame.sprite.Group()

    #bar specs
    bar = Bar()
    bar.rect.x = screensz[0]//2 - 30    #centering the bar
    bar.rect.y = screensz[1]-10

    #call on ball
    ball = Ball(screensz)

    #add sprites
    barsprite = pygame.sprite.RenderPlain(bar)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0,0))
    pygame.display.flip()

    #begins timer for "score"
    t1=time.time()

    #if player clicks x or esc key, quits pygame
    playing=True
    clock = pygame.time.Clock()
    while playing:
         for event in pygame.event.get():
              if event.type == pygame.QUIT:
                   # deactivates the pygame library
                   pygame.quit()

                   # quit the program.
                   quit()
              elif event.type==pygame.KEYDOWN:
                   if event.key==pygame.K_ESCAPE:
                        # deactivates the pygame library
                        pygame.quit()

                        # quit the program.
                        quit()
         #watches out for key presses
         pressed = pygame.key.get_pressed()
         if pressed[pygame.K_LEFT]:
              bar.move_left()
         if pressed[pygame.K_RIGHT]:
              bar.move_right()
         ball.update(bar)

         if ball.hit_edge_bottom:
              t2=time.time()
              print('You lost :( you lasted', t2-t1,'sec.')
              playing = False
         screen.fill((0, 0, 0))
         barsprite.update()
         barsprite.draw(screen)
         ball.render(screen)
         pygame.display.flip()
         clock.tick(60)


    return ()

def over(screen):
    pygame.display.flip()
    font = pygame.font.Font(None, 50)
    title = font.render('GAME OVER', True, green)
    title_pos = title.get_rect(centerx = screensz[0]//2, y = screensz[1]//3)

    play = font.render('Play Again', True, white, blue)
    play_pos = play.get_rect(centerx = screensz[0]//2, y = screensz[1]//1.5)

    # infinite loop
    while True:
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((0, 0, 0))

        screen.blit(title, title_pos)
        screen.blit(play, play_pos)

        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get():

            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:

                # deactivates the pygame library
                pygame.quit()

                # quit the program.
                quit()

            #janky play button
            if event.type == pygame.MOUSEBUTTONDOWN and 276 <= pygame.mouse.get_pos()[0] <= 325 and 335 <= pygame.mouse.get_pos()[1] <= 356 :
                return();

            # Draws the surface object to the screen.
            pygame.display.update()


def main():
    #initiates pygame
    pygame.init()

    #create screen specs
    screen = pygame.display.set_mode(screensz)
    pygame.display.set_caption("Pong Game")

    while True:
        start(screen)
        game(screen)
        over(screen)

main()

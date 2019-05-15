import pygame
import random
# first we initialize the pygame
pygame.init()


class Ball():
    ball = pygame.image.load('cannon_ball_64x64.png')
    def __init__(self, x = 50, y = 400, height = 64, width = 64):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.vel = 5
        self.hitbox = (self.x + 17, self.y +2, width, height) # hitbox params
        self.left = False
        self.right = False
        self.jump = False
        self.stationary = True
        self.jumpcount = 10
        self.double_jump = False
        self.gravity = 1
        self.jump_vel = 20
        self.apex = 0
        self.hitbox = (self.x , self.y , 29, 29)

    def draw(self, win):
        ''' This is going to draw on the window that we pass in
                think of the window as the background and the ball is going to be drawn on top of it'''
        if not self.stationary:
            if self.left:
                win.blit(self.ball, (self.x, self.y))

            else:
                win.blit(self.ball, (self.x, self.y))
        else:
            if self.right:
                win.blit(self.ball, (self.x, self.y))
            else:
                win.blit(self.ball, (self.x, self.y))
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        self.hitbox = (self.x , self.y, self.width, self.height)

class Game:
    '''The game class is the entire class needed to run the game
            it creates the ball object as well as the canvas to be drawn on'''
    def __init__(self, width=500, h=500):
        self.gamelen = h
        self.gamewidth = width
        self.ball = Ball()
        self.canvas = Canvas(self.gamelen, self.gamewidth)
        self.hoop = Hoop()
        self.music = pygame.mixer.music.load('music.mp3')
        self.score = 0
        pygame.mixer.music.play(-1)

    def run(self):
        game = True
        previous_hit_time = pygame.time.get_ticks()
        while game:
            pygame.time.delay(10)  # 10 milisecond deplay

            # end the game on press of button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False

            # print(self.ball.y)

            keys = pygame.key.get_pressed()
            print(self.ball.y)
            print(self.ball.x)

            if keys[pygame.K_LEFT] and self.ball.x > self.ball.vel:
                self.ball.x -= self.ball.vel
                self.ball.left = True
                self.ball.right = False

            elif keys[pygame.K_RIGHT] and self.ball.x < self.gamewidth - self.ball.width - self.ball.vel:
                self.ball.x += self.ball.vel
                self.ball.right = True
                self.ball.left = False

            else:
                self.ball.stationary = True

            if not (self.ball.jump):
                if keys[pygame.K_SPACE]:
                    self.ball.jump = True
                    jump_time = pygame.time.get_ticks()
            else:
                self.ball.jump_vel -= 1
                # print(self.ball.y)
                self.ball.y -= self.ball.jump_vel
                print(self.ball.y)

                if self.ball.jump_vel < 0:
                    if keys[pygame.K_SPACE]:
                        self.ball.jump_vel += 20
                if self.ball.y >= 400:
                    self.ball.jump_vel += 20
                    self.ball.apex = self.ball.jump_vel / 2

                # if at the bottom of the screen where y cooordinate is greater than 400
                if self.ball.y >= 400:
                    self.ball.jump = False
                    self.ball.jump_vel = 20
                    # self.ball.jump_vel = 20

            hit_time = pygame.time.get_ticks()
            if self.ball.hitbox[1] < self.hoop.hitbox[1] + self.hoop.hitbox[3] and self.ball.hitbox[1] + self.ball.hitbox[3] > self.hoop.hitbox[1]\
                    and hit_time - previous_hit_time > 500:
                if self.ball.hitbox[0] + self.ball.hitbox[2] > self.hoop.hitbox[0] and self.ball.hitbox[0] < self.hoop.hitbox[0] + self.hoop.hitbox[
                    2]:
                        previous_hit_time = hit_time
                        self.score +=1
                        self.hoop.randomize_location()


            # updating the canvas
            self.canvas.draw_background(self.score)
            self.hoop.draw(self.canvas.get_canvas())
            self.ball.draw(self.canvas.get_canvas())
            self.canvas.update()
            # print(f'hoop {# self.hoop.hitbox}')
            # print(f'ball {self.ball.hitbox}')


class Canvas:
    '''this is a class meant to draw the background and update texts, and images'''

    def __init__(self, h, w):
        self.bg = pygame.image.load('bg.jpg')
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((self.width, self.height)) # this is the "win"
        self.font = pygame.font.SysFont('comicans', 30, True)

    def get_canvas(self):
        '''This returns the screen acting as a window to be drawn on'''
        return self.screen

    def draw_background(self, score):
        '''this blits the background for the game'''
        self.text = self.font.render(f'Score: {score}', 1, (0,0,0))
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.text, (390, 10))

    @staticmethod
    def update():
        '''this is a static method that is used to update the pygame interface'''
        pygame.display.update()


class Hoop:
    def __init__(self):
        self.color = (0,0,0)
        self.loc = [400, 200, 100, 20]
        self.hitbox = [self.loc[0], self.loc[1], self.loc[0], self.loc[3]]
        self.counter = 0



    def randomize_location(self):
        # x = random.choice([0,400])
        if self.counter % 2 == 0:
            x = 0
        else:
            x = 400
        self.counter +=1
        y = random.randint(100,300)
        self.loc = [x,y,100,20]
        if x == 400:
            self.hitbox = [self.loc[0], self.loc[1], self.loc[0], self.loc[3]]
        else:
            self.hitbox = [self.loc[0], self.loc[1], self.loc[0] + self.loc [2], self.loc[3]]

    def draw(self, win):
        pygame.draw.ellipse(win, self.color, self.loc) # # x, y, width, height
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

game = Game()
game.run()


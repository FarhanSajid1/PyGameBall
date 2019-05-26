import pygame

# first we initialize the pygame
pygame.init()
gamelen, gamewidth = 500, 500
bg = pygame.image.load('bg.jpg')
win = pygame.display.set_mode((gamelen, gamewidth))

class Ball():
    ball = pygame.image.load('cannon_ball_64x64.png')
    def __init__(self, x = 50, y = 400, height = 64, width = 64):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.vel = 5
        self.hitbox = (self.x + 17, self.y +2, 31, 57) # hitbox params
        self.left = False
        self.right = False
        self.jump = False
        self.stationary = True
        self.jumpcount = 10
        self.double_jump = False
        self.gravity = 1
        self.jump_vel = 20
        self.apex = 0
        self.stop = -10

    def draw(self, win):
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

def redraw():
    win.blit(bg, (0, 0))  # blit in the top right corner
    ball.draw(win)
    pygame.display.update()  # update the display

ball = Ball()
game = True
while game:
    pygame.time.delay(10) # 10 milisecond deplay

    # end the game on press of button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    # print(ball.y)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and ball.x > ball.vel:
        ball.x -= ball.vel
        ball.left = True
        ball.right = False

    elif keys[pygame.K_RIGHT] and ball.x < gamewidth - ball.width - ball.vel:
        ball.x += ball.vel
        ball.right = True
        ball.left = False

    else:
        ball.stationary = True

    if not (ball.jump):
        if keys[pygame.K_SPACE]:
            ball.jump = True
            jump_time = pygame.time.get_ticks()
    else:
        ball.jump_vel -= 1
        print(ball.y)
        ball.y -=ball.jump_vel

        if ball.jump_vel < 0:
            if keys[pygame.K_SPACE]:
                ball.jump_vel +=20
        if ball.y >= 400:
            ball.jump_vel += 20
            ball.apex = ball.jump_vel / 2

        if ball.y >= 400:
            ball.jump = False
            ball.jump_vel = 20
            # ball.jump_vel = 20



    redraw()


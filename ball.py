import pygame

# first we initialize the pygame
pygame.init()

bg = pygame.image.load('bg.jpg')
gamelen, gamewidth = 500, 500
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
        self.max_jump =3
        self.current_jump = 0

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




ball = Ball()
def redraw():
    win.blit(bg, (0,0)) # blit in the top right corner
    ball.draw(win)
    pygame.display.update() # update the display

game = True

previous_hit_time = pygame.time.get_ticks()
while game:
    pygame.time.delay(10) # 10 milisecond deplay

    # end the game on press of button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and ball.x > ball.vel:
        ball.x -= ball.vel
        ball.left = True
        ball.right = False
        ball.jump = True

    elif keys[pygame.K_RIGHT] and ball.x < gamewidth - ball.width - ball.vel:
        ball.x += ball.vel
        ball.right = True
        ball.left = False
        ball.jump = True

    else:
        ball.stationary = True

    if not (ball.jump):
        if keys[pygame.K_SPACE]:
            ball.jump = True
            jump_time = pygame.time.get_ticks()
    else:
        # hit_time = pygame.time.get_ticks()
        # if ball.current_jump < ball.max_jump and hit_time - previous_hit_time > 800:
        #     ball.current_jump +=1
        #     if keys[pygame.K_SPACE]:
        #         ball.jumpcount +=10
        #         apex +=10
        #         previous_hit_time = hit_time
        #     if ball.current_jump == ball.max_jump:
        #         ball.current_jump = 0
        #
        apex = ball.jumpcount / 2
        neg = 1
        if ball.jumpcount >= -10:
            neg = 1
            if ball.jumpcount < apex:
                neg = -1
            ball.y -= (ball.jumpcount **2) * .5 * neg
            ball.jumpcount -=1
        else:
            ball.jump = False
            ball.jumpcount = 10
    redraw()


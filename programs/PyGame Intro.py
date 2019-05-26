import pygame
import time

pygame.init()

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')


#this initializes a display with tuple for height and width
'''this is the game environment dummy'''
gamelen, gamewidth = 800,800
win  = pygame.display.set_mode((gamelen, gamewidth))
pygame.display.set_caption("Farhan's Game")
score = 0

'''Initializing music'''
hit = pygame.mixer.Sound('hit.wav')
bullet = pygame.mixer.Sound('bullet.wav')

music = pygame.mixer.music.load('music.mp3')
#this actually plays the music and loops through it continuously
pygame.mixer.music.play(-1)

class player():
    def __init__(self, x = 50, y = 400, height = 64, width = 64):
        # game variables
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.vel = 5
        # create left right and walk count variables
        self.left = False
        self.right = False
        self.jumping = False
        self.jumpcount = 10
        self.walkcount = 0
        self.standing = True
        #adding a hitbox to surround the characters
        self.hitbox = (self.x + 17, self.y +11, 29, 52)
        self.health = 10
        self.visible = True

    def draw(self, win):
        '''This function is speficially for redrawing the character
                The window is passed in, i.e the background that we are going to want to use '''
        if self.walkcount + 1 > 27:  # if the frames are more than 27 we reset them to 0 because of amount of images
            self.walkcount = 0

        if self.visible:  # draw only if the character is visible
            if not (self.standing): # if you are not standing..
                if self.left:
                    win.blit(walkLeft[self.walkcount // 3], (self.x, self.y))  # we use floor division to round down
                    self.walkcount += 1

                elif self.right:
                    win.blit(walkRight[self.walkcount // 3], (self.x, self.y))
                    self.walkcount += 1

            else:  # else just means that if the character is standing still or jumping initially
                if self.right:
                    win.blit(walkRight[0], (self.x, self.y))
                else:
                    win.blit(walkLeft[0], (self.x, self.y))
            # we have to update the hitbox whenever we move
            '''health bar'''
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))  # red
            pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, (50 - (5 * (10 - self.health))), 10)) # green
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win , (255,0 ,0), self.hitbox, 2) # 2 represents the rectangle size


    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False



class enemy():
    '''These are the image loading variables that we will be using'''
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    def __init__(self, x = 0, y = 400, height =64, width=64, end=gamewidth):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.vel = 5
        self.end = end - self.width - self.vel
        self.walkcount = 0
        self.path = [self.x, self.end]
        # adding an enemy hitbox
        self.hitbox = (self.x + 17, self.y +2, 31, 57) # (x,y, width, height)
        self.health = 10
        self.visible = True

    def draw(self, win):
        '''this function is responsible for letting the enemy walk'''
        self.move()

        if self.visible: # draw only if the character is visible
            if self.walkcount + 1 >= 33: #if the walkcount is greater than 33 we reset it
                self.walkcount = 0

            if self.vel > 0: #if velocity is positive (moving right)
                win.blit(self.walkRight[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
            else:
                win.blit(self.walkLeft[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))  # red
            pygame.draw.rect(win, (0, 255, 0), (self.hitbox[0], self.hitbox[1] - 20, (50 - (5 * (10 - self.health))), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0: #if the velocity is positive and moving to the right
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else: # once we can no longer move to the right we change the velocity to the enemy turn around
                self.vel = self.vel * -1 #this turns us around
                self.walkcount = 0 # we reset the walk count to begin at 0
        else:
            '''Remember that the vel is negative in this scenario, once self.x is negative you turn around.'''
            if self.x + self.vel > self.path[0]:
                self.x += self.vel
            else: # once we can no longer move to the right we change the velocity to the enemy turn around
                self.vel = self.vel * -1 #this turns us around
                self.walkcount = 0 # we reset the walk count to begin at 0

    def hit(self):
        '''When we hit the monster, we subtract the health by 1 until he has no health and he dies'''
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False


class Projectile():
    def __init__(self, x, y, facing, radius=6, color=(0,0,0), vel = 10):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = vel * facing

    def draw(self, win):
        pygame.draw.circle(win,self.color, (self.x, self.y), self.radius)

#initializations
man = player()
bullets = []
troll = enemy()
font = pygame.font.SysFont('comicans', 30, True) # setting the font and making the font bold
font1 = pygame.font.SysFont('comicans', 30, True)

# drawing function
def redraw():
    # walkcount is just for us being able to draw and make the animation feel more realistic!
    win.blit(bg, (0,0))
    text = font.render(f'Score: {score}', 1, (0,0,0))
    win.blit(text, (390, 10))
    man.draw(win) # passing in the background window to start at 0,0 the right corner
    troll.draw(win)
    #add the bullets so that they are drawn
    for bullet in bullets:
        bullet.draw(win)
    if not (troll.visible) or not (man.visible):
        text1 = font1.render(f'Do you want to replay? Press y to continue', 1 , (0,0,0))
        win.blit(text1, (gamewidth//2 - 200, gamelen//2))
    pygame.display.update()


a = True
# this list will store all the bullets that we create
bullets = []
previous_time = pygame.time.get_ticks()
previous_hit_time = pygame.time.get_ticks()
while a:
    '''End the game if the enemy is killed'''

    pygame.time.delay(10) #this delays the game by 100 milliseconds

    #processing the events on the keyboard
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            a = False
    keys = pygame.key.get_pressed() #this returns all the keys that are pressed
    # we introduce constraints in order to create boundaries

    '''This manages the bullets destroying them and registering hits'''

    for bullet in bullets:
         # check if the bullet has hit the character!
        if man.visible and troll.visible:
            # if the y+ radius is less than the y top corner plus the height of the hitbox
            # and if the bullet + radius is less than the top right
            if bullet.y + bullet.radius < troll.hitbox[1] + troll.hitbox[3] and bullet.y + bullet.radius  > troll.hitbox[1]:
                if bullet.x + bullet.radius > troll.hitbox[0] and bullet.x + bullet.radius < troll.hitbox[0] + troll.hitbox[2]:
                    hit.play() # play the hit music
                    troll.hit() # runs the troll.hit method
                    score +=1
                    bullets.pop(bullets.index(bullet))

        if bullet.x < gamewidth and bullet.x > 0: # if the bullet is on screen
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # Restart after the game ends
    if not (troll.visible) or not (man.visible):
        if keys[pygame.K_y]:
            troll.health = 10
            troll.visible = True
            man.health = 10
            man.visile = True
            score = 0

    # if the goblin hits me!
    hit_time = pygame.time.get_ticks()
    # hitbox [x, y, width, height]
    if man.visible and troll.visible:
        if man.hitbox[1] < troll.hitbox[1] + troll.hitbox[3] and man.hitbox[1] + man.hitbox[3] > troll.hitbox[1] and \
            hit_time - previous_hit_time > 500:
            if man.hitbox[0] + man.hitbox[2] > troll.hitbox[0] and man.hitbox[0] < troll.hitbox[0] + troll.hitbox[2]:
                previous_hit_time = hit_time
                man.hit()
                score -=1
                hit.play()
    '''If man.y < troll's y plus height and man height + length greater than troll's height
       if man'.x  + width greater than right side of troll and man.x less than troll.x + width'''

    '''Registering Movements!'''
    # if the space bar is pressed create a new bullet
    if keys[pygame.K_SPACE]:
        current_time = pygame.time.get_ticks()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5 and current_time - previous_time > 500:
            previous_time = current_time
            bullets.append(Projectile(round(man.x + man.width//2), round(man.y + man.width//2), facing=facing))

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        # we create left, right, variables so we know what animation essentially that we have to use when walking...
        man.left = True
        man.right = False
        man.standing = False

    elif keys[pygame.K_RIGHT] and man.x < gamewidth - man.width - man.vel :
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    #if the character is standing still
    else:
        man.standing = True
        man.walkcount = 0

    # we are going to create a jump variable which turns off y movement when jump is activated.
    if not (man.jumping): #meaning if jumping is false enable these
        if keys[pygame.K_UP]:
            man.jumping = True # when space is pressed this will be turn into true
            # we make both right and left, false so that the character's initial build loads..
            man.walkcount = 0
    else:
        neg = 1
        '''this essentially checks the jump, once the jump is lower than -10 i.e when the parabola hits 0
        This if statement is rendered false, and the jumping turns into false.'''
        if man.jumpcount >= -10:
            neg = 1
            if man.jumpcount < 0:
                neg = -1
            man.y -= (man.jumpcount **2) * .5 * neg
            man.jumpcount -= 1
        else:
            man.jumping = False
            man.jumpcount = 10
    redraw()



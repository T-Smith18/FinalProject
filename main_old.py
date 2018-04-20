import pygame
from pygame import *
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,size,):
        self.x = x
        self.y = y
        self.size = size
        self.jumping= False
        self.jump_offset= 0
        self.movex=0
        self.movey=0
        self.frame = 0
    def control(self,x,y):
        '''
        control player movement
        '''
        self.movex += x
        self.movey += y
    def update(self):
        '''
        Update sprite position
        '''
        self.rect.x = self.rect.x + self.movex   
        self.rect.y = self.rect.y + self.movey

def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type== KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
def jumpKeys(Player):
    #keypress function
    keys= pygame.key.get_pressed()
    if keys[K_SPACE] and Player.jumping == False and Player.jump_offset == 0:
        Player.jumping=True
def moveKeys(Player):
    if event.type==pygame.KEYDOWN:
        if event.key == pygame.K_w:
            print("placeholder")
        if event.key == pygame.K_s:
            print("placeholder")
        if event.key == pygame.K_a:
            print("placeholder")
        if event.key == pygame.K_d:
            print("placeholder")
  
    if event.type==pygame.KEYUP:
        if event.key == pygame.K_w:
            print("placeholder")
        if event.key == pygame.K_s:
            print("placeholder")
        if event.key == pygame.K_a:
            print("placeholder")
        if event.key == pygame.K_d:
            print("placeholder")

pygame.image.load("resources/graphics/smiley.png")


        




def goJump(Player):
    global jump_height

    if Player.jumping:
        #jump speed upward
        Player.jump_offset += 8
        if Player.jump_offset >= jump_height:
            Player.jumping=False
    elif Player.jump_offset > 0 and Player.jumping == False:
        #jump speed falling
        Player.jump_offset -=10


    

#SETUP
W, H = 1280,720
HW = W//2
HH =  H//2
AREA = W+H
SCREEN=1280,720


#Defining colors
WHITE = (255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
SOLID_FILL=0

p=Player(HW,HH,30)
jump_height=200

pygame.init()
CLOCK= pygame.time.Clock()
DS=pygame.display.set_mode((W,H))
FPS=30
ANI=4

while True:
    events()
    jumpKeys(p)
    goJump(p)

    #pygame.draw.circle(DS, WHITE, (p.x, p.y - p.jump_offset), p.size, SOLID_FILL)
    platform_color=RED
    pygame.draw.rect(DS, platform_color, (HW-100, HH+ p.size, 200, 10), SOLID_FILL)

    #if p.jump_offset == 0:
       # platform_color=RED
       # pygame.draw.rect(DS, platform_color, (HW-100, HH+ p.size, 200, 10), SOLID_FILL)

    pygame.display.update()
    CLOCK.tick(FPS)
    DS.fill(BLACK)


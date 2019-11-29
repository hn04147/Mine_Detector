import sys
import pygame
from pygame.locals import *
from image import *

TARGET_FPS=30

clock = pygame.time.Clock()

#background color
WHITE=(255,255,255)
COLOUR=(211,211,211)

pygame.init()
screen=pygame.display.set_mode((500,500), DOUBLEBUF)
pygame.display.set_caption("Mine Sweeper")

#쓸데없는거
a=[[0]*10 for i in range(10)]
num=1
for i in range (0,10):
    for j in range (0,10):
        a[i][j]=num
        num=num+1
for i in range (0,10):
    for j in range (0,10):
        print(a[i][j], end=' ')
    print("\n")
        
#def mouse_coordinate_to_single_coordinate(mousex, mousey):
    
    

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        #when left mouse button up get mouse coordinate
        if event.type==MOUSEBUTTONUP:
            mousex, mousey = pygame.mouse.get_pos()
            print(mousex,mousey)
    screen.fill(COLOUR)

    for i in range (0,10):
        for j in range (0,10):
            screen.blit(blank,(i*50,j*50))
    screen.blit(mine,(250,350))
    screen.blit(blank_clicked,(150,250))
    screen.blit(blank_flag,(100,100))

    pygame.display.flip()
    clock.tick(TARGET_FPS)

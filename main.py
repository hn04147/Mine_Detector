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
mine_array=[[0]*10 for i in range(10)]
for i in range (0,10):
    for j in range (0,10):
        print(mine_array[i][j], end=' ')
    print("\n")
        

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        #when left mouse button up get mouse coordinate
        if event.type==MOUSEBUTTONUP:
            mousex, mousey = pygame.mouse.get_pos()
            print("mousex:", mousex, "mousey:", mousey)
            #마우스 좌표와 실제 좌표의 x,y 값이 반대로여서 x,y를 반대로 설
            y = mousex//50
            x = mousey//50
            print("x=", y, "y=", x)
            mine_array[x][y]=1

            #print array
            for i in range (0,10):
                for j in range (0,10):
                    print(mine_array[i][j], end=' ')
                print("\n")
            
    screen.fill(COLOUR)

    for i in range (0,10):
        for j in range (0,10):
            if mine_array[j][i]==0:
                screen.blit(blank,(i*50,j*50))
            elif mine_array[j][i]==1:
                screen.blit(blank_clicked,(i*50,j*50))

    '''mine_list=[]
    mine_n=0

    while mine_n<11:
        mine_x=random.randrange(0,11)
        mine_y=random.randrange(0,11)
        screen.blit(mine,(mine_x*50,mine_y*50+100))
        mine_list.append(mine_x)
        mine_list.append(mine_y)
        mine_n=mine_n+1
    
    print(mine_list)'''
    
    #screen.blit(mine,(250,350))
    #screen.blit(blank_flag,(100,100))

    pygame.display.flip()
    clock.tick(TARGET_FPS)

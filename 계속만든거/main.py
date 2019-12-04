import sys
import pygame
from pygame.locals import *
from image import *
import random

TARGET_FPS=30
clock = pygame.time.Clock()

#global
MINE_NUM=20
row = 10
col = 10

#background color
WHITE=(255,255,255)
COLOUR=(211,211,211)

pygame.init()
screen=pygame.display.set_mode((col*50,row*50), DOUBLEBUF)
pygame.display.set_caption("Mine Sweeper")


#0부터 시작하는 mine_array 0으로 초기화
#LEFTMOUSEBUTTON일경우 공백이고 주변에 지뢰가 있을 경우 주변 지뢰 수 n으로 치환
#그냥 공백일 경우는 -1로 치환
#지뢰를 클릭했을 경우 10 게임오버
#RIGHTMOUSEBUTTON일경우 flag 이미지로 바꾸고 9로 치환
after_click=[[0]*col for i in range(row)]       


#지뢰가 있으면 -1, 주변에 지뢰가 있으면 지뢰수 n, 주변에 지뢰가 없으면 0
#처음엔 0으로 초기화
before_click=[[0]*col for i in range(row)]

#지뢰 10개 랜덤으로 배치 0->-1
index=0
while index < MINE_NUM:
    randomx = random.randrange(0,row)
    randomy = random.randrange(0,col)
    if before_click[randomx][randomy] == 0:
        before_click[randomx][randomy] = -1
        index = index + 1


################################################################################
        
#공백 주변에 있는 지뢰의 수를 배열에 입력
#1) 모서리에 걸치지 않는 칸부터 설정
# _________
# | * * * |
# | * * * |
# | * * * |
# ---------
for i in range (1,row-1):
    for j in range (1,col-1):
        if before_click[i][j]!=-1:
            index = 0
            for y in range (j-1, j+2):
                if before_click[i-1][y]==-1:
                    index = index + 1
                if before_click[i+1][y]==-1:
                    index = index + 1
            if before_click[i][j-1]==-1:
                index = index + 1
            if before_click[i][j+1]==-1:
                index = index + 1
            before_click[i][j]=index
#2) 꼭짓점칸 설정
#  * ----- *
#  |       |
#  |       |
#  |       |
#  * ----- *
#(0,0):
if before_click[0][0]!=-1:
    if before_click[0][1]==-1: before_click[0][0]+=1
    if before_click[1][1]==-1: before_click[0][0]+=1
    if before_click[1][0]==-1: before_click[0][0]+=1
#(0,col-1):
if before_click[0][col-1]!=-1:
    if before_click[0][col-2]==-1: before_click[0][col-1]+=1
    if before_click[1][col-2]==-1: before_click[0][col-1]+=1
    if before_click[1][col-1]==-1: before_click[0][col-1]+=1
#(row-1,0):
if before_click[row-1][0]!=-1:
    if before_click[row-2][0]==-1: before_click[row-1][0]+=1
    if before_click[row-2][1]==-1: before_click[row-1][0]+=1
    if before_click[row-1][1]==-1: before_click[row-1][0]+=1
#(row-1,col-1):
if before_click[row-1][col-1]!=-1:
    if before_click[row-2][col-2]==-1: before_click[row-1][col-1]+=1
    if before_click[row-2][col-1]==-1: before_click[row-1][col-1]+=1
    if before_click[row-1][col-2]==-1: before_click[row-1][col-1]+=1
#3) 모서리칸 설정
#    * * * 
#  *       *
#  *       *
#  *       *
#    * * *
#UPSIDE
for i in range (1,col-1):
    if before_click[0][i]!=-1:
        if before_click[0][i-1]==-1: before_click[0][i]+=1
        if before_click[0][i+1]==-1: before_click[0][i]+=1
        for j in range (i-1, i+2):
            if before_click[1][j]==-1: before_click[0][i]+=1
#DOWNSIDE
for i in range (1,col-1):
    if before_click[row-1][i]!=-1:
        if before_click[row-1][i-1]==-1: before_click[row-1][i]+=1
        if before_click[row-1][i+1]==-1: before_click[row-1][i]+=1
        for j in range (i-1, i+2):
            if before_click[row-2][j]==-1: before_click[row-1][i]+=1
#LEFTSIDE
for i in range (1, row-1):
    if before_click[i][0]!=-1:
        if before_click[i-1][0]==-1: before_click[i][0]+=1
        if before_click[i+1][0]==-1: before_click[i][0]+=1
        for j in range (i-1, i+2):
            if before_click[j][1]==-1: before_click[i][0]+=1
#RIGHTSIDE
for i in range (1, row-1):
    if before_click[i][col-1]!=-1:
        if before_click[i-1][col-1]==-1: before_click[i][col-1]+=1
        if before_click[i+1][col-1]==-1: before_click[i][col-1]+=1
        for j in range (i-1, i+2):
            if before_click[j][col-2]==-1: before_click[i][col-1]+=1
            
################################################################################



for i in range (0,row):
    for j in range (0,col):
        print("%3d"%before_click[i][j],end=' ')
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

            if before_click[x][y]==0:
                after_click[x][y]=-1
            elif before_click[x][y]==-1:
                after_click[x][y]=10
            elif before_click[x][y] == 1:
                after_click[x][y] = 1
            elif before_click[x][y] == 2:
                after_click[x][y] = 2
            elif before_click[x][y] == 3:
                after_click[x][y] = 3
            elif before_click[x][y] == 4:
                after_click[x][y] = 4
            elif before_click[x][y] == 5:
                after_click[x][y] = 5
            elif before_click[x][y] == 6:
                after_click[x][y] = 6
            elif before_click[x][y] == 7:
                after_click[x][y] = 7
            elif before_click[x][y] == 8:
                after_click[x][y] = 8

            #print array
            '''print("mine_array:")
            for i in range (0,row):
                for j in range (0,col):
                    print("%3d"%after_click[i][j], end=' ')
                print("\n")'''
            
    

    #이미지 출력
    for i in range (0,col):
        for j in range (0,row):
            if after_click[j][i]==0:
                screen.blit(blank,(i*50,j*50))
            elif after_click[j][i]==-1:
                screen.blit(blank_clicked,(i*50,j*50))
            elif after_click[j][i]==10:
                screen.blit(mine,(i*50,j*50))
            elif after_click[j][i]==1:
                screen.blit(num1, (i*50,j*50))
            elif after_click[j][i]==2:
                screen.blit(num2, (i*50,j*50))
            elif after_click[j][i]==3:
                screen.blit(num3, (i*50,j*50))
            elif after_click[j][i]==4:
                screen.blit(num4, (i*50,j*50))
            elif after_click[j][i]==5:
                screen.blit(num5, (i*50,j*50))
            elif after_click[j][i]==6:
                screen.blit(num6, (i*50,j*50))
            elif after_click[j][i]==7:
                screen.blit(num7, (i*50,j*50))
            elif after_click[j][i]==8:
                screen.blit(num8, (i*50,j*50))


    pygame.display.flip()
    clock.tick(TARGET_FPS)

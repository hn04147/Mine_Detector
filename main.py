import sys
import pygame
from pygame.locals import *
from image import *
import random
import tkinter
import tkinter.messagebox


TARGET_FPS=30
clock = pygame.time.Clock()
crashed = True


#global
MINE_NUM=10
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
after_click=[[0]*(col+2) for i in range(row+2)]       


#지뢰가 있으면 -1, 주변에 지뢰가 있으면 지뢰수 n, 주변에 지뢰가 없으면 0
#처음엔 0으로 초기화
before_click=[[0]*(col+2) for i in range(row+2)]

#지뢰 10개 랜덤으로 배치 0->-1
def random_mine():
    index=0
    while index < MINE_NUM:
        randomx = random.randrange(0,row)
        randomy = random.randrange(0,col)
        if before_click[randomx][randomy] == 0:
            before_click[randomx][randomy] = -1
            index = index + 1

#클릭한 칸 여는 함수
def open_blank(i, j):
    if before_click[i][j] == 0 and after_click[i][j] != -1: 
        after_click[i][j] = -1
        if i!=0: open_blank(i-1,j)
        if i!=0 and j!=col-1: open_blank(i-1,j+1)
        if j!=col-1: open_blank(i,j+1)
        if i!=row-1 and j!=col-1: open_blank(i+1,j+1)
        if i!=row-1: open_blank(i+1,j)
        if i!=row-1 and j!=0: open_blank(i+1,j-1)
        if j!=0: open_blank(i,j-1)
        if i!=0 and j!=0: open_blank(i-1,j-1)  
    elif before_click[i][j] != -1 and after_click[i][j] != -1:
        after_click[i][j] = before_click[i][j]
    elif before_click[i][j] == -1:
        after_click[i][j] = 10
        gameover()
        crashed = False

#before_click array에 수 입력
def calculate_before_click():
    for i in range (0, row):
        for j in range (0, col):
            if before_click[i][j] != -1:
                index = 0
                if i!=0:
                    if before_click[i-1][j] == -1: index = index + 1
                if i!=0 and j!=col-1:
                    if before_click[i-1][j+1] == -1: index = index + 1
                if j!=col-1:
                    if before_click[i][j+1] == -1: index = index + 1
                if i!=row-1 and j!=col-1:
                    if before_click[i+1][j+1] == -1: index = index + 1
                if i!=row-1:
                    if before_click[i+1][j] == -1: index = index + 1
                if i!=row-1 and j!=0:
                    if before_click[i+1][j-1] == -1: index = index + 1
                if j!=0:
                    if before_click[i][j-1] == -1: index = index + 1
                if i!=0 and j!=0:
                    if before_click[i-1][j-1] == -1: index = index + 1
                before_click[i][j] = index

#게임판 출력
def blit_game():
    for i in range (0,col):
        for j in range (0,row):
            if after_click[j][i]==0: screen.blit(blank,(i*50,j*50))
            elif after_click[j][i]==-1: screen.blit(blank_clicked,(i*50,j*50))
            elif after_click[j][i]==10: screen.blit(mine,(i*50,j*50))
            elif after_click[j][i]==9: screen.blit(blank_flag,(i*50,j*50))
            elif after_click[j][i]==1: screen.blit(num1, (i*50,j*50))
            elif after_click[j][i]==2: screen.blit(num2, (i*50,j*50))
            elif after_click[j][i]==3: screen.blit(num3, (i*50,j*50))
            elif after_click[j][i]==4: screen.blit(num4, (i*50,j*50))
            elif after_click[j][i]==5: screen.blit(num5, (i*50,j*50))
            elif after_click[j][i]==6: screen.blit(num6, (i*50,j*50))
            elif after_click[j][i]==7: screen.blit(num7, (i*50,j*50))
            elif after_click[j][i]==8: screen.blit(num8, (i*50,j*50))

def gameover():
    tkinter.messagebox.showinfo("GAME OVER","GAME OVER")

random_mine()
calculate_before_click()

while crashed:
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

            open_blank(x,y)
        if event.type==KEYDOWN:
            mousex, mousey = pygame.mouse.get_pos()
            print("mousex:", mousex, "mousey:", mousey)
            y = mousex//50
            x = mousey//50
            after_click[x][y]=9
            

    #이미지 출력
    blit_game()

    pygame.display.flip()
    clock.tick(TARGET_FPS)

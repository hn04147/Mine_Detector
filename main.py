import sys
import pygame
from pygame.locals import *

TARGET_FPS=30

clock = pygame.time.Clock()

WHITE=(255,255,255)

mine=pygame.image.load('mine.jpg')


pygame.init()
screen=pygame.display.set_mode((500,600), DOUBLEBUF)
pygame.display.set_caption("Mine Sweeper")

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)

    for i in range (0,10):
        for j in range (0,10):
            screen.blit(mine,(i*50,j*50+100))

    pygame.display.flip()
    clock.tick(TARGET_FPS)

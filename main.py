import sys
import pygame
from pygame.locals import *
from image import *

TARGET_FPS=30

clock = pygame.time.Clock()

WHITE=(255,255,255)
COLOUR=(211,211,211)

pygame.init()
screen=pygame.display.set_mode((500,600), DOUBLEBUF)
pygame.display.set_caption("Mine Sweeper")

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(COLOUR)

    for i in range (0,10):
        for j in range (0,10):
            screen.blit(blank,(i*50,j*50+100))
    screen.blit(mine,(250,450))
    screen.blit(blank_clicked,(150,350))
    screen.blit(blank_flag,(100,200))

    pygame.display.flip()
    clock.tick(TARGET_FPS)

#! /usr/bin/env python

import pygame
import time

def set_display(dim=(640,400)):
    return pygame.display.set_mode(dim)
    

pygame.display.init()
print(pygame.display.Info())
X=pygame.display.Info().current_w
Y=pygame.display.Info().current_h

screen = pygame.display.set_mode((X,Y),pygame.FULLSCREEN)
screen.fill((0,200,50))
pygame.display.flip()
time.sleep(2)
screen.fill((100,20,50))
image = pygame.image.load('ball.jpg')
screen.blit(image, (20,20))
pygame.display.flip()
time.sleep(2)
screen.fill((80,20,200))
screen.blit(pygame.transform.scale(image, (500,500)), (50,50))
box1 = pygame.Surface((int(X/3),int(Y/10)))
box1.fill((255,255,0))
box2 = pygame.Surface((int(X/3),int(Y/10)))
box2.fill((255,0,0))
box3 = pygame.Surface((int(X/3),int(Y/10)))
box3.fill((0,255,0))
screen.blit(box1, (int(X/3),Y-int(Y/10)))
screen.blit(box2, (0,Y-int(Y/10)))
screen.blit(box3, (int(2*X/3),Y-int(Y/10)))
pygame.display.flip()
time.sleep(2)



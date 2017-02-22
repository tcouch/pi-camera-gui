#! /usr/bin/env python

import pygame
#from picamera import PiCamera
from time import sleep
import sys
#from gpiozero import Button

#Setup buttons
#BlueButton = Button(4, pull_up=False)
#RedButton = Button(?, pull_up=False)
#YellowButton = Button(?, pull_up=False)

#Setup pygame screen
pygame.display.init()
pygame.font.init()
print(pygame.display.Info())
X=pygame.display.Info().current_w
Y=pygame.display.Info().current_h
screen = pygame.display.set_mode((X,Y),pygame.FULLSCREEN)

#Other variables
black = (0,0,0)
white = (255,255,255)
ready_bg = (15,80,180)
countdown_bg = (180,80,15)
decide_bg = (15,180,80)
discard_bg = (255,0,0)
saved_bg = (0,255,0)
font1 = 'resources/Quicksand-Regular.otf'

def set_display(dim=(640,400)):
    return pygame.display.set_mode(dim)
    
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def display_ready_screen():
    screen.fill(ready_bg)
    largeText = pygame.font.Font(font1,115)
    text = "READY"
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((X/2),(Y/2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    pressed = wait_for_input()
    if pressed == pygame.K_ESCAPE: sys.exit()
    else: display_count_down()

def wait_for_input():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.key

def display_count_down():
    largeText = pygame.font.Font(font1,115)
    for i in range(5,1,-1):
        screen.fill(countdown_bg)
        text = str(i)
    	TextSurf, TextRect = text_objects(text, largeText)
    	TextRect.center = ((X/2),(Y/2))
    	screen.blit(TextSurf, TextRect)
    	pygame.display.update()
        sleep(1)
    screen.fill(countdown_bg)
    text = "1"
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((X/2),(Y/2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    sleep(0.5)
    take_photo()

def take_photo():
    print("Pretend this takes a photo")
    decide()

def discard_image():
    screen.fill(discard_bg)
    largeText = pygame.font.Font(font1,115)
    text = "IMAGE DISCARDED"
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((X/2),(Y/2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    sleep(2)
    display_ready_screen()

def save_image():
    screen.fill(saved_bg)
    largeText = pygame.font.Font(font1,115)
    text = "IMAGE SAVED"
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((X/2),(Y/2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    sleep(2)
    display_ready_screen()

def decide():
    screen.fill(decide_bg)
    box1 = pygame.Surface((int(X/3),int(Y/10)))
    box1.fill((255,255,0))
    box2 = pygame.Surface((int(X/3),int(Y/10)))
    box2.fill((255,0,0))
    box3 = pygame.Surface((int(X/3),int(Y/10)))
    box3.fill((0,255,0))
    image = pygame.image.load('resources/tom1.jpg')
    ix,iy = image.get_size()
    scale_factor = X/float(ix)
    screen.blit(pygame.transform.scale(image, (X,int(scale_factor*iy))), (0,0))
    screen.blit(box1, (int(X/3),Y-int(Y/10)))
    screen.blit(box2, (0,Y-int(Y/10)))
    screen.blit(box3, (int(2*X/3),Y-int(Y/10)))
    pygame.display.update()
    pressed = wait_for_input()
    if pressed == pygame.K_LEFT:
        discard_image()
    elif pressed == pygame.K_RIGHT:
        save_image()
    else: sys.exit()

    

display_ready_screen()

#screen.fill((0,200,50))
#pygame.display.flip()
#sleep(2)
#screen.fill((100,20,50))
#image = pygame.image.load('ball.jpg')
#screen.blit(image, (20,20))
#pygame.display.flip()
#sleep(2)
#screen.fill((80,20,200))
#screen.blit(pygame.transform.scale(image, (500,500)), (50,50))
#box1 = pygame.Surface((int(X/3),int(Y/10)))
#box1.fill((255,255,0))
#box2 = pygame.Surface((int(X/3),int(Y/10)))
#box2.fill((255,0,0))
#box3 = pygame.Surface((int(X/3),int(Y/10)))
#box3.fill((0,255,0))
#screen.blit(box1, (int(X/3),Y-int(Y/10)))
#screen.blit(box2, (0,Y-int(Y/10)))
#screen.blit(box3, (int(2*X/3),Y-int(Y/10)))
#pygame.display.flip()
#sleep(2)



#! /usr/bin/env python

import pygame
from picamera import PiCamera
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
#Setup camera
camera = PiCamera()
camera.rotation = 270
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
    wait_for_touch()
    display_count_down()

def wait_for_input():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.key

def wait_for_touch():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                return pygame.mouse.get_pos()


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
    camera.start_preview()
    sleep(2)
    camera.capture('images/tom.jpg')
    camera.stop_preview()
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

class button(object):
    def __init__(self,**kwargs):
        self.name = kwargs["name"]
        self.dimensions = kwargs["dimensions"]
        self.x1 = kwargs["x1"]
        self.y1 = kwargs["y1"]
        self.x2 = self.x1 + self.dimensions[0]
        self.y2 = self.y1 + self.dimensions[1]
        self.function = kwargs["function"]
        self.colour = kwargs["colour"]
        self.surface = self.create_surface()

    def create_surface(self):
        surface = pygame.Surface(self.dimensions)
        surface.fill(self.colour)
        return surface

    def touched(self,touch_pos):
        if self.x1 <= touch_pos[0] <= self.x2:
            if self.y1 <= touch_pos[1] <= self.y2:
                return True
        else: return False

    def show(self):
        screen.blit(self.surface, (self.x1,self.y1))

def decide():
    screen.fill(decide_bg)
    image = pygame.image.load('images/tom.jpg')
    ix,iy = image.get_size()
    scale_factor = X/float(ix)
    screen.blit(pygame.transform.scale(image, (X,int(scale_factor*iy))), (0,0))
    buttons = {
        "accept": button(**accept_button_config),
        "reject": button(**reject_button_config),
        "exit": button(**exit_button_config)
        }
    for k,v in buttons.items(): v.show()
    pygame.display.update()
    while True:
        touch_pos = wait_for_touch()
        for k,v in buttons.items():
            if v.touched(touch_pos):
                v.function()

#Button settings
reject_button_config = {
    "name": "reject",
    "dimensions": (int(X/3),int(Y/10)),
    "x1": 0,
    "y1": Y-int(Y/10),
    "colour": (255,0,0),
    "function": discard_image
    }

accept_button_config = {
    "name": "accept",
    "dimensions": (int(X/3),int(Y/10)),
    "x1": int(2*X/3),
    "y1": Y-int(Y/10),
    "colour": (0,255,0),
    "function": save_image
    }

exit_button_config = {
    "name": "exit",
    "dimensions": (int(Y/10),int(Y/10)),
    "x1": 0,
    "y1": 0,
    "colour": (255,255,255),
    "function": sys.exit
    }
    

display_ready_screen()

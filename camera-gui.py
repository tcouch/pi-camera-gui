#! /usr/bin/env python

import pygame
from picamera import PiCamera
from time import sleep
import sys
from io import BytesIO
from datetime import datetime as dt
#from gpiozero import Button

#Setup buttons
#BlueButton = Button(4, pull_up=False)
#RedButton = Button(?, pull_up=False)
#YellowButton = Button(?, pull_up=False)

#Setup pygame screen
pygame.display.init()
pygame.font.init()
#pygame.mouse.set_visible(False)
print(pygame.display.Info())
X=pygame.display.Info().current_w
Y=pygame.display.Info().current_h
screen = pygame.display.set_mode((X,Y),pygame.FULLSCREEN)
#Setup camera
camera = PiCamera()
camera.rotation = 270
camera.resolution = (3280,2464)
#Other variables
black = (0,0,0)
white = (0,0,0)
red = (255,0,0)
ready_bg = (15,80,180)
countdown_bg = (0,0,0)
#countdown_bg = (180,80,15)
decide_bg = (15,180,80)
discard_bg = (255,0,0)
saved_bg = (0,255,0)
font1 = 'resources/Quicksand-Regular.otf'



def set_display(dim=(640,400)):
    return pygame.display.set_mode(dim)
    
def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def display_ready_screen():
    screen.fill(ready_bg)
    largeText = pygame.font.Font(font1,115)
    text = "READY"
    TextSurf, TextRect = text_objects(text, largeText, black)
    TextRect.center = ((X/2),(Y/2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    wait_for_touch()
    take_photo()

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


def take_photo():
    img_stream = BytesIO()
    largeText = pygame.font.Font(font1,115)
    camera.start_preview()
    camera.preview.alpha = 128
    for i in range(3,0,-1):
        screen.fill(countdown_bg)
        text = str(i)
        TextSurf, TextRect = text_objects(text, largeText, red)
        TextRect.center = ((X/2),(Y/2))
    	screen.blit(TextSurf, TextRect)
        pygame.display.update()
        sleep(1)
    camera.capture(img_stream,'jpeg')
    camera.stop_preview()
    decide(img_stream)

def discard_image(image):
    screen.fill(discard_bg)
    largeText = pygame.font.Font(font1,115)
    text = "IMAGE DISCARDED"
    TextSurf, TextRect = text_objects(text, largeText, black)
    TextRect.center = ((X/2),(Y/2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    sleep(2)
    display_ready_screen()

def save_image(image):
    filename = "images/" + dt.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
    pygame.image.save(image, filename)
    screen.fill(saved_bg)
    largeText = pygame.font.Font(font1,115)
    text = "IMAGE SAVED"
    TextSurf, TextRect = text_objects(text, largeText, black)
    TextRect.center = ((X/2),(Y/2))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    sleep(2)
    display_ready_screen()

def exit_gui(image):
    sys.exit()

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

def decide(img_stream):
    screen.fill(decide_bg)
    img_stream.seek(0)
    image = pygame.image.load(img_stream)
    ix,iy = image.get_size()
    scale_factor = Y/float(iy)
    jx = int(scale_factor*ix)
    jy = int(scale_factor*iy)
    xoffset = int((X-jx)/2)
    buttons = {
        "accept": button(**accept_button_config),
        "reject": button(**reject_button_config)
        }
    for k,v in buttons.items(): v.show()
    stop = button(**exit_button_config)
    stop.show()   
    screen.blit(pygame.transform.scale(image, (jx,jy)), (xoffset,0))
    pygame.display.update()
    while True:
        touch_pos = wait_for_touch()
        for k,v in buttons.items():
            if v.touched(touch_pos):
                v.function(image)

#Button settings
reject_button_config = {
    "name": "reject",
    "dimensions": (int(X/8),Y),
    "x1": 0,
    "y1": 0,
    "colour": (255,0,0),
    "function": discard_image,
    "text": "Discard"
    }

accept_button_config = {
    "name": "accept",
    "dimensions": (int(X/8),Y),
    "x1": int(7*X/8),
    "y1": 0,
    "colour": (0,255,0),
    "function": save_image,
    "text": "Keep"
    }

exit_button_config = {
    "name": "exit",
    "dimensions": (int(Y/10),int(Y/10)),
    "x1": 0,
    "y1": 0,
    "colour": (255,255,255),
    "function": exit_gui
    }
    

display_ready_screen()

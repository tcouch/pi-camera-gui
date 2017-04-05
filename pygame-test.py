#! /usr/bin/env python

import pygame
import pygame.freetype
from time import sleep
import sys
from io import BytesIO
from datetime import datetime as dt

#Setup pygame screen
pygame.display.init()
pygame.freetype.init()
#pygame.mouse.set_visible(False)
print(pygame.display.Info())
X=800
Y=480
#X=pygame.display.Info().current_w
#Y=pygame.display.Info().current_h
screen = pygame.display.set_mode((X,Y))
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
font1 = 'Quicksand-Regular.otf'

def text_objects(text, font, colour):
    textSurface = font.render(text, colour)
    return textSurface

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

def exit_gui(image):
    sys.exit()
    
def save_image(image):
    print("Image saved")
    decide()

def discard_image(image):
    print("Image discarded")
    decide()

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
        if "text" in kwargs:
            self.text = kwargs["text"]
            self.dotext = True
            self.txtSurf,self.txtRect = self.add_text()
        else: self.dotext = False
        if "image" in kwargs:
            self.imagefile = kwargs["image"]
            self.add_image()
        
    def create_surface(self):
        surface = pygame.Surface(self.dimensions)
        surface.fill(self.colour)
        return surface
    
    def add_text(self):
        print("Adding text: {0}".format(self.text))
        smallFont = pygame.freetype.Font(font1,50)
        smallFont.vertical = True
        accross = self.x1 + self.dimensions[0]/2
        down = self.y1 + self.dimensions[1]/2
        txtSurf, txtRect = smallFont.render(self.text)
        txtRect.center = (accross,down)
        return txtSurf, txtRect
        
    def add_image(self):
        img = pygame.image.load(self.imagefile)
        self.surface.blit(pygame.transform.scale(img,(50,50)),(40,200))
        return 0
    
    def touched(self,touch_pos):
        if self.x1 <= touch_pos[0] <= self.x2:
            if self.y1 <= touch_pos[1] <= self.y2:
                return True
        else: return False

    def show(self):
        screen.blit(self.surface, (self.x1,self.y1))
        if self.dotext: screen.blit(self.txtSurf, self.txtRect)

def decide():
    screen.fill(decide_bg)
    image = pygame.image.load('pi-cam-v2-test.jpg')
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
    "text": "DISCARD"
    }

accept_button_config = {
    "name": "accept",
    "dimensions": (int(X/8),Y),
    "x1": int(7*X/8),
    "y1": 0,
    "colour": (0,255,0),
    "function": save_image,
    "image": "good.png"
    }

exit_button_config = {
    "name": "exit",
    "dimensions": (int(Y/10),int(Y/10)),
    "x1": 0,
    "y1": 0,
    "colour": (255,255,255),
    "function": exit_gui
    }
    

decide()

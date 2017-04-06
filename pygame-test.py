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
margin = 20
#X=pygame.display.Info().current_w
#Y=pygame.display.Info().current_h
#camera.resolution = (3280,2464)
photo_resolution = (3280,2464)
photo_display_height = Y - 2*margin
photo_scale_factor = photo_display_height / photo_resolution[1] 
photo_display_width = int(photo_resolution[0] * photo_scale_factor)
photo_display_dims = (photo_display_width,photo_display_height)

screen = pygame.display.set_mode((X,Y))
#Other variables
black = (0,0,0)
white = (0,0,0)
red = (255,0,0)
ready_bg = (15,80,180)
countdown_bg = (0,0,0)
#countdown_bg = (180,80,15)
#decide_bg = (43,87,151)
decide_bg = (0,0,0)
discard_bg = (218,83,44)
saved_bg = (0,163,0)
font1 = 'resources/Quicksand-Regular.otf'

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
        self.width = kwargs["width"]
        self.height = kwargs["height"]
        self.dimensions = (self.width,self.height)
        self.x1 = kwargs["x1"]
        self.y1 = kwargs["y1"]
        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height
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
        accross = self.x1 + self.width/2
        down = self.y1 + self.height/2
        txtSurf, txtRect = smallFont.render(self.text)
        txtRect.center = (accross,down)
        return txtSurf, txtRect
        
    def add_image(self):
        img = pygame.image.load(self.imagefile)
        img_dimensions = (int(3/4*self.width),int(3/4*self.width))
        img_x = self.width/2 - img_dimensions[0]/2
        img_y = self.height/2 - img_dimensions[1]/2
        self.surface.blit(pygame.transform.scale(img,img_dimensions),(img_x,img_y))
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
    image = pygame.image.load('resources/pi-cam-v2-test.jpg')
    buttons = {
        "accept": button(**accept_button_config),
        "reject": button(**reject_button_config),
        "exit": button(**exit_button_config)
        }
    for k,v in buttons.items(): v.show()
    screen.blit(pygame.transform.scale(image, photo_display_dims), (margin,margin))
    pygame.display.update()
    while True:
        touch_pos = wait_for_touch()
        for k,v in buttons.items():
            if v.touched(touch_pos):
                v.function(image)

#Button settings
reject_button_config = {
    "name": "reject",
    "width": int(X - photo_display_width - 3 * margin),
    "height": int(X - photo_display_width - 3 * margin),
#    "height": int(Y/2 - 1.5*margin),
    "x1": photo_display_width + 2 * margin,
    "y1": int(X - photo_display_width - margin),
#    "y1": Y/2 + margin/2,
    "colour": discard_bg,
    "function": discard_image,
    "image": "resources/delete.png"
    }

accept_button_config = {
    "name": "accept",
    "width": int(X - photo_display_width - 3 * margin),
    "height": int(X - photo_display_width - 3 * margin),
#    "height": int(Y/2 - 1.5*margin),
    "x1": photo_display_width + 2 * margin,
    "y1": margin,
    "colour": saved_bg,
    "function": save_image,
    "image": "resources/like.png"
    }

exit_button_config = {
    "name": "exit",
    "width": int((X - photo_display_width - 3 * margin)/2),
    "height": int((X - photo_display_width - 3 * margin)/2),
    "x1": photo_display_width + 2 * margin,
    "y1": int(2*(X - photo_display_width - 1.5 * margin)),
    "colour": (255,255,255),
    "function": exit_gui,
    "image": "resources/close.png"
    }
    

decide()

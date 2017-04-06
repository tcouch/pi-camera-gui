#! /usr/bin/env python3

import pygame
import pygame.freetype
from picamera import PiCamera
from time import sleep
import sys
from io import BytesIO
from datetime import datetime as dt

#Setup pygame screen
pygame.display.init()
pygame.freetype.init()
#pygame.mouse.set_visible(False)
print(pygame.display.Info())
X=pygame.display.Info().current_w
Y=pygame.display.Info().current_h
screen = pygame.display.set_mode((X,Y),pygame.FULLSCREEN)
margin = 20
photo_resolution = (3280,2464)
photo_display_height = Y - 2*margin
photo_scale_factor = photo_display_height / photo_resolution[1] 
photo_display_width = int(photo_resolution[0] * photo_scale_factor)
photo_display_dims = (photo_display_width,photo_display_height)

#Setup camera
camera = PiCamera()
camera.rotation = 270
camera.resolution = photo_resolution
#Other variables
black = (0,0,0)
white = (0,0,0)
red = (255,0,0)
ready_bg = (15,80,180)
countdown_bg = (0,0,0)
#countdown_bg = (180,80,15)
#decide_bg = (43,87,151)
decide_bg = (0,0,0)
delete_bg = (218,83,44)
save_bg = (0,163,0)
font1 = 'resources/Quicksand-Regular.otf'



def set_display(dim=(640,400)):
    return pygame.display.set_mode(dim)
    
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
    largeText = pygame.freetype.Font(font1,115)
    camera.start_preview()
    camera.preview.alpha = 128
    for i in range(3,0,-1):
        screen.fill(countdown_bg)
        text = str(i)
        txtSurf, txtRect = largeText.render(text, red)
        txtRect.center = ((X/2),(Y/2))
        screen.blit(txtSurf, txtRect)
        pygame.display.update()
        sleep(1)
    camera.capture(img_stream,'jpeg')
    camera.stop_preview()
    decide(img_stream)

def exit_gui(image):
    sys.exit()

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
        if "alpha" in kwargs:
            self.alpha = kwargs["alpha"]
        else:
            self.alpha = 220
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
        surface.set_alpha(self.alpha)
        return surface
    
    def add_text(self):
        print("Adding text: {0}".format(self.text))
        smallFont = pygame.freetype.Font(font1,50)
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

def ready():
    bgPattern = pygame.image.load('resources/bg-pattern.jpg')
    screen.blit(pygame.transform.scale(bgPattern, (X,Y)), (0,0))
    capture = button(**capture_button_config)
    capture.show()
    capture_msg = button(**capture_msg_config)
    capture_msg.show()
    pygame.display.update()
    while True:
        touch_pos = wait_for_touch()
        if capture.touched(touch_pos):
            capture.function()

def decide(img_stream):
    #screen.fill(decide_bg)
    img_stream.seek(0)
    image = pygame.image.load(img_stream)
    bgPattern = pygame.image.load('resources/bg-pattern.jpg')
    buttons = {
        "accept": button(**accept_button_config),
        "reject": button(**reject_button_config),
        "exit": button(**exit_button_config)
        }
    screen.blit(pygame.transform.scale(bgPattern, (X,Y)), (0,0))
    screen.blit(pygame.transform.scale(image, photo_display_dims), (margin,margin))
    for k,v in buttons.items(): v.show()
    pygame.display.update()
    while True:
        touch_pos = wait_for_touch()
        for k,v in buttons.items():
            if v.touched(touch_pos):
                v.function(image)
                
def save_image(image):
    filename = "images/" + dt.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
    pygame.image.save(image, filename)
    bgPattern = pygame.image.load('resources/bg-pattern.jpg')
    screen.blit(pygame.transform.scale(bgPattern, (X,Y)), (0,0))
    message = button(**save_msg_config)
    message.show()
    pygame.display.update()
    sleep(2)
    ready()

def discard_image(image):
    bgPattern = pygame.image.load('resources/bg-pattern.jpg')
    screen.blit(pygame.transform.scale(bgPattern, (X,Y)), (0,0))
    message = button(**del_msg_config)
    message.show()
    pygame.display.update()
    sleep(2)
    ready()

#Button settings

capture_button_config = {
    "name": "go",
    "width": int(X/8),
    "height": int(X/8),
    "x1": int(X/2 - X/16),
    "y1": int(Y/2 + X/16),
    "colour": ready_bg,
    "function": take_photo,
    "image": "resources/camera.png"
    }
    
capture_msg_config = {
    "name": "ready",
    "width": int(3*X/4),
    "height": int(Y/4),
    "x1": int(X/2 - 3*X/8),
    "y1": int(Y/4),
    "colour": ready_bg,
    "function": None,
    "text": "Take a photo!"
}    

reject_button_config = {
    "name": "reject",
    "width": int(X - photo_display_width - 3 * margin),
    "height": int(X - photo_display_width - 3 * margin),
    "x1": photo_display_width + 2 * margin,
    "y1": int(X - photo_display_width - margin),
    "colour": delete_bg,
    "function": discard_image,
    "image": "resources/delete.png"
    }

accept_button_config = {
    "name": "accept",
    "width": int(X - photo_display_width - 3 * margin),
    "height": int(X - photo_display_width - 3 * margin),
    "x1": photo_display_width + 2 * margin,
    "y1": margin,
    "colour": save_bg,
    "function": save_image,
    "image": "resources/like.png"
    }

save_msg_config = {
    "name": "saved",
    "width": int(3*X/4),
    "height": int(Y/4),
    "x1": int(X/2 - 3*X/8),
    "y1": int(Y/2 - Y/8),
    "colour": save_bg,
    "function": None,
    "text": "The image is saved"
    }
    
del_msg_config = {
    "name": "deleted",
    "width": int(3*X/4),
    "height": int(Y/4),
    "x1": int(X/2 - 3*X/8),
    "y1": int(Y/2 - Y/8),
    "colour": delete_bg,
    "function": None,
    "text": "The image is gone"
    }

exit_button_config = {
    "name": "exit",
    "width": int((X - photo_display_width - 3 * margin)/2),
    "height": int((X - photo_display_width - 3 * margin)/2),
    "x1": photo_display_width + 2 * margin,
    "y1": int(2*(X - photo_display_width - 1.5 * margin)),
    "colour": (255,255,255),
    "function": exit_gui,
    "image": "resources/close.png",
    "alpha": None
    }
    

ready()

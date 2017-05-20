#! /usr/bin/env python3

import sys
import os
import pygame
import pygame.freetype
from picamera import PiCamera
from time import sleep
from io import BytesIO
from datetime import datetime as dt

# Constants
COUNTDOWN = 5
CAMERA_ROTATION = 270
PHOTO_RESOLUTION = (3280, 2464)
MARGIN = 20
FONT1 = '/home/pi/pi-camera-gui/resources/Quicksand-Regular.otf'
BG_PATTERN = '/home/pi/pi-camera-gui/resources/bg-pattern.jpg'
BLACK = (0, 0, 0)
WHITE = (0, 0, 0)
RED = (255, 0, 0)
READY_BG = (15, 80, 180)
COUNTDOWN_BG = (0, 0, 0)
DECIDE_BG = (0, 0, 0)
DELETE_BG = (218, 83, 44)
SAVE_BG = (0, 163, 0)
DEFAULT_BUTTON_ALPHA = 220
X = 800
Y = 480

btn_dim = X - 585 - 3 * MARGIN

class Controller:
    def __init__(self, mode="normal"):
        self.mode = mode
        self.model = Model(mode=self.mode)
        self.view = View(self.model)

    def go(self):
        encore = True
        while encore:
            self.view.show_ready_screen()
            self.model.wait_for_touch()
            self.model.camera.start_preview()
            self.model.camera.preview.alpha = 128
            self.view.show_countdown()
            self.model.take_photo()
            self.model.camera.stop_preview()
            self.view.show_decision_screen()
            response = self.get_decision()
            if response == "save":
                self.model.save_image(self.view.photo)
                self.view.show_saved_screen()
            elif response == "discard":
                self.model.discard_image()
                self.view.show_discard_screen()
            elif response == "exit":
                encore = False
            sleep(1)

    def get_decision(self):
        decided = False
        while not decided:
            touch = self.model.wait_for_touch()
            for button in self.model.choice_buttons:
                if button.touched(touch):
                    response = button.response
                    decided = True
        return response

class Model:
    def __init__(self, mode):
        self.setup_camera()
        self.choice_buttons = [
          Button(**accept_button_config),
          Button(**reject_button_config)
        ]
        if mode == "test":
            self.choice_buttons.append(Button(**exit_button_config))

    def setup_camera(self):
        self.camera = PiCamera()
        self.camera.rotation = CAMERA_ROTATION
        self.camera.resolution = PHOTO_RESOLUTION

    def take_photo(self):
        img_stream = BytesIO()
        self.camera.capture(img_stream, 'jpeg')
        self.image = img_stream
        self.image.seek(0)

    def wait_for_touch(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    return pygame.mouse.get_pos()

    def save_image(self, image):
        filename = "/home/pi/pi-camera-gui/images/" + dt.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
        pygame.image.save(image, filename)
        return 0

    def discard_image(self):
        pass

        
class View:
    def __init__(self,model):
        self.model = model
        self.setup_display()
        self.photo_display_size = self.get_photo_display_size()
        self.background = pygame.image.load(BG_PATTERN)
        
    def setup_display(self):
        pygame.display.init()
        pygame.freetype.init()
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.screen_size = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_size,
                                              pygame.FULLSCREEN)
        self.hide_cursor()

    def hide_cursor(self):
        # Make cursor transparent
        pygame.mouse.set_cursor((8, 8), (0, 0),
                                (0, 0, 0, 0, 0, 0, 0, 0),
                                (0, 0, 0, 0, 0, 0, 0, 0))

    def get_photo_display_size(self):
        # Photo is full screen height minus margin top and bottom
        photo_display_height = self.screen_height - 2 * MARGIN
        # Calculate desired display width to preserve aspect ratio
        photo_resolution = self.model.camera.resolution
        photo_scale_factor = photo_display_height / photo_resolution[1]
        photo_display_width = int(photo_resolution[0] * photo_scale_factor)
        print(photo_display_width, photo_display_height)
        return photo_display_width, photo_display_height

    def reset_background(self):
        scaled_background = pygame.transform.scale(self.background, self.screen_size)
        self.screen.blit(scaled_background, (0, 0))

    def show_decision_screen(self):
        self.reset_background()
        self.photo = pygame.image.load(self.model.image)
        scaled_photo = pygame.transform.scale(self.photo, self.photo_display_size)
        photo_position = (MARGIN, MARGIN)
        self.screen.blit(scaled_photo, photo_position)
        buttons = self.model.choice_buttons
        for button in buttons:
            button.show(self.screen)
        pygame.display.update()

    def show_ready_screen(self):
        self.reset_background()
        Button(**ready_button_config).show(self.screen)
        Button(**ready_msg_config).show(self.screen)
        pygame.display.update()

    def show_saved_screen(self):
        self.reset_background()
        Button(**save_msg_config).show(self.screen)
        pygame.display.update()

    def show_discard_screen(self):
        self.reset_background()
        Button(**del_msg_config).show(self.screen)
        pygame.display.update()

    def show_countdown(self):
        large_text = pygame.freetype.Font(FONT1, 115)
        for i in range(COUNTDOWN, 0, -1):
            self.screen.fill(COUNTDOWN_BG)
            self.screen.set_alpha(0)
            text = str(i)
            txt_surf, txt_rect = large_text.render(text, RED)
            txt_rect.center = ((X/2), (Y/2))
            self.screen.blit(txt_surf, txt_rect)
            pygame.display.update()
            sleep(1)
        self.screen.fill(COUNTDOWN_BG)
        pygame.display.update()


class Button(object):
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.width = kwargs["width"]
        self.height = kwargs["height"]
        self.size = (self.width, self.height)
        self.x1 = kwargs["x1"]
        self.y1 = kwargs["y1"]
        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height
        self.response = kwargs["response"]
        self.colour = kwargs["colour"]
        if "alpha" in kwargs:
            self.alpha = kwargs["alpha"]
        else:
            self.alpha = DEFAULT_BUTTON_ALPHA
        self.surface = self.create_surface()
        if "text" in kwargs:
            self.text = kwargs["text"]
            self.dotext = True
            self.txt_surf, self.txt_rect = self.add_text()
        else:
            self.dotext = False
        if "image" in kwargs:
            self.imagefile = kwargs["image"]
            self.add_image()

    def create_surface(self):
        surface = pygame.Surface(self.size)
        surface.fill(self.colour)
        surface.set_alpha(self.alpha)
        return surface

    def add_text(self):
        small_font = pygame.freetype.Font(FONT1, 50)
        txt_surf, txt_rect = small_font.render(self.text)
        txt_x = self.x1 + self.width/2
        txt_y = self.y1 + self.height/2
        txt_rect.center = (txt_x, txt_y)
        return txt_surf, txt_rect

    def add_image(self):
        img = pygame.image.load(self.imagefile)
        img_size = tuple((int(3/4*dim) for dim in self.size))
        ix, iy = (a/2 - b/2 for a, b in zip(self.size, img_size))
        self.surface.blit(pygame.transform.scale(img, img_size),
                          (ix, iy))
        return 0

    def touched(self, touch_pos):
        if self.x1 <= touch_pos[0] <= self.x2:
            if self.y1 <= touch_pos[1] <= self.y2:
                return True
        else:
            return False

    def show(self, screen):
        screen.blit(self.surface, (self.x1, self.y1))
        if self.dotext:
            screen.blit(self.txt_surf, self.txt_rect)


# Button settings

ready_button_config = {
    "name": "go",
    "width": int(X/8),
    "height": int(X/8),
    "x1": int(X/2 - X/16),
    "y1": int(Y/2 + X/16),
    "colour": READY_BG,
    "response": None,
    "image": "/home/pi/pi-camera-gui/resources/camera.png"
    }

ready_msg_config = {
    "name": "ready",
    "width": int(3*X/4),
    "height": int(Y/4),
    "x1": int(X/2 - 3*X/8),
    "y1": int(Y/4),
    "colour": READY_BG,
    "text": "Tap to take a photo!",
    "response": None
}

reject_button_config = {
    "name": "reject",
    "width": btn_dim,
    "height": btn_dim,
    "x1": 585 + 2 * MARGIN,
    "y1": btn_dim + 2 * MARGIN,
    "colour": DELETE_BG,
    "response": "discard",
    "image": "/home/pi/pi-camera-gui/resources/delete.png"
    }

accept_button_config = {
    "name": "accept",
    "width": btn_dim,
    "height": btn_dim,
    "x1": 585 + 2 * MARGIN,
    "y1": MARGIN,
    "colour": SAVE_BG,
    "response": "save",
    "image": "/home/pi/pi-camera-gui/resources/like.png"
    }

save_msg_config = {
    "name": "saved",
    "width": int(3*X/4),
    "height": int(Y/4),
    "x1": int(X/2 - 3*X/8),
    "y1": int(Y/2 - Y/8),
    "colour": SAVE_BG,
    "response": None,
    "text": "Image saved"
    }

del_msg_config = {
    "name": "deleted",
    "width": int(3*X/4),
    "height": int(Y/4),
    "x1": int(X/2 - 3*X/8),
    "y1": int(Y/2 - Y/8),
    "colour": DELETE_BG,
    "response": None,
    "text": "Image deleted"
    }

exit_button_config = {
    "name": "exit",
    "width": 20,
    "height": 20,
    "x1": 0,
    "y1": 0,
    "colour": (255, 255, 255),
    "response": "exit",
    "image": "/home/pi/pi-camera-gui/resources/close.png",
    "alpha": None
    }


if __name__=="__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            C = Controller(mode="test")
            C.go()
    else:
        C = Controller()
        C.go()

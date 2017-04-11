#! /usr/bin/env python3

import sys
import pygame
import pygame.freetype
from picamera import PiCamera
from time import sleep
from io import BytesIO
from datetime import datetime as dt

# Constants
CAMERA_ROTATION = 270
PHOTO_RESOLUTION = (3280, 2464)
MARGIN = 20
FONT1 = 'resources/Quicksand-Regular.otf'
BG_PATTERN = 'resources/bg-pattern.jpg'
BLACK = (0, 0, 0)
WHITE = (0, 0, 0)
RED = (255, 0, 0)
READY_BG = (15, 80, 180)
COUNTDOWN_BG = (0, 0, 0)
DECIDE_BG = (0, 0, 0)
DELETE_BG = (218, 83, 44)
SAVE_BG = (0, 163, 0)
DEFAULT_BUTTON_ALPHA = 220


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self.model)

    def go(self):
        self.view.show_ready_screen()
        self.model.wait_for_touch()
        self.model.camera.start_preview()
        self.view.show_countdown()
        self.model.take_photo()
        self.model.camera.stop_preview()
        self.view.show_decision_screen()
        sleep(5)
        sys.exit()
        

class Model:
    def __init__(self):
        self.setup_camera()
        self.choice_buttons = {
        "accept": Button(**accept_button_config),
        "reject": Button(**reject_button_config),
        "exit": Button(**exit_button_config)
        }

    def setup_camera(self):
        self.camera = PiCamera()
        self.camera.rotation = CAMERA_ROTATION
        self.camera.resolution = PHOTO_RESOLUTION
        self.camera.preview.alpha = 128

    def take_photo(self):
        img_stream = BytesIO()
        self.camera.capture(img_stream, 'jpeg')
        self.image = img_stream

    def get_image(self):
        self.image.seek(0)
        return self.image

    def wait_for_touch(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    return pygame.mouse.get_pos()

        
class View:
    def __init__(self,model):
        self.model = model
        self.setup_display()
        self.photo_display_size = get_photo_display_size()
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
        return photo_display_width, photo_display_height

    def reset_background(self):
        scaled_background = pygame.transform.scale(self.background, self.screen_size)
        self.screen.blit(scaled_background, (0, 0))

    def show_decision_screen(self):
        self.reset_background()
        photo = pygame.image.load(self.model.get_image())        
        scaled_photo = pygame.transform.scale(photo, self.photo_display_size)
        photo_position = (MARGIN, MARGIN)
        self.screen.blit(scaled_photo, photo_position)
        buttons = self.model.choice_buttons
        for k, v in buttons.items():
            v.show()
        pygame.display.update()

    def show_ready_screen(self):
        self.reset_background()
        Button(**ready_button_config).show()
        Button(**ready_msg_config).show()
        pygame.display.update()

    def show_saved_screen(self):
        self.reset_background()
        Button(**save_msg_config).show()
        pygame.display.update()

    def show_discard_screen(self):
        self.reset_background()
        Button(**del_msg_config).show()
        pygame.display.update()

    def show_countdown(self):
        large_text = pygame.freetype.Font(FONT1, 115)
        for i in range(3, 0, -1):
            self.screen.fill(COUNTDOWN_BG)
            self.screen.set_alpha(0)
            text = str(i)
            txt_surf, txt_rect = large_text.render(text, RED)
            txt_rect.center = ((X/2), (Y/2))
            self.screen.blit(txt_surf, txt_rect)
            pygame.display.update()
            sleep(1)


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
        self.function = kwargs["function"]
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

    def show(self):
        screen.blit(self.surface, (self.x1, self.y1))
        if self.dotext:
            screen.blit(self.txt_surf, self.txt_rect)


def wait_for_touch():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                return pygame.mouse.get_pos()


def take_photo():
    img_stream = BytesIO()
    large_text = pygame.freetype.Font(FONT1, 115)
    camera.start_preview()
    camera.preview.alpha = 128
    for i in range(3, 0, -1):
        screen.fill(COUNTDOWN_BG)
        screen.set_alpha(0)
        text = str(i)
        txt_surf, txt_rect = large_text.render(text, RED)
        txt_rect.center = ((X/2), (Y/2))
        screen.blit(txt_surf, txt_rect)
        pygame.display.update()
        sleep(1)
    camera.capture(img_stream, 'jpeg')
    camera.stop_preview()
    decide(img_stream)


def ready():
    background = pygame.image.load(BG_PATTERN)
    screen.blit(pygame.transform.scale(background, (X, Y)), (0, 0))
    capture = Button(**ready_button_config)
    capture.show()
    capture_msg = Button(**ready_msg_config)
    capture_msg.show()
    pygame.display.update()
    while True:
        touch_pos = wait_for_touch()
        if capture.touched(touch_pos):
            capture.function()


def decide(img_stream):
    img_stream.seek(0)
    image = pygame.image.load(img_stream)
    background = pygame.image.load(BG_PATTERN)
    buttons = {
        "accept": Button(**accept_button_config),
        "reject": Button(**reject_button_config),
        "exit": Button(**exit_button_config)
        }
    screen.blit(pygame.transform.scale(background, (X, Y)), (0, 0))
    screen.blit(pygame.transform.scale(image, photo_display_dims),
                (MARGIN, MARGIN))
    for k, v in buttons.items():
        v.show()
    pygame.display.update()
    while True:
        touch_pos = wait_for_touch()
        for k, v in buttons.items():
            if v.touched(touch_pos):
                v.function(image)


def save_image(image):
    filename = "images/" + dt.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
    pygame.image.save(image, filename)
    background = pygame.image.load(BG_PATTERN)
    screen.blit(pygame.transform.scale(background, (X, Y)), (0, 0))
    message = Button(**save_msg_config)
    message.show()
    pygame.display.update()
    sleep(2)
    ready()


def discard_image(image):
    background = pygame.image.load(BG_PATTERN)
    screen.blit(pygame.transform.scale(background, (X, Y)), (0, 0))
    message = Button(**del_msg_config)
    message.show()
    pygame.display.update()
    sleep(2)
    ready()


def exit_gui(image):
    sys.exit()


# Button settings

ready_button_config = {
    "name": "go",
    "width": int(X/8),
    "height": int(X/8),
    "x1": int(X/2 - X/16),
    "y1": int(Y/2 + X/16),
    "colour": READY_BG,
    "function": take_photo,
    "image": "resources/camera.png"
    }

ready_msg_config = {
    "name": "ready",
    "width": int(3*X/4),
    "height": int(Y/4),
    "x1": int(X/2 - 3*X/8),
    "y1": int(Y/4),
    "colour": READY_BG,
    "function": None,
    "text": "Take a photo!"
}

reject_button_config = {
    "name": "reject",
    "width": int(X - photo_display_width - 3 * MARGIN),
    "height": int(X - photo_display_width - 3 * MARGIN),
    "x1": photo_display_width + 2 * MARGIN,
    "y1": int(X - photo_display_width - MARGIN),
    "colour": DELETE_BG,
    "function": discard_image,
    "image": "resources/delete.png"
    }

accept_button_config = {
    "name": "accept",
    "width": int(X - photo_display_width - 3 * MARGIN),
    "height": int(X - photo_display_width - 3 * MARGIN),
    "x1": photo_display_width + 2 * MARGIN,
    "y1": MARGIN,
    "colour": SAVE_BG,
    "function": save_image,
    "image": "resources/like.png"
    }

save_msg_config = {
    "name": "saved",
    "width": int(3*X/4),
    "height": int(Y/4),
    "x1": int(X/2 - 3*X/8),
    "y1": int(Y/2 - Y/8),
    "colour": SAVE_BG,
    "function": None,
    "text": "The image is saved"
    }

del_msg_config = {
    "name": "deleted",
    "width": int(3*X/4),
    "height": int(Y/4),
    "x1": int(X/2 - 3*X/8),
    "y1": int(Y/2 - Y/8),
    "colour": DELETE_BG,
    "function": None,
    "text": "The image is gone"
    }

exit_button_config = {
    "name": "exit",
    "width": int((X - photo_display_width - 3 * MARGIN)/2),
    "height": int((X - photo_display_width - 3 * MARGIN)/2),
    "x1": photo_display_width + 2 * MARGIN,
    "y1": int(2*(X - photo_display_width - 1.5 * MARGIN)),
    "colour": (255, 255, 255),
    "function": exit_gui,
    "image": "resources/close.png",
    "alpha": None
    }


ready()

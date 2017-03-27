from picamera import PiCamera
from time import sleep
from io import BytesIO

camera = PiCamera()

def take_picture():
    camera.start_preview()
    camera.preview.alpha = 128
    stream = BytesIO()
    sleep(2)
    camera.capture(stream,'jpeg')
    return stream


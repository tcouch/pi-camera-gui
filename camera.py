from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
camera.rotation = 180
sleep(5)
camera.capture('/home/pi/Desktop/hayley.jpg')
camera.stop_preview()

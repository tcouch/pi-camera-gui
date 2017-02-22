from picamera import PiCamera
from time import sleep
from gpiozero import Button

button = Button(4, pull_up=False)
camera = PiCamera()

camera.start_preview()
button.wait_for_press()
camera.capture('/home/pi/Desktop/tom1.jpg')
camera.stop_preview()

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if GPIO.input(4):
        print("switch is closed")
    else:
        print("switch is open")

GPIO.cleanup()

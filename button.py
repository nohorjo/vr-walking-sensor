import RPi.GPIO as GPIO

def create(pin, callback):
    GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback = lambda x: callback())

class Button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    def is_pressed(self):
        return GPIO.input(self.pin)

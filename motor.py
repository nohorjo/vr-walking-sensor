import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BCM)

Seq = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1],
]

class Motor:
    def __init__(self, pins):
        self.pins = pins
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)

    def disable(self):
        self.__setStep([0, 0, 0, 0])

    def rotate(self, degrees):
        if degrees < 0:
            steps = Seq
            delay = 0.001
        else:
            steps = list(reversed(Seq[::2]))
            delay = 0.002
        for i in range(round(abs(degrees) * 1.422)):
            for step in steps:
                self.__setStep(step)
                sleep(delay)

    def __setStep(self, values):
        for pin, value in zip(self.pins, values):
            GPIO.output(pin, value)


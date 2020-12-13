import RPi.GPIO as GPIO
from time import sleep
import _thread
 
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
        self.turning = False
        self.__interrupt = False
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)

    def disable(self):
        self.__set_step([0, 0, 0, 0])

    def rotate(self, degrees):
        if self.turning:
            self.__interrupt = True
            while self.turning:
                pass
            self.__interrupt = False

        _thread.start_new_thread(self.__rotate, (degrees,))

    def __rotate(self, degrees):
        if degrees < 0:
            steps = Seq
            delay = 0.001
        else:
            steps = list(reversed(Seq[::2]))
            delay = 0.002
        self.turning = True
        for i in range(round(abs(degrees) * 1.422)):
            for step in steps:
                if self.__interrupt:
                    self.turning = False
                    return
                self.__set_step(step)
                sleep(delay)
        self.turning = False

    def __set_step(self, values):
        for pin, value in zip(self.pins, values):
            GPIO.output(pin, value)


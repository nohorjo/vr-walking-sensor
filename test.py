import display
from button import Button
from motor import Motor
from accelerometers import Accelerometers

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

try:
    sensor = Accelerometers([5])
    m = Motor([22, 23, 24, 25])
    buttonLeft = Button(17)
    buttonCenter = Button(18)
    buttonRight = Button(27)

    angles = [10, 20, 30, 45, 60, 90, 120, 180, 240, 275, 360]
    selectedAngle = 0
    display.text('Will rotate %d' % angles[selectedAngle], 0)

    printAcc = True

    while True:
        data = sensor.getData()

        print(data)
        
        if printAcc:
            display.text('Acc x: %.3f' % data['ax'], 2)
            display.text('Acc y: %.3f' % data['ay'], 3)
            display.text('Acc z: %.3f' % data['az'], 4)
        else:
            display.text('Rot x: %.3f' % data['gx'], 2)
            display.text('Rot y: %.3f' % data['gy'], 3)
            display.text('Rot z: %.3f' % data['gz'], 4)

        if buttonLeft.isPressed():
            display.text('Rotate anticlockwise', 1)
            m.rotate(-angles[selectedAngle])

        if buttonCenter.isPressed():
            printAcc = not printAcc
            selectedAngle = (selectedAngle + 1) % len(angles)
            display.text('Will rotate %d' % angles[selectedAngle], 0)

        if buttonRight.isPressed():
            display.text('Rotate clockwise', 1)
            m.rotate(angles[selectedAngle])

        display.show()

        sleep(0.16)
finally:
    display.clear()
    GPIO.cleanup()


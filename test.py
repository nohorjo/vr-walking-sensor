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
    button_left = Button(17)
    button_center = Button(18)
    button_right = Button(27)

    angles = [10, 20, 30, 45, 60, 90, 120, 180, 240, 275, 360]
    selected_angle = 0
    display.text('Will rotate %d' % angles[selected_angle], 0)

    printAcc = True

    while True:
        data = sensor.get_data()

        print(data)
        
        if printAcc:
            display.text('Acc x: %.3f' % data['ax'], 2)
            display.text('Acc y: %.3f' % data['ay'], 3)
            display.text('Acc z: %.3f' % data['az'], 4)
        else:
            display.text('Rot x: %.3f' % data['gx'], 2)
            display.text('Rot y: %.3f' % data['gy'], 3)
            display.text('Rot z: %.3f' % data['gz'], 4)

        if button_left.is_pressed():
            display.text('Rotate anticlockwise', 1)
            m.rotate(-angles[selected_angle])

        if button_center.is_pressed():
            printAcc = not printAcc
            selected_angle = (selected_angle + 1) % len(angles)
            display.text('Will rotate %d' % angles[selected_angle], 0)

        if button_right.is_pressed():
            display.text('Rotate clockwise', 1)
            m.rotate(angles[selected_angle])

        display.show()

        sleep(0.16)
finally:
    display.clear()
    GPIO.cleanup()


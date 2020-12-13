import display
from button import Button
from motor import Motor
from accelerometers import Accelerometers

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

try:
    button_left = Button(4)
    button_center = Button(17)
    button_right = Button(18)

    sensor = Accelerometers([
        27, # brown
        22, # yellow
        23, # orange
    ])

    motor_x = Motor([
        24, # black
        25, # purple
        5, # white
        6, # green
    ])
    motor_y = Motor([
        12, # orange
        13, # red
        16, # brown
        26, # yellow
    ])

    angles = [10, 20, 30, 45, 60, 90, 120, 180, 240, 275, 360]
    selected_angle = 0

    selected_sensor = 0

    display.text('Will rotate %d' % angles[selected_angle], 0)

    printAcc = True

    while True:
        data = sensor.get_data(selected_sensor)

        print(data)
        
        if printAcc:
            display.text('Acc x: %.3f, s %d' % (data['ax'], selected_sensor), 2)
            display.text('Acc y: %.3f' % data['ay'], 3)
            display.text('Acc z: %.3f' % data['az'], 4)
        else:
            display.text('Rot x: %.3f, s %d' % (data['gx'], selected_sensor), 2)
            display.text('Rot y: %.3f' % data['gy'], 3)
            display.text('Rot z: %.3f' % data['gz'], 4)

        if button_left.is_pressed():
            display.text('Rotate anticlockwise', 1)
            motor_x.rotate(-angles[selected_angle])
            selected_sensor = 0

        if button_center.is_pressed():
            printAcc = not printAcc
            selected_angle = (selected_angle + 1) % len(angles)
            display.text('Will rotate %d' % angles[selected_angle], 0)
            selected_sensor = 1

        if button_right.is_pressed():
            display.text('Rotate clockwise', 1)
            motor_x.rotate(angles[selected_angle])
            selected_sensor = 2

        display.show()

        sleep(0.16)
finally:
    display.clear()
    GPIO.cleanup()
    print('Cleanup')


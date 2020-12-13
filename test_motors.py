#!/usr/bin/env python3

from motor import Motor

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

try:
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

    while True:
        print(angles[selected_angle])

        if not (motor_y.turning and motor_x.turning):
            motor_y.rotate(angles[selected_angle])
            motor_x.rotate(-angles[selected_angle])

            selected_angle = (selected_angle + 1) % len(angles)

        sleep(1)
finally:
    GPIO.cleanup()
    print('Cleanup')


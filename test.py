import display
from button import Button
from motor import Motor

from time import sleep
from mpu6050 import mpu6050
import RPi.GPIO as GPIO

try:
    sensor = mpu6050(0x68)
    m = Motor([22, 23, 24, 25])
    buttonLeft = Button(17)
    buttonCenter = Button(18)
    buttonRight = Button(27)

    angles = [10, 20, 30, 45, 60, 90, 120, 180, 240, 275, 360]
    selectedAngle = 0
    display.text('Will rotate %d' % angles[selectedAngle], 0)

    printAcc = True

    while True:
        accelerometer_data = sensor.get_accel_data()
        gyro_data = sensor.get_gyro_data()

        print('acc', accelerometer_data, 'gyro', gyro_data)
        
        if printAcc:
            display.text('Acc x: %f' % accelerometer_data['x'], 2)
            display.text('Acc y: %f' % accelerometer_data['y'], 3)
            display.text('Acc z: %f' % accelerometer_data['z'], 4)
        else:
            display.text('Rot x: %f' % gyro_data['x'], 2)
            display.text('Rot y: %f' % gyro_data['y'], 3)
            display.text('Rot z: %f' % gyro_data['z'], 4)

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
except:
    display.clear()
    GPIO.cleanup()


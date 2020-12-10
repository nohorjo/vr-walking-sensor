import display
import button
from motor import Motor

from time import sleep
from mpu6050 import mpu6050
import RPi.GPIO as GPIO

sensor = mpu6050(0x68)
m = Motor([22, 23, 24, 25])

angles = [10, 20, 30, 45, 60, 90, 120, 180, 240, 275, 360]
selectedAngle = 0
display.text('Will rotate %d' % angles[selectedAngle], 0)

printAcc = True

def button_callback1():
    global printAcc, angles, selectedAngle
    printAcc = not printAcc
    display.text('Rotate anticlockwise', 1)
    display.show()
    m.rotate(-angles[selectedAngle])

def button_callback2():
    global printAcc, angles, selectedAngle
    printAcc = not printAcc
    selectedAngle = (selectedAngle + 1) % len(angles)
    display.text('Will rotate %d' % angles[selectedAngle], 0)
    display.show()

def button_callback3():
    global printAcc, angles, selectedAngle
    display.text('Rotate clockwise', 1)
    printAcc = not printAcc
    display.show()
    m.rotate(angles[selectedAngle])

button.create(17, button_callback1)
button.create(18, button_callback2)
button.create(27, button_callback3)

try:
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

        display.show()

        sleep(0.25)
except:
    display.clear()
    GPIO.cleanup()


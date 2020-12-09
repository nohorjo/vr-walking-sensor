import display
import button

from time import sleep

from mpu6050 import mpu6050

sensor = mpu6050(0x68)

printAcc = True

def button_callback1():
    global printAcc
    display.text('1 pressed', 0)
    printAcc = not printAcc
    display.show()

def button_callback2():
    global printAcc
    display.text('2 pressed', 0)
    printAcc = not printAcc
    display.show()

def button_callback3():
    global printAcc
    display.text('3 pressed', 0)
    printAcc = not printAcc
    display.show()

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

        sleep(1)
except:
    display.clear()


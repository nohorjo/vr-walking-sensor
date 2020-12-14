from mpu6050 import mpu6050
import RPi.GPIO as GPIO
from time import sleep

import display

class Accelerometers:
    def __init__(self, pins, sample_size = 20):
        self.pins = pins
        self.offsets = []

        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

        for index, pin in enumerate(pins):
            display.text('init %d' % index, 0)
            display.show()
            self.offsets.append({
                'gx': 0,
                'gy': 0,
                'gz': 0,
                'ax': 0,
                'ay': 0,
                'az': 0,
            })
            GPIO.output(pin, 1)
            sleep(0.01)
            self.sensor = mpu6050(0x69)
            self.calibrate(index, sample_size)

    def get_data(self, index = 0):
        pin = self.pins[index]
        offsets = self.offsets[index]

        GPIO.output(pin, 1)
        sleep(0.01)
        data = self.__get_data_no_set()
        GPIO.output(pin, 0)

        return {
            'gx': data['gx'] - offsets['gx'],
            'gy': data['gy'] - offsets['gy'],
            'gz': data['gz'] - offsets['gz'],
            'ax': data['ax'] - offsets['ax'],
            'ay': data['ay'] - offsets['ay'],
            'az': data['az'] - offsets['az'],
        }

    def __get_data_no_set(self, sample_size = 10):
        gx = 0
        gy = 0
        gz = 0
        ax = 0
        ay = 0
        az = 0

        for x in range(sample_size):
            got_data = False
            for y in range(10):
                try:
                    gyro_data = self.sensor.get_gyro_data()
                    accelerometer_data = self.sensor.get_accel_data()
                    got_data = True
                    break
                except:
                    sleep(0.01)
            if got_data:
                gx = gx + gyro_data['x']
                gy = gy + gyro_data['y']
                gz = gz + gyro_data['z']
                ax = ax + accelerometer_data['x']
                ay = ay + accelerometer_data['y']
                az = az + accelerometer_data['z']
            else:
                sample_size = sample_size - 1

        if sample_size is 0:
            sample_size = 1

        gx = gx / sample_size
        gy = gy / sample_size
        gz = gz / sample_size
        ax = ax / sample_size
        ay = ay / sample_size
        az = az / sample_size
    
        return {
            'gx': gx,
            'gy': gy,
            'gz': gz,
            'ax': ax,
            'ay': ay,
            'az': az,
        }

    def calibrate(self, index, sample_size = 2000):
        pin = self.pins[index]

        gx = 0
        gy = 0
        gz = 0
        ax = 0
        ay = 0
        az = 0

        GPIO.output(pin, 1)
        sleep(0.01)

        for x in range(sample_size):
            data = self.__get_data_no_set()
            gx = gx + data['gx']
            gy = gy + data['gy']
            gz = gz + data['gz']
            ax = ax + data['ax']
            ay = ay + data['ay']
            az = az + data['az']

        GPIO.output(pin, 0)

        offset = self.offsets[index]

        offset['gx'] = gx / sample_size
        offset['gy'] = gy / sample_size
        offset['gz'] = gz / sample_size
        offset['ax'] = ax / sample_size
        offset['ay'] = ay / sample_size
        offset['az'] = az / sample_size


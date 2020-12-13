from mpu6050 import mpu6050
import RPi.GPIO as GPIO
from time import sleep

class Accelerometers:
    def __init__(self, pins, sample_size = 200):
        self.pins = pins
        self.offsets = []

        for index, pin in enumerate(pins):
            self.offsets.append({
                'gx': 0,
                'gy': 0,
                'gz': 0,
                'ax': 0,
                'ay': 0,
                'az': 0,
            })
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 1)
            self.sensor = mpu6050(0x69)
            self.__calibrate(index, sample_size)

    def getData(self, index = 0):
        pin = self.pins[index]
        offsets = self.offsets[index]

        GPIO.output(pin, 1)
        data = self.__getDataNoSet()
        GPIO.output(pin, 0)

        return {
            'gx': data['gx'] - offsets['gx'],
            'gy': data['gy'] - offsets['gy'],
            'gz': data['gz'] - offsets['gz'],
            'ax': data['ax'] - offsets['ax'],
            'ay': data['ay'] - offsets['ay'],
            'az': data['az'] - offsets['az'],
        }

    def __getDataNoSet(self, sample_size = 20):
        gx = 0
        gy = 0
        gz = 0
        ax = 0
        ay = 0
        az = 0

        for x in range(sample_size):
            for y in range(10):
                try:
                    gyro_data = self.sensor.get_gyro_data()
                    accelerometer_data = self.sensor.get_accel_data()
                    break
                except:
                    sleep(0.01)
            gx = gx + gyro_data['x']
            gy = gy + gyro_data['y']
            gz = gz + gyro_data['z']
            ax = ax + accelerometer_data['x']
            ay = ay + accelerometer_data['y']
            az = az + accelerometer_data['z']

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

    def __calibrate(self, index, sample_size = 2000):
        pin = self.pins[index]

        gx = 0
        gy = 0
        gz = 0
        ax = 0
        ay = 0
        az = 0

        GPIO.output(pin, 1)

        for x in range(sample_size):
            data = self.__getDataNoSet()
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


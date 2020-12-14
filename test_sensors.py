#!/usr/bin/env python3

from accelerometers import Accelerometers
import display
import loading

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

try:
    pins = [
        22, # yellow #brown
        23, # orange #red
        #  27, # brown #white
    ]
    sensor = Accelerometers(pins, sample_size = 1)
    loading.done = True
    display.clear()

    while True:
        data = []
        for i in range(len(pins)):
            data.append(sensor.get_data(i))

        if True: # csv
            print('%.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f' % (
                data[0]['ax'],
                data[0]['ay'],
                data[0]['az'],
                data[0]['gx'],
                data[0]['gy'],
                data[0]['gz'],
                data[1]['ax'],
                data[1]['ay'],
                data[1]['az'],
                data[1]['gx'],
                data[1]['gy'],
                data[1]['gz'],
            ))
        else:
            print("")
            for i in range(len(pins)):
                d = data[i]
                print('%d = ax: %.2f, ay: %.2f, az: %.2f\tgx: %.2f, gy: %.2f, gz: %.2f' % (
                    i, d['ax'], d['ay'], d['az'], d['gx'], d['gy'], d['gz'],
                ))
            print("")

        sleep(0.5)
finally:
    GPIO.cleanup()


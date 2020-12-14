#!/usr/bin/env python3

from accelerometers import Accelerometers
import display

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

try:
    sensor = Accelerometers([
        27, # brown
        22, # yellow
        23, # orange
    ])
    display.clear()

    while True:
        data = [None, None, None]
        for i in range(3):
            data[i] = sensor.get_data(i)

        print("""
            0 = ax: %.2f, ay: %.2f, az: %.2f\tgx: %.2f, gy: %.2f, gz: %.2f
            1 = ax: %.2f, ay: %.2f, az: %.2f\tgx: %.2f, gy: %.2f, gz: %.2f
            2 = ax: %.2f, ay: %.2f, az: %.2f\tgx: %.2f, gy: %.2f, gz: %.2f
        """ % (
            data[0]['ax'], data[0]['ay'], data[0]['az'], data[0]['gx'], data[0]['gy'], data[0]['gz'], 
            data[1]['ax'], data[1]['ay'], data[1]['az'], data[1]['gx'], data[1]['gy'], data[1]['gz'], 
            data[2]['ax'], data[2]['ay'], data[2]['az'], data[2]['gx'], data[2]['gy'], data[2]['gz'], 
        ))
        
        sleep(0.5)
finally:
    GPIO.cleanup()


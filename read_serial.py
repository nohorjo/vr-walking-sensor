#!/usr/bin/env python3

from serial import Serial
from time import sleep

s = Serial('/dev/ttyUSB0', 115200)
sleep(2)

try:
    while True:
        m = s.readline().decode().rstrip()
        print(m)
        sleep(11/1000)
finally:
    s.close()
